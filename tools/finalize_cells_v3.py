import io, os, shutil
from PIL import Image

src = r"D:\AI\voidgen-mod\docs\cells_v3"
dst = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
for f in os.listdir(src):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
print("copied", len([f for f in os.listdir(src) if f.endswith('.png')]))

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.1"', 'version="2.1.2"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)

bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.1.jar", "voidgen-2.1.2.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

# comparison sheet
cells = dst
order = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
scale = 12
px = 16 * scale
pad = 12
w = pad + len(order) * (px + pad)
img = Image.new("RGBA", (w, 2 * (px + pad) + 2 * pad), (26, 28, 34, 255))
for i, t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad))
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
row = [("cells", "void_cell_housing.png"), ("cells", "void_component.png"),
       ("ref", "item_storage_cell_1k.png"), ("ref", "item_cell_housing.png"), ("ref", "item_storage_cell_256k.png")]
for i, (kind, f) in enumerate(row):
    base = cells if kind == "cells" else ref
    img.alpha_composite(Image.open(os.path.join(base, f)).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad + px + pad))
out = r"D:\AI\voidgen-mod\docs\ae_cells_v3.png"
img.save(out)
print("saved", out, img.size)