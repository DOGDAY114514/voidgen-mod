import os
from PIL import Image
src = r"D:\AI\voidgen-mod\docs\cells_v3\void_cell_1k.png"
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item\item_storage_cell_1k.png"
scale = 20
px = 16 * scale
img = Image.new("RGBA", (2 * px + 36, px + 24), (26, 28, 34, 255))
img.alpha_composite(Image.open(src).convert("RGBA").resize((px, px), Image.NEAREST), (12, 12))
img.alpha_composite(Image.open(ref).convert("RGBA").resize((px, px), Image.NEAREST), (px + 24, 12))
out = r"D:\AI\voidgen-mod\docs\cell_1k_vs_ae2.png"
img.save(out)
print("saved", out, img.size)