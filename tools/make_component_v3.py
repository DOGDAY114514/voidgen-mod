import os
from PIL import Image

ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
outdir = r"D:\AI\voidgen-mod\docs\cells_v3"
os.makedirs(outdir, exist_ok=True)

img = Image.open(os.path.join(ref, "cell_component_256k.png")).convert("RGBA")
px = img.load()
for y in range(16):
    for x in range(16):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        mx, mn = max(r, g, b), min(r, g, b)
        lum = (r + g + b) / 3.0
        if mx - mn >= 30 and b > r and b >= g - 8:
            if lum > 170:
                px[x, y] = (176, 240, 255, a)
            elif lum > 110:
                px[x, y] = (110, 206, 255, a)
            else:
                px[x, y] = (58, 138, 200, a)
        elif lum > 180:
            px[x, y] = (int(r * 0.97 + 240 * 0.03), int(g * 0.97 + 232 * 0.03), int(b * 0.97 + 255 * 0.03), a)
px[1, 1] = (186, 252, 255, 255)
px[14, 14] = (110, 200, 240, 255)
img.save(os.path.join(outdir, "void_component.png"))

# copy to resources
dst = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item\void_component.png"
img.save(dst)

# comparison sheet: ours vs AE2 1k / 4k? we only have 1k & 256k refs
scale = 20
pxs = 16 * scale
sheet = Image.new("RGBA", (3 * pxs + 4 * 16, pxs + 32), (26, 28, 34, 255))
ours = Image.open(dst).convert("RGBA").resize((pxs, pxs), Image.NEAREST)
c1k = Image.open(os.path.join(ref, "cell_component_1k.png")).convert("RGBA").resize((pxs, pxs), Image.NEAREST)
c256 = Image.open(os.path.join(ref, "cell_component_256k.png")).convert("RGBA").resize((pxs, pxs), Image.NEAREST)
sheet.alpha_composite(ours, (16, 16))
sheet.alpha_composite(c1k, (pxs + 32, 16))
sheet.alpha_composite(c256, (2 * pxs + 48, 16))
sheet.save(r"D:\AI\voidgen-mod\docs\component_vs_ae2.png")
print("saved component + comparison")