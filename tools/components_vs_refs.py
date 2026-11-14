import os
from PIL import Image, ImageDraw
ROOT = r"D:\AI\voidgen-mod"
ref = os.path.join(ROOT, "docs", "ref_components")
ours = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")
tiers = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 12
cell = 16*scale
pad = 10
img = Image.new("RGBA", (pad + 10*(cell+pad), pad*3 + 2*cell + 22), (22, 23, 29, 255))
d = ImageDraw.Draw(img)
for i,t in enumerate(tiers):
    a = Image.open(os.path.join(ours, "void_component_%s.png" % t)).convert("RGBA").resize((cell,cell), Image.NEAREST)
    b = Image.open(os.path.join(ref, "ref_component_%s.png" % t)).convert("RGBA").resize((cell,cell), Image.NEAREST)
    x = pad + i*(cell+pad)
    img.alpha_composite(a, (x, pad))
    img.alpha_composite(b, (x, pad*2 + cell))
    d.text((x+4, pad*2 + 2*cell + 4), t.upper(), fill=(210,215,225,255))
d.text((pad, 2), "ours", fill=(150,220,255,255))
d.text((pad, pad + cell + 2), "ref", fill=(255,200,120,255))
out = os.path.join(ROOT, "docs", "components_vs_refs.png")
img.save(out)
print("saved", out, img.size)