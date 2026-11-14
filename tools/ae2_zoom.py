import os
from PIL import Image

base = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
files = ["item_storage_cell_1k.png", "item_cell_housing.png", "item_storage_cell_256k.png",
         "cell_component_1k.png", "cell_component_256k.png", "storage_cell_led.png"]
scale = 20
cell = 16 * scale
pad = 16
img = Image.new("RGBA", (pad + len(files) * (cell + pad), pad + cell + pad), (30, 32, 38, 255))
for i, f in enumerate(files):
    tile = Image.open(os.path.join(base, f)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    img.alpha_composite(tile, (pad + i * (cell + pad), pad))
out = r"D:\AI\voidgen-mod\docs\ae2_ref\ae2_zoom.png"
img.save(out)
print("saved", out, img.size)
print("order:", files)