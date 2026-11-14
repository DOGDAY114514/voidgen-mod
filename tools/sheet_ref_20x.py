import os
from PIL import Image, ImageDraw
ref = r"D:\AI\voidgen-mod\docs\ref_components"
tiers = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 20
cell = 16 * scale
pad = 14
img = Image.new("RGBA", (pad + 10*(cell+pad), pad*2 + cell + 20), (20, 21, 26, 255))
d = ImageDraw.Draw(img)
for i, t in enumerate(tiers):
    tile = Image.open(os.path.join(ref, "ref_component_%s.png" % t)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    x = pad + i*(cell+pad)
    img.alpha_composite(tile, (x, pad))
    d.text((x + cell//2 - 10, pad + cell + 4), t.upper(), fill=(205, 210, 220, 255))
out = r"D:\AI\voidgen-mod\docs\ref_components_20x.png"
img.save(out)
print("saved", out)