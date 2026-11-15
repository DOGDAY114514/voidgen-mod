import os
from PIL import Image

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
DEEP, TOP, LEFT, RIGHT, HIGH, CYAN = (26,16,48), (204,194,252), (120,92,204), (82,56,150), (240,238,255), (110,240,255)

img = Image.new("RGBA", (16,16), (0,0,0,0))
px = img.load()
def fill(x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if 0 <= x < 16 and 0 <= y < 16: px[x,y] = (c[0],c[1],c[2],255)

# top diamond
for y in range(1,8):
    half = 6*(1 - abs(y-4)/3)
    if half < 0: continue
    fill(7-int(half), y, 7+int(half), y, TOP)
# left/right faces
for y in range(5,11):
    fill(1, y, 7, y, LEFT)
    fill(8, y, 13, y, RIGHT)
for i, y in enumerate(range(11,14)):
    fill(1, y, 7-(i+1), y, LEFT)
    fill(8+(i+1), y, 13, y, RIGHT)
# outline: diamond border, centre spine, bottom edges
for y in range(1,8):
    half = 6*(1 - abs(y-4)/3)
    if half < 0: continue
    x0, x1 = 7-int(half), 7+int(half)
    px[x0,y] = (*DEEP,255); px[x1,y] = (*DEEP,255)
fill(7, 7, 7, 13, DEEP)
for i, y in enumerate(range(11,14)):
    px[1,y] = (*DEEP,255); px[7-(i+1),y] = (*DEEP,255)
    px[8+(i+1),y] = (*DEEP,255); px[13,y] = (*DEEP,255)
# accents: void sigil on top + rivets on top edges
for (x,y) in ((6,4),(7,3),(8,4),(7,5)): px[x,y] = (*CYAN,255)
for (x,y) in ((2,4),(12,4)): px[x,y] = (*HIGH,255)
# bevel highlight on top edge of side faces
for x in range(2,7): px[x,5] = (*HIGH,255)
for x in range(9,13): px[x,5] = (*HIGH,255)

img.save(os.path.join(root,"item","void_ingot_block.png"))
# preview combined
ingot = Image.open(os.path.join(root,"item","void_ingot.png")).convert("RGBA")
scale, pad = 12, 16
prev = Image.new("RGBA", (pad*3 + 16*scale*2, pad*2 + 16*scale), (22,24,30,255))
prev.alpha_composite(ingot.resize((16*scale,16*scale), Image.NEAREST), (pad,pad))
prev.alpha_composite(img.resize((16*scale,16*scale), Image.NEAREST), (pad*2+16*scale,pad))
prev.save(r"D:\AI\voidgen-mod\docs\ingot_block_preview.png")
print("saved")