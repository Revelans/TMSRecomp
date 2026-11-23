"""Convert the runtime's 32-bit BMP frame dumps to PNG (stdlib only).

    python tools/bmp2png.py in.bmp [out.png] [--scale 2] [--r11g11b10] [--crop x0,y0,x1,y1 [--zoom 2]]

--r11g11b10: the dump is a raw B10G11R11 float target (NX_DUMP_RT of an HDR target); clamped to 0..1.
"""
import struct
import sys
import zlib


def uf(v, mbits):  # unsigned small float: 5-bit exponent, mbits mantissa
    e, m = v >> mbits, v & ((1 << mbits) - 1)
    if e == 0:
        return m / (1 << mbits) * 2.0 ** -14
    return 65504.0 if e == 31 else (1 + m / (1 << mbits)) * 2.0 ** (e - 15)


def main():
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else src[:-4] + ".png"
    scale = int(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 1
    packed = "--r11g11b10" in sys.argv
    d = open(src, "rb").read()
    off, w, h = struct.unpack_from("<I", d, 10)[0], struct.unpack_from("<i", d, 18)[0], struct.unpack_from("<i", d, 22)[0]
    top_down = h < 0
    h = abs(h)
    x0, y0, x1, y1 = (int(v) for v in sys.argv[sys.argv.index("--crop") + 1].split(",")) if "--crop" in sys.argv else (0, 0, w, h)
    zoom = int(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 1
    rows = []
    for y in range(y0, y1, scale):
        sy = y if top_down else h - 1 - y
        row = d[off + sy * w * 4: off + (sy + 1) * w * 4]
        px = bytearray()
        for x in range(x0, x1, scale):
            if packed:
                v = struct.unpack_from("<I", row, 4 * x)[0]
                r, g, b = (min(255, int(uf(c, mb) ** (1 / 2.2) * 255)) for c, mb in
                           ((v & 0x7FF, 6), (v >> 11 & 0x7FF, 6), (v >> 22, 5)))
            else:
                b, g, r = row[4 * x], row[4 * x + 1], row[4 * x + 2]
            px += bytes((r, g, b)) * zoom
        rows += [b"\0" + bytes(px)] * zoom
    ow, oh = (x1 - x0 + scale - 1) // scale * zoom, (y1 - y0 + scale - 1) // scale * zoom

    def chunk(t, data):
        return struct.pack(">I", len(data)) + t + data + struct.pack(">I", zlib.crc32(t + data) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", ow, oh, 8, 2, 0, 0, 0)) + \
        chunk(b"IDAT", zlib.compress(b"".join(rows), 6)) + chunk(b"IEND", b"")
    open(dst, "wb").write(png)
    print(dst, ow, oh)


if __name__ == "__main__":
    main()
