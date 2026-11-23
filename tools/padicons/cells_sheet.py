# cells_sheet.py <dump dir> <out.bmp> file:x,y,w,h ... : each rect (+6 px margin) zoomed to 96 px, in a row of 10
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from find_discs import load_dds
dump, out, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
C, cols, M = 96, 10, 6
rows = (len(specs) + cols - 1) // cols
sheet = np.zeros((rows * C, cols * C, 3), np.float32); sheet[:] = (90, 60, 40)
files = {f.rsplit('_', 1)[-1][:-4]: f for f in os.listdir(dump) if f.endswith('.dds')}
for i, s in enumerate(specs):
    h_, r = s.split(':'); x, y, w, h = map(int, r.split(','))
    im = load_dds(os.path.join(dump, files[h_]))
    x0, y0 = max(0, x - M), max(0, y - M)
    c = im[y0:y + h + M, x0:x + w + M].astype(np.float32)
    sz = max(c.shape[:2])
    iy = np.clip((np.arange(C) * sz / C).astype(int), 0, c.shape[0] - 1); ix = np.clip((np.arange(C) * sz / C).astype(int), 0, c.shape[1] - 1)
    c = c[iy][:, ix]; a = c[..., 3:4] / 255
    oy, ox = (i // cols) * C, (i % cols) * C
    sheet[oy:oy + C, ox:ox + C] = sheet[oy:oy + C, ox:ox + C] * (1 - a) + c[..., 2::-1] * a
H, W = sheet.shape[:2]; rw = (W * 3 + 3) & ~3
hdr = b'BM' + (54 + rw * H).to_bytes(4, 'little') + bytes(4) + (54).to_bytes(4, 'little') + (40).to_bytes(4, 'little') + \
      W.to_bytes(4, 'little') + (-H).to_bytes(4, 'little', signed=True) + (1).to_bytes(2, 'little') + (24).to_bytes(2, 'little') + bytes(24)
d = np.zeros((H, rw), np.uint8); d[:, :W * 3] = sheet.clip(0, 255).astype(np.uint8).reshape(H, W * 3)
open(out, 'wb').write(hdr + d.tobytes())
