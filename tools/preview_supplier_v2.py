import io
from PIL import Image
strip = Image.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\me_void_supplier.png").convert("RGBA")
scale = 10
cell = 16 * scale
img = Image.new("RGBA", (16 + 8*(cell+12), 16 + cell), (22, 24, 30, 255))
for i in range(8):
    img.alpha_composite(strip.crop((0, i*16, 16, i*16+16)).resize((cell, cell), Image.NEAREST), (16 + i*(cell+12), 16))
img.save(r"D:\AI\voidgen-mod\docs\supplier_frames_v2.png")
iv = Image.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item\void_value.png").convert("RGBA")
iv.resize((160,160), Image.NEAREST).save(r"D:\AI\voidgen-mod\docs\void_value_10x.png")
print("preview saved")