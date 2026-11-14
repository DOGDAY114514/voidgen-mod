import os
from PIL import Image, ImageDraw
ref = r"D:\AI\voidgen-mod\docs\ref_components"
tiers = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 14
cell = 16 * scale
pad = 12
label_h = 18
img = Image.new("RGBA", (pad + 10*(cell+pad), pad*2 + cell + label_h), (24, 25, 31, 255))
d = ImageDraw.Draw(img)
for i, t in enumerate(tiers):
    p = os.path.join(ref, "ref_component_%s.png" % t)
    tile = Image.open(p).convert("RGBA").resize((cell, cell), Image.NEAREST)
    x = pad + i*(cell+pad)
    img.alpha_composite(tile, (x, pad))
    d.text((x + cell//2 - 8, pad + cell + 3), t.upper(), fill=(200, 205, 215, 255))
out = r"D:\AI\voidgen-mod\docs\ref_components_row.png"
img.save(out)
print("saved", out, img.size)