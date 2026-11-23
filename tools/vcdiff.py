"""VCDIFF (RFC 3284) decoder for xdelta3 / Delta Patcher patches without secondary compression.

Usage:
    python tools/vcdiff.py <source file> <patch.xdelta> <output file>

Checks the xdelta3 per-window Adler-32, so a patch made for another game version fails instead of writing a bad file.
"""
import struct
import sys
import zlib

MAGIC = b"\xd6\xc3\xc4\x00"
NOOP, ADD, RUN, COPY = 0, 1, 2, 3
S_NEAR, S_SAME = 4, 3


def default_code_table():
    """The RFC 3284 section 5.6 default table: 256 entries of (type1, size1, mode1, type2, size2, mode2)."""
    t = [(RUN, 0, 0, NOOP, 0, 0)]
    t += [(ADD, s, 0, NOOP, 0, 0) for s in range(0, 18)]
    for m in range(S_NEAR + S_SAME + 2):
        t.append((COPY, 0, m, NOOP, 0, 0))
        t += [(COPY, s, m, NOOP, 0, 0) for s in range(4, 19)]
    for m in range(6):  # RFC order: mode outermost, then ADD size, then COPY size
        for a in range(1, 5):
            t += [(ADD, a, 0, COPY, s, m) for s in range(4, 7)]
    for m in range(6, 9):
        for a in range(1, 5):
            t.append((ADD, a, 0, COPY, 4, m))
    t += [(COPY, 4, m, ADD, 1, 0) for m in range(9)]
    assert len(t) == 256
    return t


TABLE = default_code_table()


class Reader:
    def __init__(self, buf, pos=0):
        self.buf, self.pos = buf, pos

    def byte(self):
        b = self.buf[self.pos]
        self.pos += 1
        return b

    def int(self):
        v = 0
        while True:
            b = self.buf[self.pos]
            self.pos += 1
            v = v << 7 | (b & 0x7F)
            if not b & 0x80:
                return v

    def take(self, n):
        b = self.buf[self.pos:self.pos + n]
        self.pos += n
        return b


def decode_window(src_seg, data, inst, addr, tlen):
    out = bytearray()
    d, i, a = Reader(data), Reader(inst), Reader(addr)
    near = [0] * S_NEAR
    same = [0] * (S_SAME * 256)
    slot = 0
    slen = len(src_seg)
    while i.pos < len(inst):
        code = i.byte()
        t1, s1, m1, t2, s2, m2 = TABLE[code]
        for t, s, m in ((t1, s1, m1), (t2, s2, m2)):
            if t == NOOP:
                continue
            if s == 0:
                s = i.int()
            if t == ADD:
                out += d.take(s)
            elif t == RUN:
                out += bytes([d.byte()]) * s
            else:
                here = slen + len(out)
                if m == 0:
                    x = a.int()
                elif m == 1:
                    x = here - a.int()
                elif m < 2 + S_NEAR:
                    x = near[m - 2] + a.int()
                else:
                    x = same[(m - 2 - S_NEAR) * 256 + a.byte()]
                near[slot] = x
                slot = (slot + 1) % S_NEAR
                same[x % (S_SAME * 256)] = x
                if x + s <= slen:
                    out += src_seg[x:x + s]
                else:
                    if x < slen:  # source tail, then target start
                        n = slen - x
                        out += src_seg[x:]
                        s -= n
                        x = 0
                    else:
                        x -= slen
                    while s > 0:  # may overlap the bytes being written
                        n = min(s, len(out) - x)
                        if n <= 0:
                            raise ValueError("bad copy address %d (target %d)" % (x, len(out)))
                        out += out[x:x + n]
                        x += n
                        s -= n
    if len(out) != tlen:
        raise ValueError("window size %d, expected %d" % (len(out), tlen))
    return out


def apply(src_path, patch_path, out_path, progress=True):
    with open(patch_path, "rb") as f:
        p = f.read()
    if p[:4] != MAGIC:
        raise ValueError("not a VCDIFF file")
    r = Reader(p, 4)
    hdr = r.byte()
    if hdr & 1:
        raise ValueError("secondary compression not supported (id %d)" % r.byte())
    if hdr & 2:
        raise ValueError("custom code table not supported")
    if hdr & 4:
        r.take(r.int())
    windows = 0
    with open(src_path, "rb") as src, open(out_path, "wb") as out:
        while r.pos < len(p):
            win = r.byte()
            src_seg = b""
            if win & 3:
                if win & 2:
                    raise ValueError("VCD_TARGET windows not supported")
                slen = r.int()
                spos = r.int()
                src.seek(spos)
                src_seg = src.read(slen)
                if len(src_seg) != slen:
                    raise ValueError("source file too short (wrong file or version)")
            r.int()  # length of the delta encoding
            tlen = r.int()
            if r.byte():
                raise ValueError("compressed sections not supported")
            dl, il, al = r.int(), r.int(), r.int()
            want = struct.unpack(">I", r.take(4))[0] if win & 4 else None
            data, inst, addr = r.take(dl), r.take(il), r.take(al)
            w = decode_window(src_seg, data, inst, addr, tlen)
            if want is not None and zlib.adler32(w) != want:
                raise ValueError("checksum mismatch in window %d: the source file is not the one this patch was made for"
                                 % windows)
            out.write(w)
            windows += 1
            if callable(progress) and windows % 64 == 0:
                progress(r.pos, len(p))  # patch bytes read so far (setup.py --mod)
            elif progress and windows % 64 == 0:
                print("  %d windows, %d MB" % (windows, out.tell() >> 20), flush=True)
    return windows


def selftest():
    # ADD "abc", COPY 3 from source at 0, COPY 6 from target start (overlapping run), RUN 2 'z'.
    src = b"XYZ"
    data = b"abc" + b"z"
    inst = bytes([4, 19, 3]) + bytes([19, 6]) + bytes([0, 2])  # ADD 3; COPY size 0 mode 0 (size 3); COPY 6; RUN 2
    addr = bytes([0, 3])  # mode 0 absolute: 0 (source), 3 (= target start)
    w = decode_window(src, data, inst, addr, 14)
    assert bytes(w) == b"abcXYZabcXYZzz", w


if __name__ == "__main__":
    selftest()
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    n = apply(sys.argv[1], sys.argv[2], sys.argv[3])
    print("ok: %d windows -> %s" % (n, sys.argv[3]))
