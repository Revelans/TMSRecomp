"""Disassemble a guest function from the linked image with call targets named. python tools/dis.py <addr|symbol> [n]"""
import json, struct, sys
from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

L = json.load(open("private/tms/link/layout.json"))
img = open("private/tms/link/image.bin", "rb").read()
B = L["image_base"]
names = {}
for m in L["modules"]:
    for k, v in m["exports"].items():
        names.setdefault(v, k)
for k, v in L["thunks"].items():
    names[v] = "thunk:" + k
inv = {v: k for k, v in names.items()}
arg = sys.argv[1]
a = int(arg, 16) if arg.startswith("0x") else inv[arg]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)


def plt(t):
    w0, w1, w2 = (struct.unpack_from("<I", img, t - B + 4 * k)[0] for k in range(3))
    if (w0 & 0xFFFFF000) == 0xE28FC000 and (w2 & 0xFFFFF000) == 0xE5BCF000:
        ror = lambda v, r: ((v >> r) | (v << (32 - r))) & 0xFFFFFFFF if r else v
        got = t + 8 + ror(w0 & 0xFF, ((w0 >> 8) & 15) * 2) + ror(w1 & 0xFF, ((w1 >> 8) & 15) * 2) + (w2 & 0xFFF)
        return struct.unpack_from("<I", img, got - B)[0]
    return t


print(f"{a:#x} {names.get(a, '')}")
for x in range(a, a + 4 * n, 4):
    i = next(md.disasm(img[x - B:x - B + 4], x), None)
    if i is None:
        print(f"  {x:#x} .word {struct.unpack_from('<I', img, x - B)[0]:#010x}")
        continue
    extra = ""
    if i.mnemonic.startswith("bl") or i.mnemonic.startswith("b"):
        if i.op_str.startswith("#"):
            t = plt(int(i.op_str[1:], 16))
            extra = "  ; " + names.get(t, hex(t))
    print(f"  {x:#x} {i.mnemonic:8s} {i.op_str}{extra}")
