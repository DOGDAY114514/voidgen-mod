import os
from PIL import Image
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
tiers = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
# frame-by-frame preview of 1k cell + 16k component
scale = 6
rows = []
for name in ["void_cell_1k", "void_component_16k"]:
    p = os.path.join(base, name + ".png")
    img = Image.open(p).convert("RGBA")
    w, h = img.size
    frames = h // 16
    row = Image.new("RGBA", (frames*(16*scale + 8), 16*scale), (24,25,31,255))
    for i in range(frames):
        frame = img.crop((0, i*16, 16, (i+1)*16)).resize((16*scale, 16*scale), Image.NEAREST)
        row.alpha_composite(frame, (i*(16*scale + 8), 0))
    rows.append((name, row))
maxw = max(r.width for _, r in rows)
out = Image.new("RGBA", (maxw, sum(r.height for _, r in rows) + 20*(len(rows)-1)), (24,25,31,255))
y = 0
for name, row in rows:
    out.alpha_composite(row, (0, y))
    y += row.height + 20
out.save(r"D:\AI\voidgen-mod\docs\animated_frames.png")
print("saved docs/animated_frames.png", out.size)
for t in ["void_cell_1k","void_component_16k"]:
    p = os.path.join(base, t + ".png")
    im = Image.open(p)
    print(t, im.size, "mcmeta:", os.path.exists(p + ".mcmeta"))