from PIL import Image

face = Image.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\void_ingot_block.png").convert("RGBA")
W = 320; H = 360
cx, cy, w, h, hgt = 160, 40, 120, 60, 90
out = Image.new("RGBA", (W, H), (22, 24, 30, 255))
px = out.load(); fpx = face.load()

def sample(u, v, shade):
    x = min(15, max(0, int(u*16)))
    y = min(15, max(0, int(v*16)))
    r, g, b, a = fpx[x, y]
    return (int(r*shade), int(g*shade), int(b*shade), a)

for Y in range(H):
    for X in range(W):
        # top diamond
        s = (X - (cx - w)) / w
        t = (Y - (cy + h)) / h
        u = (s - t) / 2.0
        v = (s + t) / 2.0
        if 0 <= u <= 1 and 0 <= v <= 1:
            px[X, Y] = sample(u, v, 1.0)
            continue
        # left face
        u2 = (X - (cx - w)) / w
        t2 = (Y - (cy + h) - u2*h) / hgt
        if 0 <= u2 <= 1 and 0 <= t2 <= 1:
            px[X, Y] = sample(u2, t2, 0.70)
            continue
        # right face
        u3 = (X - cx) / w
        t3 = (Y - (cy + 2*h) + u3*h) / hgt
        if 0 <= u3 <= 1 and 0 <= t3 <= 1:
            px[X, Y] = sample(u3, t3, 0.50)
            continue

out.resize((640, 720), Image.NEAREST).save(r"D:\AI\voidgen-mod\docs\void_ingot_block_item.png")
face.resize((192,192), Image.NEAREST).save(r"D:\AI\voidgen-mod\docs\void_ingot_block_face.png")
print("saved")