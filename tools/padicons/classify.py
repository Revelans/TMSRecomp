# classify.py <dump dir> <candidates.txt> <out prefix>: label button discs found by find_discs.py (A B X Y + - and
# "other") by comparing their glyph with reference glyphs from the labelled atlases (pad_icons.cpp k_atlases), grow the
# rect over a black ring if there is one, and write
#   <out>.txt   file x y w h label ring score   (every candidate)
#   <out>.bmp   contact sheet of the accepted ones, in label order (check it by eye)
#   <out>.cpp   pad_icons.cpp Cell tables per atlas for the accepted ones
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from find_discs import load_dds  # noqa: E402

REFS = [  # atlas hash, x, y, w, h, label (known cells)
    ("ea576a96a510fd6e", 6, 1236, 32, 31, "FACE_A"), ("ea576a96a510fd6e", 46, 1236, 32, 31, "FACE_B"),
    ("ea576a96a510fd6e", 86, 1236, 32, 32, "FACE_X"), ("ea576a96a510fd6e", 126, 1236, 32, 32, "FACE_Y"),
    ("ea576a96a510fd6e", 166, 1236, 32, 31, "PLUS"), ("ea576a96a510fd6e", 206, 1236, 32, 32, "MINUS"),
    ("34c763427410e392", 221, 4, 22, 22, "FACE_A"), ("34c763427410e392", 4, 35, 22, 22, "FACE_B"),
    ("34c763427410e392", 159, 4, 22, 22, "FACE_X"), ("34c763427410e392", 190, 4, 22, 22, "FACE_Y"),
    ("34c763427410e392", 128, 4, 22, 22, "PLUS"), ("34c763427410e392", 97, 4, 22, 22, "MINUS"),
]
N = 20


def glyph(im, x, y, w, h):
    """darkness of the inner disc (0..1), N x N, glyph centred and scaled to its bounding box"""
    c = im[y:y + h, x:x + w].astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    r = (w + h) / 4
    inside = ((yy - (h - 1) / 2) ** 2 + (xx - (w - 1) / 2) ** 2) <= (r * 0.8) ** 2
    lum = c[..., :3].mean(-1) * (c[..., 3] / 255) + 255 * (1 - c[..., 3] / 255)
    d = np.where(inside, (255 - lum) / 255, 0)
    ys, xs = np.nonzero(d > 0.25)
    if len(ys) < 4:
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    s = max(y1 - y0, x1 - x0)
    cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    iy = np.clip((cy - s / 2 + (np.arange(N) + 0.5) * s / N).astype(int), 0, h - 1)
    ix = np.clip((cx - s / 2 + (np.arange(N) + 0.5) * s / N).astype(int), 0, w - 1)
    g = d[iy][:, ix]
    g = g - g.mean()
    n = np.linalg.norm(g)
    return g / n if n else None


def ring(im, x, y, w, h):
    """pixels of dark opaque ring around the white disc (0: plain disc)"""
    H, W = im.shape[:2]
    for k in range(1, 6):
        x0, y0, x1, y1 = max(0, x - k), max(0, y - k), min(W, x + w + k), min(H, y + h + k)
        border = np.concatenate([im[y0, x0:x1], im[y1 - 1, x0:x1], im[y0:y1, x0], im[y0:y1, x1 - 1]])
        dark = (border[:, 3] > 160) & (border[:, :3].max(1) < 90)
        if dark.mean() < 0.5:
            return k - 1
    return 5


def main():
    dump, cand, out = sys.argv[1:4]
    files = {f.rsplit("_", 1)[-1][:-4]: f for f in os.listdir(dump) if f.endswith(".dds")}
    cache = {}

    def img(f):
        if f not in cache:
            if len(cache) > 8:
                cache.clear()
            cache[f] = load_dds(os.path.join(dump, f))
        return cache[f]

    refs = []
    for h_, x, y, w, h, lab in REFS:
        g = glyph(img(files[h_]), x, y, w, h)
        refs.append((lab, g))
    rows = []
    for line in open(cand):
        f, x, y, w, h = line.split()
        x, y, w, h = map(int, (x, y, w, h))
        im = img(f)
        g = glyph(im, x, y, w, h)
        if g is None:
            continue
        scores = sorted(((float((g * rg).sum()), lab) for lab, rg in refs), reverse=True)
        best, lab = scores[0]
        k = ring(im, x, y, w, h)
        rows.append((f, x - k, y - k, w + 2 * k, h + 2 * k, lab if best > 0.8 else "other", k, best))
    with open(out + ".txt", "w") as o:
        for r in rows:
            o.write("%s %d %d %d %d %s %d %.3f\n" % r)
    ok = sorted((r for r in rows if r[5] != "other"), key=lambda r: (r[5], r[0]))
    # sheet
    C, cols = 48, 20
    nr = (len(ok) + cols - 1) // cols
    sheet = np.zeros((max(1, nr) * C, cols * C, 3), np.float32)
    sheet[:] = (90, 60, 40)
    for i, (f, x, y, w, h, lab, k, sc) in enumerate(ok):
        im = img(f)[max(0, y):y + h, max(0, x):x + w].astype(np.float32)
        s = max(im.shape[0], im.shape[1])
        iy = np.clip((np.arange(C) * s / C).astype(int), 0, im.shape[0] - 1)
        ix = np.clip((np.arange(C) * s / C).astype(int), 0, im.shape[1] - 1)
        c = im[iy][:, ix]
        a = c[..., 3:4] / 255
        oy, ox = (i // cols) * C, (i % cols) * C
        sheet[oy:oy + C, ox:ox + C] = sheet[oy:oy + C, ox:ox + C] * (1 - a) + c[..., 2::-1] * a
    H, W = sheet.shape[:2]
    rw = (W * 3 + 3) & ~3
    hdr = b"BM" + (54 + rw * H).to_bytes(4, "little") + bytes(4) + (54).to_bytes(4, "little") + (40).to_bytes(4, "little") + \
        W.to_bytes(4, "little") + (-H).to_bytes(4, "little", signed=True) + (1).to_bytes(2, "little") + (24).to_bytes(2, "little") + bytes(24)
    d = np.zeros((H, rw), np.uint8)
    d[:, :W * 3] = sheet.clip(0, 255).astype(np.uint8).reshape(H, W * 3)
    open(out + ".bmp", "wb").write(hdr + d.tobytes())
    # C++ tables
    by = {}
    for f, x, y, w, h, lab, k, sc in ok:
        by.setdefault(f, []).append((x, y, w, h, lab, k))
    with open(out + ".cpp", "w") as o:
        for f, cells in sorted(by.items()):
            hsh = f.rsplit("_", 1)[-1][:-4]
            o.write("// %s\n" % f)
            o.write("const Cell k_%s[] = {%s};\n" % (hsh, ", ".join("{%d, %d, %d, %d, %s}" % c[:5] for c in cells)))
    print(len(rows), "candidates,", len(ok), "labelled, atlases:", len({r[0] for r in ok}))
    for i, r in enumerate(ok):
        print(i, r[0][:40], r[1:6], "ring %d score %.2f" % (r[6], r[7]))


if __name__ == "__main__":
    main()
