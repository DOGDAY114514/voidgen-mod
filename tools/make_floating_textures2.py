import io, os
from PIL import Image

def clamp(v): return max(0, min(255, int(v)))
def recolor_block(src, out):
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    ramp = [(34, 24, 58), (78, 56, 122), (132, 106, 182), (188, 174, 228), (222, 246, 255)]
    n = len(ramp) - 1
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            pos = (lum / 255.0) * n
            i = min(n - 1, int(pos)); f = pos - i
            c0, c1 = ramp[i], ramp[i + 1]
            px[x, y] = (clamp(c0[0] + (c1[0]-c0[0])*f),
                        clamp(c0[1] + (c1[1]-c0[1])*f),
                        clamp(c0[2] + (c1[2]-c0[2])*f), a)
    img.save(out)

res = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block"
ref = r"D:\AI\voidgen-mod\docs\ref_floating"
for key in ("damaged", "chipped", "flawed", "flawless"):
    recolor_block(os.path.join(ref, key + ".png"), os.path.join(res, "floating_budding_" + key + ".png"))

sheet = Image.new("RGBA", (4*96 + 5*12, 96 + 2*12), (22, 24, 30, 255))
for i, key in enumerate(("damaged", "chipped", "flawed", "flawless")):
    tile = Image.open(os.path.join(res, "floating_budding_" + key + ".png")).convert("RGBA").resize((96, 96), Image.NEAREST)
    sheet.alpha_composite(tile, (12 + i*(96+12), 12))
# also item row
items = [os.path.join(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item", n) for n in ("floating_crystal.png", "floating_crystal_dust.png")]
full = Image.new("RGBA", (4*96 + 5*12, 2*96 + 3*12), (22, 24, 30, 255))
full.alpha_composite(sheet, (0, 0))
for i, f in enumerate(items):
    tile = Image.open(f).convert("RGBA").resize((96, 96), Image.NEAREST)
    full.alpha_composite(tile, (12 + i*(96+12), 96 + 2*12))
full.save(r"D:\AI\voidgen-mod\docs\floating_crystals_v1.png")
print("done")