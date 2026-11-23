"""CRI CPK archive reader: @UTF tables, TOC, CRILAYLA decompression.

Usage:
    python tools/cpk.py list <cpk> [--grep substr]
    python tools/cpk.py extract <cpk> <outdir> [--grep substr]
"""
import argparse
import os
import struct
import sys

# @UTF column storage (high nibble) and type (low nibble)
ST_ZERO, ST_CONST, ST_ROW = 0x10, 0x30, 0x50
TYPES = {0: ">B", 1: ">b", 2: ">H", 3: ">h", 4: ">I", 5: ">i", 6: ">Q", 7: ">q", 8: ">f", 9: ">d"}
T_STR, T_DATA = 0xA, 0xB


def read_utf(buf, pos=0):
    """Parse an @UTF table at buf[pos]; returns (table name, list of row dicts)."""
    if buf[pos:pos + 4] != b"@UTF":
        raise ValueError("not @UTF")
    base = pos + 8
    _ver, rows_off, str_off, data_off, name_off, ncols, row_len, nrows = struct.unpack_from(">HHIIIHHI", buf, base)
    rows_off += base
    str_off += base
    data_off += base

    def cstr(o):
        o += str_off
        return buf[o:buf.index(b"\0", o)].decode("utf-8", "replace")

    def value(t, p):
        if t == T_STR:
            return cstr(struct.unpack_from(">I", buf, p)[0]), 4
        if t == T_DATA:
            o, n = struct.unpack_from(">II", buf, p)
            return bytes(buf[data_off + o:data_off + o + n]), 8
        f = TYPES[t]
        return struct.unpack_from(f, buf, p)[0], struct.calcsize(f)

    cols = []
    p = base + 0x18
    for _ in range(ncols):
        flags = buf[p]
        name = cstr(struct.unpack_from(">I", buf, p + 1)[0])
        p += 5
        const = None
        if flags & 0xF0 == ST_CONST:
            const, n = value(flags & 0xF, p)
            p += n
        cols.append((name, flags & 0xF0, flags & 0xF, const))
    rows = []
    for r in range(nrows):
        p = rows_off + r * row_len
        row = {}
        for name, st, t, const in cols:
            if st == ST_ROW:
                row[name], n = value(t, p)
                p += n
            elif st == ST_CONST:
                row[name] = const
            else:
                row[name] = None
        rows.append(row)
    return cstr(name_off), rows


def crilayla(src):
    """Decompress a CRILAYLA block (LZ read backwards, 0x100-byte raw prefix stored at the end)."""
    if src[:8] != b"CRILAYLA":
        return src
    usize, csize = struct.unpack_from("<II", src, 8)
    out = bytearray(usize + 0x100)
    out[:0x100] = src[0x10 + csize:0x10 + csize + 0x100]
    inp = 0x10 + csize - 1
    pool = 0
    left = 0

    def bits(n):
        nonlocal inp, pool, left
        v = 0
        while n:
            if left == 0:
                pool = src[inp]
                inp -= 1
                left = 8
            take = min(left, n)
            v = (v << take) | ((pool >> (left - take)) & ((1 << take) - 1))
            left -= take
            n -= take
        return v

    o = len(out) - 1
    while o >= 0x100:
        if bits(1):
            off = bits(13) + 3
            length = 3
            for w in (2, 3, 5):
                n = bits(w)
                length += n
                if n != (1 << w) - 1:
                    break
            else:
                while True:
                    n = bits(8)
                    length += n
                    if n != 0xFF:
                        break
            for _ in range(length):
                out[o] = out[o + off]
                o -= 1
        else:
            out[o] = bits(8)
            o -= 1
    return bytes(out)


class Cpk:
    def __init__(self, path):
        self.f = open(path, "rb")
        head = self.f.read(0x800)
        if head[:4] != b"CPK ":
            raise ValueError("not a CPK")
        _, rows = read_utf(head, 0x10)
        self.header = rows[0]
        toc_off, toc_size = self.header["TocOffset"], self.header["TocSize"]
        self.files = []
        if toc_off:
            self.f.seek(toc_off)
            toc = self.f.read(toc_size)
            _, self.files = read_utf(toc, 0x10)
            for r in self.files:
                r["_offset"] = r["FileOffset"] + 0x800  # measured: offsets count from the end of the 0x800 header, not TocOffset

    def path(self, r):
        d = r.get("DirName") or ""
        return f"{d}/{r['FileName']}" if d else r["FileName"]

    def read(self, r):
        self.f.seek(r["_offset"])
        data = self.f.read(r["FileSize"])
        if r["ExtractSize"] != r["FileSize"]:
            data = crilayla(data)
            if len(data) != r["ExtractSize"]:
                raise ValueError(f"{self.path(r)}: {len(data)} != {r['ExtractSize']}")
        return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "extract", "header"])
    ap.add_argument("cpk")
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--grep")
    a = ap.parse_args()
    c = Cpk(a.cpk)
    if a.cmd == "header":
        for k, v in c.header.items():
            print(k, v if not isinstance(v, bytes) else f"<{len(v)} bytes>")
        return
    for r in c.files:
        p = c.path(r)
        if a.grep and a.grep not in p:
            continue
        if a.cmd == "list":
            print(f"{r['FileSize']:>10} {r['ExtractSize']:>10} {p}")
        else:
            dst = os.path.join(a.outdir, p)
            os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
            with open(dst, "wb") as f:
                f.write(c.read(r))
    print(f"{len(c.files)} files", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
