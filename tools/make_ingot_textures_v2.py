import os, math
from PIL import Image

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
ref = r"D:\AI\voidgen-mod\docs\ingot_ref"
DEEP, MID, LIGHT, HIGH = (30,18,56), (98,60,170), (170,150,238), (234,230,255)
CYAN, CYAN_D = (110,240,255), (62,168,190)

def lerp(a,b,t): return tuple(int(round(a[i]+(b[i]-a[i])*t)) for i in range(3))
def palette(lum):
    if lum < 90: return lerp(DEEP, MID, lum/90.0)
    if lum < 190: return lerp(MID, LIGHT, (lum-90)/100.0)
    return lerp(LIGHT, HIGH, (lum-190)/65.0)

def recolor(img):
    px = img.load(); out = Image.new("RGBA", img.size, (0,0,0,0)); op = out.load()
    for y in range(img.height):
        for x in range(img.width):
            r,g,b,a = px[x,y]
            if a == 0: continue
            c = palette(int(0.299*r+0.587*g+0.114*b)); op[x,y] = (c[0],c[1],c[2],a)
    return out

def put(img,x,y,c):
    px = img.load()
    if 0 <= x < 16 and 0 <= y < 16 and px[x,y][3] > 0: px[x,y] = (c[0],c[1],c[2],255)

def make_ingot():
    img = recolor(Image.open(os.path.join(ref,"iron_ingot.png")).convert("RGBA"))
    # thin void rune diagonal
    for i in range(0,7):
        x, y = 4+i, 9 - round(i*3/6)
        put(img, x, y, CYAN if i % 2 == 0 else CYAN_D)
    for (x,y) in ((5,6),(11,8),(8,10)): put(img,x,y,CYAN)
    return img

def make_block_icon():
    img = Image.new("RGBA",(16,16),(0,0,0,0))
    def rect(x0,y0,x1,y1,c):
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                if 0 <= x < 16 and 0 <= y < 16: img.putpixel((x,y),(c[0],c[1],c[2],255))
    # isometric-ish cube: top face diamond + two side faces
    TOP = (200,190,252); LEFT = (120,92,204); RIGHT = (82,56,150); OUT = (26,16,48)
    pts = [(7,1),(13,4),(7,7),(1,4)]
    # top face fill by scanlines between edges
    for y in range(1,8):
        lo, hi = 99, -1
        for i in range(len(pts)):
            x0,y0 = pts[i]; x1,y1 = pts[(i+1)%4]
            if (y0 <= y <= y1) or (y1 <= y <= y0):
                if y0 == y1: xs = [x0,x1]
                else:
                    t = (y-y0)/(y1-y0); xs = [x0+(x1-x0)*t]
                for x in xs:
                    x = int(round(x)); lo = min(lo,x); hi = max(hi,x)
        if lo <= hi:
            rect(lo, y, hi, y, TOP)
    # side faces
    for y in range(5,14):
        rect(1, y, 7, y, LEFT)
        rect(8, y, 13, y, RIGHT)
    # shade/outline top edge
    rect(1,4,13,4, OUT)
    for x in range(1,14,3): rect(x,1, x,3, OUT) if False else None
    # top face accents: cyan sigil + rivets
    rect(6,4,8,4, CYAN_D); rect(7,3,7,3, CYAN)
    rect(2,2,2,2, HIGH); rect(12,2,12,2, HIGH)
    # bottom outline
    rect(1,10,7,10, (40,26,70)); rect(8,10,13,10, (40,26,70))
    return img

os.remove(os.path.join(root, "block", "void_ingot_block.png")) if os.path.exists(os.path.join(root, "block", "void_ingot_block.png")) else None
ingot = make_ingot(); block = make_block_icon()
ingot.save(os.path.join(root, "item", "void_ingot.png"))
block.save(os.path.join(root, "item", "void_ingot_block.png"))
# preview
scale, pad = 12, 16
prev = Image.new("RGBA", (pad*3 + 16*scale*2, pad*2 + 16*scale), (22,24,30,255))
prev.alpha_composite(ingot.resize((16*scale,16*scale), Image.NEAREST), (pad,pad))
prev.alpha_composite(block.resize((16*scale,16*scale), Image.NEAREST), (pad*2+16*scale,pad))
prev.save(r"D:\AI\voidgen-mod\docs\ingot_block_preview.png")
print("done")