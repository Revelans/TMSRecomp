# resist_popup.py <out.png> [font]: the RESIST hit popup art (s106), drawn like the game's WEAK popup: tilted chunky
# caps, vertical gradient fill, dark outline glow. 408x184 (2x the 204x92 atlas cell; pad_icons scales it down).
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 408, 184
font = ImageFont.truetype(sys.argv[2] if len(sys.argv) > 2 else 'C:/Windows/Fonts/Montserrat-BlackItalic.otf', 96)
text = 'RESIST'
big = Image.new('L', (W * 2, H * 2), 0)
ImageDraw.Draw(big).text((W, H), text, font=font, anchor='mm', fill=255)
mask = big.rotate(7, resample=Image.BICUBIC, center=(W, H)).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
bbox = mask.getbbox()
top, bot = (255, 255, 255), (96, 150, 220)  # white -> steel blue
grad = Image.new('RGBA', (W, H))
for y in range(H):
    t = min(1, max(0, (y - bbox[1]) / max(1, bbox[3] - bbox[1])))
    c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
    ImageDraw.Draw(grad).line([(0, y), (W, y)], fill=c + (255,))
outline = mask.filter(ImageFilter.MaxFilter(11))
glow = outline.filter(ImageFilter.GaussianBlur(4))
out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
out.paste(Image.new('RGBA', (W, H), (16, 16, 40, 200)), (0, 0), glow)
out.paste(Image.new('RGBA', (W, H), (20, 24, 56, 255)), (0, 0), outline)
out.paste(grad, (0, 0), mask)
out.save(sys.argv[1])
print(bbox)
