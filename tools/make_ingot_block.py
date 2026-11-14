import os
from PIL import Image
outdir = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
from PIL import ImageDraw
d = ImageDraw.Draw(img)
d.rectangle([2, 3, 13, 12], fill=(46, 40, 66, 255))
d.rectangle([3, 4, 12, 11], fill=(74, 66, 102, 255))
d.line([3, 4, 12, 4], fill=(120, 108, 160, 255))
d.line([3, 5, 3, 11], fill=(112, 100, 150, 255))
d.line([3, 11, 12, 11], fill=(34, 30, 50, 255))
d.line([12, 5, 12, 11], fill=(38, 33, 54, 255))
for y in (6, 8, 10):
    d.line([5, y, 10, y], fill=(150, 110, 230, 255))
    d.point((5, y), fill=(200, 170, 255, 255))
d.rectangle([5, 5, 10, 5], fill=(96, 84, 136, 255))
img.save(os.path.join(outdir, "void_ingot_block.png"))
print("ingot block texture written")