import os
from PIL import Image
src = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\void_assembler.png"
img = Image.open(src).convert("RGBA")
w, h = img.size
frames = h // 16
scale = 9
cell = 16 * scale
pad = 10
out = Image.new("RGBA", (pad + frames * (cell + pad), pad * 2 + cell), (24, 26, 32, 255))
for i in range(frames):
    fr = img.crop((0, i * 16, 16, (i + 1) * 16)).resize((cell, cell), Image.NEAREST)
    out.alpha_composite(fr, (pad + i * (cell + pad), pad))
path = r"D:\AI\voidgen-mod\docs\void_assembler_frames.png"
out.save(path)
print("saved", path, out.size, "frames", frames)