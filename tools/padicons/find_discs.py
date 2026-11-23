# find_discs.py <dump dir> <out.txt>: candidate button discs (white opaque disc with a darker glyph inside) in the
# RGBA8 texture dumps (NX_TEX_DUMP *_25_*.dds). One line per candidate: file x y w h. Used to build pad_icons.cpp
# cell tables (labelled by eye from a contact sheet).
import sys, os, numpy as np
from collections import deque

def load_dds(path):
    b = open(path, 'rb').read()
    h, w = int.from_bytes(b[12:16], 'little'), int.from_bytes(b[16:20], 'little')
    pos = 148 if b[84:88] == b'DX10' else 128
    return np.frombuffer(b, np.uint8, w * h * 4, pos).reshape(h, w, 4)

def components(mask):
    h, w = mask.shape
    seen = np.zeros_like(mask, bool)
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        q = deque([(y0, x0)]); seen[y0, x0] = True
        y1, x1, ya, xa, n = y0, x0, y0, x0, 0
        while q:
            y, x = q.popleft(); n += 1
            ya, xa, y1, x1 = min(ya, y), min(xa, x), max(y1, y), max(x1, x)
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True; q.append((yy, xx))
        yield xa, ya, x1 - xa + 1, y1 - ya + 1, n

def main():
  out = []
  for f in sorted(os.listdir(sys.argv[1])):
      if '_25_' not in f or not f.endswith('.dds') or f.startswith('padicons'): continue
      im = load_dds(os.path.join(sys.argv[1], f)).astype(np.int32)
      opaque = im[..., 3] > 160
      white = opaque & (im[..., :3].min(-1) > 225)
      for x, y, w, h, n in components(white):
          if not (12 <= w <= 90 and 12 <= h <= 90 and abs(w - h) <= max(2, w // 8)): continue
          yy, xx = np.mgrid[0:h, 0:w]
          r = (w + h) / 4
          inside = ((yy - (h - 1) / 2) ** 2 + (xx - (w - 1) / 2) ** 2) <= (r * 0.92) ** 2
          sub_op = opaque[y:y + h, x:x + w]
          if sub_op[inside].mean() < 0.97: continue  # not a filled disc
          glyph = (~white[y:y + h, x:x + w]) & inside
          frac = glyph.mean() / inside.mean()
          if not (0.04 < frac < 0.55): continue
          out.append(f'{f} {x} {y} {w} {h}')
  open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
  print(len(out), 'candidates')


if __name__ == '__main__':
    main()
