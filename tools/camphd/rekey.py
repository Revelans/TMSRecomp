"""Rename <data>/movie_hd/<subdir>/<name>_<hash>.ivf from the single-packet key to the two-packet key (camphd.py
first_packet_hash), so story movies with the same black first packet get their own 4K file (s95).
Usage: rekey.py <usm dir> <movie_hd subdir>"""
import os
import sys
import tempfile

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import usm2ivf  # noqa: E402
from camphd import first_packet_hash  # noqa: E402


def main(usm_dir, hd_dir):
    usms = {f[:-4]: os.path.join(r, f) for r, _, fs in os.walk(usm_dir) for f in fs if f.endswith(".usm")}
    for f in sorted(os.listdir(hd_dir)):
        name, ext = f[:-21], f[-21:]
        if not f.endswith(".ivf") or len(f) < 22 or f[-21] != "_" or name not in usms:
            continue
        tmp = os.path.join(tempfile.gettempdir(), "rekey.ivf")
        open(tmp, "wb").write(b"".join(usm2ivf.frames(open(usms[name], "rb").read())))
        old, new = first_packet_hash(tmp, 1), first_packet_hash(tmp, 2)
        os.remove(tmp)
        if int(ext[1:17], 16) == old:
            os.replace(os.path.join(hd_dir, f), os.path.join(hd_dir, "%s_%016x.ivf" % (name, new)))
            print(f, "->", "%s_%016x.ivf" % (name, new))


if __name__ == "__main__":
    main(*sys.argv[1:3])
