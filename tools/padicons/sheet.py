# sheet.py <dump dir> <candidates.txt> <out.bmp>: contact sheet of candidate discs (64 px cells, 16 per row, on blue)
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from find_discs import load_dds
lines = [l.split() for l in open(sys.argv[2]) if l.strip()]
C, cols = 64, 16
rows = (len(lines) + cols - 1) // cols
sheet = np.zeros((rows * (C + 14), cols * C, 3), np.float32); sheet[:] = (90, 60, 40)  # BGR
cache = {}
for i, (f, x, y, w, h) in enumerate(lines):
    x, y, w, h = map(int, (x, y, w, h))
    im = cache.setdefault(f, load_dds(os.path.join(sys.argv[1], f)))
    s = max(w, h) + 4
    crop = im[max(0, y - 2):y - 2 + s, max(0, x - 2):x - 2 + s].astype(np.float32)
    k = C / s
    iy = (np.arange(C) / k).astype(int).clip(0, crop.shape[0] - 1); ix = (np.arange(C) / k).astype(int).clip(0, crop.shape[1] - 1)
    c = crop[iy][:, ix]
    a = c[..., 3:4] / 255
    oy, ox = (i // cols) * (C + 14), (i % cols) * C
    cell = sheet[oy:oy + C, ox:ox + C]
    sheet[oy:oy + C, ox:ox + C] = cell * (1 - a) + c[..., 2::-1] * a
H, W = sheet.shape[:2]
row = (W * 3 + 3) & ~3
hdr = b'BM' + (54 + row * H).to_bytes(4, 'little') + b'\0\0\0\0' + (54).to_bytes(4, 'little') + (40).to_bytes(4, 'little') + \
      W.to_bytes(4, 'little') + (-H).to_bytes(4, 'little', signed=True) + (1).to_bytes(2, 'little') + (24).to_bytes(2, 'little') + bytes(24)
data = np.zeros((H, row), np.uint8); data[:, :W * 3] = sheet.clip(0, 255).astype(np.uint8).reshape(H, W * 3)
open(sys.argv[3], 'wb').write(hdr + data.tobytes())
