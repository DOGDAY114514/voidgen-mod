import os
from PIL import Image
root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
DEEP, TOP, LEFT, RIGHT, HIGH, CYAN = (26,16,48), (204,194,252), (120,92,204), (82,56,150), (240,238,255), (110,240,255)
img = Image.new("RGBA", (16,16), (0,0,0,0)); px = img.load()
def fill(x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(max(0,x0),min(15,x1)+1):
            if 0 <= y < 16: px[x,y] = (c[0],c[1],c[2],255)
# top diamond
for y in range(1,8):
    half = int(round(6*(1 - abs(y-4)/3)))
    if half >= 0: fill(7-half, y, 7+half, y, TOP)
# left face: rows 5..10 full, 11..13 diagonal leg
for y in range(5,11): fill(1, y, 7, y, LEFT)
for y in range(11,14):
    lx = 1 + (y-10)*2
    fill(lx, y, 7, y, LEFT)
# right face
for y in range(5,11): fill(8, y, 13, y, RIGHT)
for y in range(11,14):
    rx = 13 - (y-10)*2
    fill(7, y, rx, y, RIGHT)
# outlines
for y in range(1,8):
    half = int(round(6*(1 - abs(y-4)/3)))
    px[7-half,y] = (*DEEP,255); px[7+half,y] = (*DEEP,255)
fill(7,7,7,13,DEEP)
for y in range(11,14):
    px[1+(y-10)*2,y] = (*DEEP,255); px[13-(y-10)*2,y] = (*DEEP,255)
# sigil + rivets + bevel
for (x,y) in ((6,4),(7,3),(8,4),(7,5)): px[x,y] = (*CYAN,255)
for (x,y) in ((2,4),(12,4)): px[x,y] = (*HIGH,255)
for x in range(2,6): px[x,5] = (*HIGH,255)
for x in range(9,12): px[x,5] = (*HIGH,255)
img.save(os.path.join(root,"item","void_ingot_block.png"))
ingot = Image.open(os.path.join(root,"item","void_ingot.png")).convert("RGBA")
scale, pad = 12, 16
prev = Image.new("RGBA", (pad*3 + 16*scale*2, pad*2 + 16*scale), (22,24,30,255))
prev.alpha_composite(ingot.resize((16*scale,16*scale), Image.NEAREST), (pad,pad))
prev.alpha_composite(img.resize((16*scale,16*scale), Image.NEAREST), (pad*2+16*scale,pad))
prev.save(r"D:\AI\voidgen-mod\docs\ingot_block_preview.png")
print("saved")