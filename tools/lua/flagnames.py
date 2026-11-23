"""Dump global number constants (FLG_* = n) from compiled Lua 5.2 scripts (game flag definitions).
python tools/lua/flagnames.py <FlagXxx.lua>... > flags.txt   (prints "0x<hex> NAME", sorted by value)"""
import struct, sys


def parse(d):
    p = 18 + 4 + 4 + 3  # header, linedefined, lastlinedefined, numparams/is_vararg/maxstack

    def u32():
        nonlocal p
        v = struct.unpack_from("<I", d, p)[0]
        p += 4
        return v
    code = [u32() for _ in range(u32())]
    consts = []
    for _ in range(u32()):
        t = d[p]
        p += 1
        if t == 3:
            consts.append(struct.unpack_from("<d", d, p)[0])
            p += 8
        elif t == 4:
            n = u32()
            consts.append(d[p:p + n - 1].decode("latin1"))
            p += n
        elif t == 1:
            consts.append(bool(d[p]))
            p += 1
        else:
            consts.append(None)
    return code, consts


out = {}
for path in sys.argv[1:]:
    code, k = parse(open(path, "rb").read())
    regs = {}
    for ins in code:
        op, a = ins & 0x3F, (ins >> 6) & 0xFF
        c, b = (ins >> 14) & 0x1FF, (ins >> 23) & 0x1FF
        bx = ins >> 14
        rk = lambda x: k[x - 256] if x >= 256 else regs.get(x)
        if op == 1:  # LOADK
            regs[a] = k[bx]
        elif op == 8:  # SETTABUP _ENV[RK(B)] = RK(C)
            name, val = rk(b), rk(c)
            if isinstance(name, str) and isinstance(val, float):
                out[name] = int(val)
for name, v in sorted(out.items(), key=lambda x: x[1]):
    print(f"{v:#06x} {name}")
