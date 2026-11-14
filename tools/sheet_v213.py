import os
from PIL import Image
cells = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
order = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 12
px = 16*scale
pad = 12
w = pad + len(order)*(px+pad)
img = Image.new("RGBA", (w, 2*(px+pad)+2*pad), (26,28,34,255))
for i,t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px,px), Image.NEAREST), (pad+i*(px+pad), pad))
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
row = [("cells","void_cell_housing.png"),("cells","void_component.png"),("ref","item_storage_cell_1k.png"),("ref","item_cell_housing.png"),("ref","item_storage_cell_256k.png")]
for i,(kind,f) in enumerate(row):
    base = cells if kind=="cells" else ref
    img.alpha_composite(Image.open(os.path.join(base,f)).convert("RGBA").resize((px,px), Image.NEAREST), (pad+i*(px+pad), pad+px+pad))
img.save(r"D:\AI\voidgen-mod\docs\ae_cells_v3.png")
print("sheet updated")