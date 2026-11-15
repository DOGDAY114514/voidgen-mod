import os
from PIL import Image
p = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item\void_ingot_block.png"
img = Image.open(p).convert("RGBA"); px = img.load()
CYAN = (110,240,255,255); CYAN_D = (62,168,190,255)
for (x,y) in ((3,7),(4,8),(5,9)):
    if px[x,y][3] > 0: px[x,y] = CYAN_D if (x+y)%2 else CYAN
for (x,y) in ((11,7),(10,8)):
    if px[x,y][3] > 0: px[x,y] = CYAN_D
img.save(p)
print("accented")