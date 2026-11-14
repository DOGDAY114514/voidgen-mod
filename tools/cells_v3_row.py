import os
from PIL import Image
cells = r"D:\AI\voidgen-mod\docs\cells_v3"
order = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
scale = 12
px = 16 * scale
pad = 12
w = pad + len(order) * (px + pad)
img = Image.new("RGBA", (w, 2 * (px + pad) + 2 * pad), (26, 28, 34, 255))
for i, t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad))
for i, f in enumerate(["void_cell_housing.png", "void_component.png"]):
    img.alpha_composite(Image.open(os.path.join(cells, f)).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad + px + pad))
out = r"D:\AI\voidgen-mod\docs\cells_v3_row.png"
img.save(out)
print("saved", out, img.size)