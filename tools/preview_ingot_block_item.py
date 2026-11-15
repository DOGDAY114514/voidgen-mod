import io
from PIL import Image

face = Image.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\block\void_ingot_block.png").convert("RGBA")
T = face.resize((256, 256), Image.NEAREST)

def shade(img, f):
    px = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = px[x, y]
            px[x, y] = (int(r*f), int(g*f), int(b*f), a)
    return img

top = shade(T.copy(), 1.0)
left = shade(T.copy(), 0.72)
right = shade(T.copy(), 0.52)

cx, cy = 256, 180
w, h, v = 160, 80, 110
canvas = Image.new("RGBA", (512, 512), (22, 24, 30, 255))

# top: (0,0)->L, (256,0)->T, (256,256)->R, (0,256)->B
Lx, Ly = cx - w, cy + h
# affine: X = x*(w/256) + y*(w/256) + Lx ; Y = x*(-h/256) + y*(h/256) + Ly
a, b, c = w/256, w/256, Lx
d, e, f = -h/256, h/256, Ly
canvas.alpha_composite(top.transform((512, 512), Image.AFFINE, (a, b, c, d, e, f), resample=Image.NEAREST))

# left face: (0,0)->L, (256,0)->B, down v
Bx, By = cx, cy + 2*h
a2, b2, c2 = w/256, 0, Lx
d2, e2, f2 = h/256, v/256, Ly
canvas.alpha_composite(left.transform((512, 512), Image.AFFINE, (a2, b2, c2, d2, e2, f2), resample=Image.NEAREST))

# right face: (0,0)->B, (256,0)->R
Rx, Ry = cx + w, cy + h
a3, b3, c3 = w/256, 0, Bx
d3, e3, f3 = -h/256, v/256, By
canvas.alpha_composite(right.transform((512, 512), Image.AFFINE, (a3, b3, c3, d3, e3, f3), resample=Image.NEAREST))

canvas.save(r"D:\AI\voidgen-mod\docs\void_ingot_block_item.png")
face.resize((160,160), Image.NEAREST).save(r"D:\AI\voidgen-mod\docs\void_ingot_block_face.png")
print("saved previews")