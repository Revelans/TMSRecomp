"""NSO loader: decompress an NSO into a flat image and read its dynamic symbols.

Format from Switchbrew (NSO, MOD0) and the ELF64 spec. Usage:
    python tools/nso.py <nso> [--out image.bin] [--json info.json]
"""
import argparse
import json
import struct
import sys

DT_NULL, DT_STRTAB, DT_SYMTAB, DT_STRSZ, DT_RELA, DT_RELASZ, DT_JMPREL, DT_PLTRELSZ = 0, 5, 6, 10, 7, 8, 23, 2
DT_NEEDED, DT_INIT_ARRAY, DT_INIT_ARRAYSZ = 1, 25, 27
DT_REL, DT_RELSZ = 17, 18
SHN_UNDEF = 0


def lz4_block(src, size):
    """LZ4 block decompression (the NSO segment format). Own code: setup ships no lz4 package."""
    out = bytearray()
    i, n = 0, len(src)
    while i < n:
        tok = src[i]
        i += 1
        lit = tok >> 4
        if lit == 15:
            while True:
                b = src[i]
                i += 1
                lit += b
                if b != 255:
                    break
        out += src[i:i + lit]
        i += lit
        if i >= n:
            break
        off = src[i] | src[i + 1] << 8
        i += 2
        ml = tok & 15
        if ml == 15:
            while True:
                b = src[i]
                i += 1
                ml += b
                if b != 255:
                    break
        ml += 4
        start = len(out) - off
        if off >= ml:
            out += out[start:start + ml]
        else:  # overlapping match: repeat the last `off` bytes
            out += (out[start:] * (ml // off + 1))[:ml]
    if len(out) != size:
        raise ValueError(f"lz4: {len(out)} bytes, expected {size}")
    return bytes(out)


class Nso:
    def __init__(self, data, is64=True):
        self.is64 = is64
        if data[:4] != b"NSO0":
            raise ValueError("not an NSO")
        flags = struct.unpack_from("<I", data, 0xC)[0]
        self.segments = []  # (name, mem_off, size)
        image_size = 0
        parts = []
        for i, name in enumerate(("text", "ro", "data")):
            file_off, mem_off, size = struct.unpack_from("<III", data, 0x10 + i * 0x10)
            file_size = struct.unpack_from("<I", data, 0x60 + i * 4)[0]
            raw = data[file_off:file_off + file_size]
            seg = lz4_block(raw, size) if flags & (1 << i) else raw
            if len(seg) != size:
                raise ValueError(f"{name}: size {len(seg)} != {size}")
            self.segments.append((name, mem_off, size))
            parts.append((mem_off, seg))
            image_size = max(image_size, mem_off + size)
        self.bss_size = struct.unpack_from("<I", data, 0x3C)[0]
        self.module_id = data[0x40:0x60].hex()
        img = bytearray(image_size)
        for off, seg in parts:
            img[off:off + len(seg)] = seg
        self.image = img
        self._read_mod0()

    def _read_mod0(self):
        img = self.image
        mod0 = struct.unpack_from("<I", img, 4)[0]
        if img[mod0:mod0 + 4] != b"MOD0":
            raise ValueError("MOD0 missing")
        dyn, bss_s, bss_e, eh_s, eh_e, _obj = (struct.unpack_from("<i", img, mod0 + 4 + 4 * k)[0] + mod0 for k in range(6))
        self.mod0, self.bss = mod0, (bss_s, bss_e)
        self.eh_frame_hdr = (eh_s, eh_e)
        if len(img) < bss_e:  # bss lives past the file image
            img.extend(bytes(bss_e - len(img)))
        tags = {}
        needed = []
        p = dyn
        dyn_fmt, dyn_size = ("<qQ", 16) if self.is64 else ("<iI", 8)
        while True:
            tag, val = struct.unpack_from(dyn_fmt, img, p)
            p += dyn_size
            if tag == DT_NULL:
                break
            if tag == DT_NEEDED:
                needed.append(val)
            tags.setdefault(tag, val)
        self.dynamic = tags
        strtab, strsz = tags.get(DT_STRTAB, 0), tags.get(DT_STRSZ, 0)
        strs = bytes(img[strtab:strtab + strsz])

        def cstr(off):
            return strs[off:strs.index(b"\0", off)].decode("utf-8", "replace")

        self.needed = [cstr(o) for o in needed]
        # dynsym has no count in DT; it ends where dynstr starts (linker places them adjacent) - checked below.
        symtab = tags.get(DT_SYMTAB, 0)
        sym_size = 24 if self.is64 else 16
        end = strtab if strtab > symtab else symtab + sym_size * 0x10000
        self.symbols = []  # (name, value, size, info, shndx)
        for q in range(symtab, end, sym_size):
            if self.is64:
                name_off, info, _other, shndx, value, size = struct.unpack_from("<IBBHQQ", img, q)
            else:
                name_off, value, size, info, _other, shndx = struct.unpack_from("<IIIBBH", img, q)
            if name_off >= strsz:
                break
            self.symbols.append((cstr(name_off), value, size, info, shndx))
        self.relocs = []  # (offset, type, sym index, addend or None for REL)
        rel_tables = ((DT_RELA, DT_RELASZ), (DT_JMPREL, DT_PLTRELSZ)) if self.is64 else             ((DT_REL, DT_RELSZ), (DT_JMPREL, DT_PLTRELSZ))
        for start_tag, size_tag in rel_tables:
            start, size = tags.get(start_tag), tags.get(size_tag, 0)
            if start is None:
                continue
            if self.is64:
                for q in range(start, start + size, 24):
                    off, info, addend = struct.unpack_from("<QQq", img, q)
                    self.relocs.append((off, info & 0xFFFFFFFF, info >> 32, addend))
            else:  # 32-bit Switch titles use REL: addend is the word already at the target
                for q in range(start, start + size, 8):
                    off, info = struct.unpack_from("<II", img, q)
                    self.relocs.append((off, info & 0xFF, info >> 8, None))

    def imports(self):
        return [s for s in self.symbols if s[4] == SHN_UNDEF and s[0]]

    def exports(self):
        return [s for s in self.symbols if s[4] != SHN_UNDEF and s[0]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nso")
    ap.add_argument("--out")
    ap.add_argument("--json")
    ap.add_argument("--npdm", help="main.npdm; its flags say 32- or 64-bit (default: next to the NSO)")
    a = ap.parse_args()
    import os
    npdm = a.npdm or os.path.join(os.path.dirname(a.nso), "main.npdm")
    is64 = True
    if os.path.exists(npdm):
        with open(npdm, "rb") as f:
            is64 = bool(f.read(0x10)[0xC] & 1)  # META MmuFlags bit 0: Is64BitInstruction
    with open(a.nso, "rb") as f:
        n = Nso(f.read(), is64)
    if a.out:
        with open(a.out, "wb") as f:
            f.write(n.image)
    info = {
        "is64": n.is64,
        "module_id": n.module_id,
        "segments": [{"name": s, "off": hex(o), "size": hex(z)} for s, o, z in n.segments],
        "bss": [hex(x) for x in n.bss],
        "eh_frame_hdr": [hex(x) for x in n.eh_frame_hdr],
        "needed": n.needed,
        "imports": len(n.imports()),
        "exports": len(n.exports()),
        "relocs": len(n.relocs),
        "reloc_types": sorted({r[1] for r in n.relocs}),
    }
    print(json.dumps(info, indent=1))
    if a.json:
        info["import_names"] = [s[0] for s in n.imports()]
        info["export_names"] = [[s[0], hex(s[1]), s[2]] for s in n.exports()]
        with open(a.json, "w") as f:
            json.dump(info, f, indent=1)


if __name__ == "__main__":
    sys.exit(main())
