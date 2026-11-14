from PIL import Image
import os
p = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item\item_storage_cell_1k.png"
img = Image.open(p).convert("RGBA")
px = img.load()
for y in range(16):
    row = []
    for x in range(16):
        r,g,b,a = px[x,y]
        row.append("%02x%02x%02x" % (r,g,b) if a else "......")
    print(" ".join(row))
print("--- saturation mask ---")
for y in range(16):
    row = []
    for x in range(16):
        r,g,b,a = px[x,y]
        if a == 0:
            row.append("  . ")
        else:
            mx,mn = max(r,g,b), min(r,g,b)
            sat = mx-mn
            row.append("%3d" % sat)
    print(" ".join(row))