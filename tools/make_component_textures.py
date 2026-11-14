import os
from PIL import Image

ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
outdir = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"

TIERS = {
    "1k": (64, 150, 255),
    "4k": (94, 200, 255),
    "16k": (86, 224, 206),
    "64k": (94, 226, 150),
    "256k": (150, 222, 96),
    "1m": (226, 196, 84),
    "4m": (242, 152, 72),
    "16m": (238, 108, 108),
    "64m": (188, 128, 255),
    "256m": (226, 232, 240),
}

def recolor_component(path, rgb):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    light = tuple(int(c + (255 - c) * 0.35) for c in rgb)
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            lum = (r + g + b) / 3.0
            if mx - mn >= 30 and b > r and b >= g - 8:
                if lum > 170:
                    px[x, y] = (light[0], light[1], light[2], a)
                elif lum > 110:
                    px[x, y] = (rgb[0], rgb[1], rgb[2], a)
                else:
                    px[x, y] = (int(rgb[0] * 0.72), int(rgb[1] * 0.72), int(rgb[2] * 0.72), a)
    # one sparkle
    px[1, 1] = (186, 252, 255, 255)
    return img

square = os.path.join(ref, "cell_component_256k.png")
round1k = os.path.join(ref, "cell_component_1k.png")
for tier, rgb in TIERS.items():
    base = round1k if tier == "1k" else square
    img = recolor_component(base, rgb)
    img.save(os.path.join(outdir, f"void_component_{tier}.png"))
print("components written:", len(TIERS))

# preview sheet
scale = 12
px = 16 * scale
pad = 12
row = list(TIERS.keys())
w = pad + len(row) * (px + pad)
sheet = Image.new("RGBA", (w, px + 2 * pad), (26, 28, 34, 255))
for i, t in enumerate(row):
    sheet.alpha_composite(Image.open(os.path.join(outdir, f"void_component_{t}.png")).convert("RGBA").resize((px, px), Image.NEAREST),
                          (pad + i * (px + pad), pad))
sheet.save(r"D:\AI\voidgen-mod\docs\void_components_v1.png")
print("saved sheet")