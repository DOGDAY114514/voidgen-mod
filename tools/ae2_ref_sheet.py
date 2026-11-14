import os
from PIL import Image

root = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
names = ["item_storage_cell_1k.png", "item_storage_cell_256k.png", "item_cell_housing.png", "cell_component_1k.png", "cell_component_256k.png", "storage_cell_led.png"]
scale = 8
cell = 16 * scale
pad = 12
img = Image.new("RGBA", (pad + len(names) * (cell + pad), pad + cell + pad), (30, 30, 34, 255))
for i, n in enumerate(names):
    tile = Image.open(os.path.join(root, n)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    img.alpha_composite(tile, (pad + i * (cell + pad), pad))
out = r"D:\AI\voidgen-mod\docs\ae2_ref\ae2_cells.png"
img.save(out)
print("saved", out, img.size)