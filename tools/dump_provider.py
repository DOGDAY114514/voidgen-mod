import os
from PIL import Image
p = r"D:\AI\voidgen-mod\docs\assembler_ref\pattern_provider_block.png"
img = Image.open(p).convert("RGBA")
print("size", img.size)
px = img.load()
for y in range(img.size[1]):
    row = ""
    for x in range(img.size[0]):
        r, g, b, a = px[x, y]
        import colorsys
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        if a == 0:
            c = "."
        elif s < 0.10 and v < 0.20:
            c = "#"
        elif s < 0.12 and v > 0.80:
            c = "W"
        elif s < 0.12:
            c = "+"
        elif s < 0.35:
            c = "o"
        else:
            c = "A"
        row += c
    print(f"{y:2d} {row}")