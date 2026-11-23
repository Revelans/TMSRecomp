"""Load and link the game's NSOs the way rtld would, into one prelinked guest image.

Output (all under private/, never committed):
  image.bin   guest memory from IMAGE_BASE to the end of the last module (relocated, bss zeroed)
  layout.json module bases/segments/exidx, symbol table, import thunks
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import nso  # noqa: E402

R_ARM_ABS32, R_ARM_GLOB_DAT, R_ARM_JUMP_SLOT, R_ARM_RELATIVE = 2, 21, 22, 23
STT_FUNC = 2

IMAGE_BASE = 0x00200000  # 32-bit "no reserve" address space code start (main), as on Horizon
THUNK_SIZE = 16


def align(v, a):
    return (v + a - 1) & ~(a - 1)


class Module:
    def __init__(self, name, path, base):
        with open(path, "rb") as f:
            self.n = nso.Nso(f.read(), is64=False)
        self.name, self.base = name, base
        self.size = align(self.n.bss[1], 0x1000)
        self.text = (base, base + self.n.segments[0][2])
        self.ro = (base + self.n.segments[1][1], base + self.n.segments[1][1] + self.n.segments[1][2])
        self.data = (base + self.n.segments[2][1], base + self.size)
        self.exports = {s[0]: (base + s[1], s[2], s[3] & 0xF) for s in self.n.exports()}


def link(exefs, names=("main", "sdk")):
    mods = []
    base = IMAGE_BASE
    for nm in names:
        m = Module(nm, os.path.join(exefs, nm), base)
        mods.append(m)
        base = align(base + m.size, 0x100000)
    thunk_base = base
    img = bytearray(thunk_base - IMAGE_BASE)
    for m in mods:
        o = m.base - IMAGE_BASE
        img[o:o + len(m.n.image)] = m.n.image
    thunks = {}  # name -> addr

    def lookup(name):
        for m in mods:
            e = m.exports.get(name)
            if e:
                return e[0]
        if name not in thunks:
            thunks[name] = thunk_base + THUNK_SIZE * len(thunks)
        return thunks[name]

    rel_targets = set()  # code pointers found in data (vtables, fn pointers)
    for m in mods:
        syms = m.n.symbols
        o = m.base - IMAGE_BASE
        for off, typ, si, _ in m.n.relocs:
            p = o + off
            a = struct.unpack_from("<I", img, p)[0]
            if typ == R_ARM_RELATIVE:
                v = m.base + a
            elif typ in (R_ARM_ABS32, R_ARM_GLOB_DAT, R_ARM_JUMP_SLOT):
                name, value, _sz, info, shndx = syms[si]
                s = lookup(name) if name else m.base + value
                v = s + a if typ == R_ARM_ABS32 else s
            else:
                raise ValueError(f"{m.name}: reloc type {typ} at {off:#x}")
            v &= 0xFFFFFFFF
            struct.pack_into("<I", img, p, v)
            rel_targets.add(v)
    img.extend(bytes(THUNK_SIZE * len(thunks)))
    return mods, img, thunks, rel_targets


def exidx_starts(m):
    s, e = m.n.eh_frame_hdr  # on AArch32 MOD0's eh_frame_hdr fields bound .ARM.exidx
    out = []
    for p in range(s, e, 8):
        w0 = struct.unpack_from("<I", m.n.image, p)[0]
        off = ((w0 & 0x7FFFFFFF) ^ 0x40000000) - 0x40000000  # prel31
        out.append(m.base + ((p + off) & 0xFFFFFFFF))
    return out


def main():
    exefs, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    mods, img, thunks, rel_targets = link(exefs)
    with open(os.path.join(out, "image.bin"), "wb") as f:
        f.write(img)
    layout = {
        "image_base": IMAGE_BASE,
        "image_size": len(img),
        "modules": [{
            "name": m.name, "base": m.base, "size": m.size, "text": m.text, "ro": m.ro, "data": m.data,
            "init": m.base + m.n.dynamic.get(12, 0) if 12 in m.n.dynamic else None,
            "init_array": [m.base + m.n.dynamic[25], m.n.dynamic[27]] if 25 in m.n.dynamic else None,
            "exports": {k: v[0] for k, v in m.exports.items()},
        } for m in mods],
        "thunks": thunks,
        "code_ptrs": sorted(v for v in rel_targets if any(m.text[0] <= v < m.text[1] for m in mods)),
    }
    with open(os.path.join(out, "layout.json"), "w") as f:
        json.dump(layout, f, indent=1)
    print(f"image {len(img):#x} bytes, {len(thunks)} thunks: {sorted(thunks)[:12]}...")


if __name__ == "__main__":
    main()
