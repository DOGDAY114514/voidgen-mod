"""Compare storage concepts across tiers: canister vs crate (normal + filled)."""
from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\storage_compare.png"
OUTLINE = (8, 9, 12, 255)
FRAME = (64, 70, 82, 255)
FRAME_LIGHT = (104, 112, 126, 255)
FRAME_DARK = (30, 34, 42, 255)
GLASS = (16, 19, 26, 255)
GLASS_EDGE = (44, 52, 64, 255)
SCREW = (150, 160, 174, 255)
WHITE = (240, 255, 252, 255)

TIERS = {
    1: (168, 186, 206, 255),
    2: (246, 200, 66, 255),
    3: (92, 228, 244, 255),
    4: (78, 220, 132, 255),
    5: (224, 92, 255, 255),
}


def dim(c, k=0.75):
    return (int(c[0] * k), int(c[1] * k), int(c[2] * k), 255)


def canister(tier, filled):
    a = TIERS[tier]
    dk = dim(a, 0.6)
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # top cap
    d.rectangle([4, 0, 11, 3], fill=OUTLINE)
    d.rectangle([5, 1, 10, 2], fill=FRAME)
    d.line([5, 1, 10, 1], fill=FRAME_LIGHT)
    d.line([6, 2, 9, 2], fill=WHITE if filled else a)
    # body
    d.rectangle([2, 3, 13, 14], fill=OUTLINE)
    d.rectangle([3, 4, 12, 13], fill=GLASS)
    d.line([3, 4, 12, 4], fill=GLASS_EDGE)
    d.line([3, 13, 12, 13], fill=FRAME_DARK)
    if filled:
        d.rectangle([4, 5, 11, 12], fill=a)
        d.rectangle([6, 7, 9, 10], fill=WHITE)
        d.point((5, 6), fill=WHITE)
        d.point((10, 6), fill=WHITE)
        d.point((7, 11), fill=WHITE)
        d.point((5, 11), fill=dim(a, 0.85))
    else:
        # void gas above the liquid
        for x, y in ((5, 6), (6, 5), (9, 6), (10, 5), (6, 7), (9, 7)):
            d.point((x, y), fill=dk if (x + y) % 2 else a)
        d.point((8, 6), fill=WHITE)
        # liquid with a wavy surface
        d.rectangle([4, 9, 11, 12], fill=dim(a, 0.85))
        for x in (4, 6, 8, 10):
            d.line([x, 8, x + 1, 8], fill=a)
        d.line([4, 9, 11, 9], fill=a)
        d.line([4, 12, 11, 12], fill=dk)
        d.point((6, 10), fill=WHITE)
        d.point((9, 11), fill=dim(a, 1.15))
    # glass shine
    d.line([4, 5, 4, 12], fill=(160, 200, 215, 100))
    d.point((11, 5), fill=(210, 235, 245, 130))
    # base
    d.rectangle([3, 13, 12, 14], fill=OUTLINE)
    d.line([4, 13, 11, 13], fill=SCREW)
    return im


def crate(tier, filled):
    a = TIERS[tier]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 1, 14, 14], fill=OUTLINE)
    d.rectangle([2, 2, 13, 13], fill=FRAME)
    d.line([2, 2, 13, 2], fill=FRAME_LIGHT)
    d.line([2, 2, 2, 13], fill=FRAME_LIGHT)
    d.line([2, 13, 13, 13], fill=FRAME_DARK)
    d.line([13, 2, 13, 13], fill=FRAME_DARK)
    d.line([3, 3, 12, 3], fill=FRAME_DARK)
    # tiers as corner bolts
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)):
        d.point((x, y), fill=a)
    # core window
    d.rectangle([5, 5, 10, 10], fill=OUTLINE)
    d.rectangle([6, 6, 9, 9], fill=(18, 16, 26, 255))
    if filled:
        d.rectangle([6, 6, 9, 9], fill=a)
        d.rectangle([7, 7, 8, 8], fill=WHITE)
        for x, y in ((5, 5), (10, 5), (5, 10), (10, 10)):
            d.point((x, y), fill=WHITE)
    else:
        d.point((7, 7), fill=a)
        d.point((8, 8), fill=a)
        d.point((8, 7), fill=WHITE)
        d.point((7, 9), fill=dim(a))
    return im


def sheet():
    scale = 10
    cell = 16 * scale
    pad = 12
    rows = [("canister", canister), ("crate", crate)]
    img = Image.new("RGBA", (pad + 9 * (cell + pad), pad + 4 * (cell + pad)), (20, 22, 28, 255))
    y = pad
    for _, fn in rows:
        for filled in (False, True):
            for i in range(9):
                tier = 1 + (i % 5)
                if filled and tier == 5 and i >= 4:
                    # only 4 filled tiers exist; keep layout but skip draw
                    x = pad + i * (cell + pad)
                    continue
                tile = fn(tier, filled).resize((cell, cell), Image.NEAREST)
                img.alpha_composite(tile, (pad + i * (cell + pad), y))
            y += cell + pad
    img.save(OUT)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    sheet()
