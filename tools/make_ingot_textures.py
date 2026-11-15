import os
from PIL import Image

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
ref = r"D:\AI\voidgen-mod\docs\ingot_ref"
DEEP = (30, 18, 56)
MID = (98, 60, 170)
LIGHT = (170, 150, 238)
HIGH = (234, 230, 255)
CYAN = (110, 240, 255)
CYAN_D = (62, 168, 190)

def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def palette(lum):
    if lum < 90:
        return lerp(DEEP, MID, lum / 90.0)
    if lum < 190:
        return lerp(MID, LIGHT, (lum - 90) / 100.0)
    return lerp(LIGHT, HIGH, (lum - 190) / 65.0)

def recolor(img):
    px = img.load()
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    op = out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            c = palette(lum)
            op[x, y] = (c[0], c[1], c[2], a)
    return out

def put(img, x, y, color):
    px = img.load()
    if 0 <= x < img.width and 0 <= y < img.height and px[x, y][3] > 0:
        px[x, y] = (color[0], color[1], color[2], 255)

def make_ingot():
    base = Image.open(os.path.join(ref, "iron_ingot.png")).convert("RGBA")
    img = recolor(base)
    # void rune: glowing diagonal crack
    for i in range(0, 7):
        x = 4 + i
        y = 9 - round(i * 3 / 6)
        put(img, x, y, CYAN_D)
        put(img, x, y - 1, CYAN)
    # sparkles inside the metal body
    for (x, y) in ((5, 6), (10, 9), (8, 10), (11, 6)):
        put(img, x, y, CYAN)
    put(img, 4, 9, CYAN)
    return img

def make_block():
    base = Image.open(os.path.join(ref, "iron_block.png")).convert("RGBA")
    img = recolor(base)
    # inner inset frame + centre sigil + corner studs
    for i in range(3, 13):
        put(img, i, 3, CYAN_D)
        put(img, i, 12, CYAN_D)
        put(img, 3, i, CYAN_D)
        put(img, 12, i, CYAN_D)
    for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)):
        put(img, x, y, CYAN)
    for (x, y) in ((2, 2), (13, 2), (2, 13), (13, 13)):
        put(img, x, y, HIGH)
    return img

os.makedirs(os.path.join(root, "item"), exist_ok=True)
os.makedirs(os.path.join(root, "block"), exist_ok=True)
ingot = make_ingot()
block = make_block()
ingot.save(os.path.join(root, "item", "void_ingot.png"))
block.save(os.path.join(root, "block", "void_ingot_block.png"))
# preview at 12x
scale = 12
pad = 16
W = pad * 3 + 16 * scale * 2
H = pad * 2 + 16 * scale
prev = Image.new("RGBA", (W, H), (22, 24, 30, 255))
prev.alpha_composite(ingot.resize((16 * scale, 16 * scale), Image.NEAREST), (pad, pad))
prev.alpha_composite(block.resize((16 * scale, 16 * scale), Image.NEAREST), (pad * 2 + 16 * scale, pad))
prev.save(r"D:\AI\voidgen-mod\docs\ingot_block_preview.png")
print("saved textures + preview")