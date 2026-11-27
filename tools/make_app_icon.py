# make_app_icon.py: draws runtime/launcher/app.ico, our own icon for tmslauncher.exe / tms.exe in the release (no game art:
# a sharp sign on a dark tile with a mirror-shard glow, in the launcher's colours). python tools/make_app_icon.py
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1024
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "..", "runtime", "launcher", "app.ico")

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))

bg = Image.new("RGBA", (S, S))
px = bg.load()
for y in range(S):
    for x in range(S):
        t = min(1, max(0, (x * 0.4 + y * 0.6) / S))
        px[x, y] = lerp((22, 38, 31, 255), (8, 12, 11, 255), t)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle((24, 24, S - 24, S - 24), radius=210, fill=255)
icon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
icon.paste(bg, (0, 0), mask)

# mirror shards: two thin light diagonals
shard = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(shard)
d.polygon([(560, 24), (700, 24), (300, S - 24), (160, S - 24)], fill=(85, 227, 152, 38))
d.polygon([(760, 24), (800, 24), (400, S - 24), (360, S - 24)], fill=(127, 227, 208, 30))
icon.alpha_composite(Image.composite(shard, Image.new("RGBA", (S, S)), mask))

# the sharp sign, glow + gradient fill
font = ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", 760)
glyph = Image.new("L", (S, S), 0)
gd = ImageDraw.Draw(glyph)
box = gd.textbbox((0, 0), "\u266f", font=font)
gd.text(((S - (box[2] - box[0])) / 2 - box[0], (S - (box[3] - box[1])) / 2 - box[1]), "\u266f", font=font, fill=255)
glow = Image.new("RGBA", (S, S), (52, 210, 127, 0))
glow.putalpha(glyph.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.8)))
icon.alpha_composite(glow)
grad = Image.new("RGBA", (S, S))
gp = grad.load()
for y in range(S):
    c = lerp((235, 255, 244, 255), (52, 210, 127, 255), y / S)
    for x in range(S): gp[x, y] = c
icon.paste(grad, (0, 0), glyph)

# a small star sparkle top right
sp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(sp).polygon([(800, 150), (822, 228), (900, 250), (822, 272), (800, 350), (778, 272), (700, 250), (778, 228)], fill=(255, 255, 255, 235))
icon.alpha_composite(sp)

ImageDraw.Draw(icon).rounded_rectangle((24, 24, S - 24, S - 24), radius=210, outline=(52, 210, 127, 150), width=10)
icon.resize((256, 256), Image.LANCZOS).save(out, sizes=[(256, 256), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)])
icon.resize((256, 256), Image.LANCZOS).save(os.path.join(os.environ.get("ICON_PREVIEW_DIR", here), "app_icon_preview.png"))
print(out)
