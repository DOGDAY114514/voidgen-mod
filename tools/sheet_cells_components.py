import os
from PIL import Image
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
tiers = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 8
cell = 16 * scale
pad = 10
img = Image.new("RGBA", (pad + 10*(cell+pad), pad*2 + 2*cell + pad), (24, 25, 31, 255))
for i, t in enumerate(tiers):
    comp = Image.open(os.path.join(base, "void_component_"+t+".png")).convert("RGBA").resize((cell,cell), Image.NEAREST)
    img.alpha_composite(comp, (pad + i*(cell+pad), pad))
for i, t in enumerate(tiers):
    disk = Image.open(os.path.join(base, "void_cell_"+t+".png")).convert("RGBA").resize((cell,cell), Image.NEAREST)
    img.alpha_composite(disk, (pad + i*(cell+pad), pad*2 + cell))
out = r"D:\AI\voidgen-mod\docs\void_disks_components.png"
img.save(out)
print("saved", out, img.size)