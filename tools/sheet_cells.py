import os
from PIL import Image

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
names = ["void_ingot.png", "void_component.png", "void_cell_housing.png"] + ["void_cell_%s.png" % t for t in ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]]
scale = 9
cell = 16 * scale
pad = 12
cols = 7
rows = (len(names) + cols - 1) // cols
img = Image.new("RGBA", (pad + cols * (cell + pad), pad + rows * (cell + pad)), (20, 22, 28, 255))
for i, n in enumerate(names):
    tile = Image.open(os.path.join(root, n)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    img.alpha_composite(tile, (pad + (i % cols) * (cell + pad), pad + (i // cols) * (cell + pad)))
out = r"D:\AI\voidgen-mod\docs\ae_cells_v1.png"
img.save(out)
print("saved", out, img.size)