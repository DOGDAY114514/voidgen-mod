import os
from PIL import Image

cells = r"D:\AI\voidgen-mod\docs\cells_v2"
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
order = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
scale = 12
cell_px = 16 * scale
pad = 12
w = pad + (len(order) + 3) * (cell_px + pad)
h = pad * 2 + 2 * (cell_px + pad)
img = Image.new("RGBA", (w, h), (26, 28, 34, 255))
for i, t in enumerate(order):
    tile = Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((cell_px, cell_px), Image.NEAREST)
    img.alpha_composite(tile, (pad + i * (cell_px + pad), pad))
for i, f in enumerate(["item_storage_cell_1k.png", "item_cell_housing.png", "item_storage_cell_256k.png"]):
    tile = Image.open(os.path.join(ref, f)).convert("RGBA").resize((cell_px, cell_px), Image.NEAREST)
    img.alpha_composite(tile, (pad + i * (cell_px + pad), pad + cell_px + pad))
for i, f in enumerate(["void_ingot.png", "void_component.png", "void_cell_housing.png"]):
    tile = Image.open(os.path.join(cells, f)).convert("RGBA").resize((cell_px, cell_px), Image.NEAREST)
    img.alpha_composite(tile, (pad + (i + 3) * (cell_px + pad), pad + cell_px + pad))
out = r"D:\AI\voidgen-mod\docs\cells_v2_compare.png"
img.save(out)
print("saved", out, img.size)