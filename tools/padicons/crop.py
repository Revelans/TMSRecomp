# crop.py <dds> <x> <y> <w> <h> <scale> <out.bmp>: nearest-neighbour zoom of an RGBA8 dump region over blue (for labelling)
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from find_discs import load_dds
f, x, y, w, h, k, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
c = load_dds(f)[y:y + h, x:x + w].astype(np.float32)
c = c.repeat(k, 0).repeat(k, 1)
a = c[..., 3:4] / 255
img = np.array([90, 60, 40], np.float32) * (1 - a) + c[..., 2::-1] * a
H, W = img.shape[:2]; row = (W * 3 + 3) & ~3
hdr = b'BM' + (54 + row * H).to_bytes(4, 'little') + bytes(4) + (54).to_bytes(4, 'little') + (40).to_bytes(4, 'little') + \
      W.to_bytes(4, 'little') + (-H).to_bytes(4, 'little', signed=True) + (1).to_bytes(2, 'little') + (24).to_bytes(2, 'little') + bytes(24)
d = np.zeros((H, row), np.uint8); d[:, :W * 3] = img.clip(0, 255).astype(np.uint8).reshape(H, W * 3)
open(out, 'wb').write(hdr + d.tobytes())
