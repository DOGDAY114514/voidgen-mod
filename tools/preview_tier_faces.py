import os
from PIL import Image
TEX = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block"
rows = []
names = []
for face in ("void_generator_top", "void_generator_side", "void_furnace_top", "void_furnace_side"):
    for tier in range(6):
        names.append(face + ("" if tier == 0 else "_t%d" % tier))
scale = 6; cell = 16*scale; pad = 8
cols = 6
rows_n = (len(names)+cols-1)//cols
img = Image.new("RGBA", (pad + cols*(cell+pad), pad + rows_n*(cell+pad)), (22,24,30,255))
for i, n in enumerate(names):
    p = os.path.join(TEX, n + ".png")
    tile = Image.open(p).convert("RGBA").resize((cell, cell), Image.NEAREST)
    img.alpha_composite(tile, (pad + (i%cols)*(cell+pad), pad + (i//cols)*(cell+pad)))
out = r"D:\AI\voidgen-mod\docs\tier_faces.png"
img.save(out)
print("saved", out, img.size)