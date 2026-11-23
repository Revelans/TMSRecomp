"""CRI USM -> IVF (the VP9 video chunks), so ffmpeg can decode the camp movies. Usage: usm2ivf.py in.usm out.ivf"""
import struct
import sys


def frames(usm):
    pos = 0
    while pos + 8 <= len(usm):
        sig, size = usm[pos:pos + 4], struct.unpack_from(">I", usm, pos + 4)[0]
        if sig == b"@SFV":
            hdr, pad = usm[pos + 9], struct.unpack_from(">H", usm, pos + 10)[0]
            if usm[pos + 15] & 3 == 0:  # data chunk (1 = header, 2 = end, 3 = seek)
                yield usm[pos + 8 + hdr:pos + 8 + size - pad]
        pos += 8 + size


def main(src, dst):
    # the camp movies' video chunks already hold an IVF stream (DKIF header in the first chunk, then IVF frame records)
    fs = list(frames(open(src, "rb").read()))
    assert fs and fs[0][:4] == b"DKIF", "video chunks are not IVF"
    open(dst, "wb").write(b"".join(fs))
    print(src, len(fs) - 1, "frames")


if __name__ == "__main__":
    main(*sys.argv[1:3])
