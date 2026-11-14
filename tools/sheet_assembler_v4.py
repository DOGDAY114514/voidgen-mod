import os
from PIL import Image
src = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\void_assembler.png"
img = Image.open(src).convert("RGBA")
frames = img.size[1] // 16
pick = list(range(0, frames, 4))
scale = 9
cell = 16 * scale
pad = 10
out = Image.new("RGBA", (pad + len(pick) * (cell + pad), pad * 2 + cell), (24, 26, 32, 255))
for i, f in enumerate(pick):
    fr = img.crop((0, f * 16, 16, (f + 1) * 16)).resize((cell, cell), Image.NEAREST)
    out.alpha_composite(fr, (pad + i * (cell + pad), pad))
path = r"D:\AI\voidgen-mod\docs\void_assembler_frames.png"
out.save(path)
print("saved", path, out.size, "frames", frames)