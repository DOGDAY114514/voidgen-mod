import io
from PIL import Image
strip = Image.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\me_void_supplier.png").convert("RGBA")
scale = 9
cell = 16 * scale
pad = 8
img = Image.new("RGBA", (pad + 8*(cell+pad), pad*2 + cell + len([])), (24, 26, 32, 255))
for i in range(8):
    f = strip.crop((0, i*16, 16, i*16+16)).resize((cell, cell), Image.NEAREST)
    img.alpha_composite(f, (pad + i*(cell+pad), pad))
out = r"D:\AI\voidgen-mod\docs\supplier_frames.png"
img.save(out)
print("saved", img.size)