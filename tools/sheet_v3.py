import os
from PIL import Image

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
names = [
    ("block", "nothing_collector_1.png"), ("block", "nothing_collector_2.png"),
    ("block", "nothing_collector_3.png"), ("block", "nothing_collector_4.png"),
    ("block", "nothing_collector_5.png"), ("block", "nothing_distributor.png"),
    ("item", "void_storage_iron.png"), ("item", "void_storage_gold.png"),
    ("item", "void_storage_diamond.png"), ("item", "void_storage_emerald.png"),
    ("item", "void_storage_nether.png"),
    ("item", "filled_void_storage_iron.png"), ("item", "filled_void_storage_gold.png"),
    ("item", "filled_void_storage_diamond.png"), ("item", "filled_void_storage_emerald.png"),
    ("item", "mob_spawner.png"), ("item", "void_configurator.png"),
]
scale = 10
cell = 16 * scale
cols = 6
rows = (len(names) + cols - 1) // cols
pad = 12
img = Image.new("RGBA", (pad + cols * (cell + pad), pad + rows * (cell + pad)), (22, 24, 30, 255))
for i, (sub, n) in enumerate(names):
    tile = Image.open(os.path.join(root, sub, n)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    x = pad + (i % cols) * (cell + pad)
    y = pad + (i // cols) * (cell + pad)
    img.alpha_composite(tile, (x, y))
out = r"D:\AI\voidgen-mod\docs\textures_v3.png"
img.save(out)
print("saved", out, img.size)