"""Dump the layout records (LYTS blocks: doors, triggers, objects) of a map model.apak.
python tools/lyts.py <model.apak>   (record: type, id, position xyz, size xyz, rot y, named strings)"""
import struct, sys

d = open(sys.argv[1], "rb").read()


def cstr(a):
    return d[a:d.index(b"\0", a)].decode("latin1") if 0 <= a < len(d) else "?"


pos = d.find(b"LYTS")
while pos >= 0:
    ver, n, hdr = struct.unpack_from("<3I", d, pos + 4)
    print(f"LYTS @{pos:#x} version {ver} records {n}")
    for i in range(n):
        r = pos + hdr + i * 0xa0
        if r + 0xa0 > len(d):
            break
        typ, flags, rid = struct.unpack_from("<3I", d, r)
        p = struct.unpack_from("<3f", d, r + 0xc)
        s = struct.unpack_from("<3f", d, r + 0x18)
        roty = struct.unpack_from("<f", d, r + 0x28)[0]
        ints = struct.unpack_from("<8i", d, r + 0x48)
        strs = [cstr(pos + x) for x in struct.unpack_from("<15I", d, r + 0x64) if x]
        names = [x for x in strs if x]
        print(f"  [{i}] type {typ:#x} f {flags} id {rid:#x} pos ({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f}) size ({s[0]:.0f}, {s[1]:.0f}, {s[2]:.0f}) roty {roty:.0f} ints {ints[:6]} {names}")
    pos = d.find(b"LYTS", pos + 4)
