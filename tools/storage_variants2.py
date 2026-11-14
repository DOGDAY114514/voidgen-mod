"""Storage texture concepts round 2: battery / crate / gem."""
import os

from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\storage_variants2.png"
OUTLINE = (8, 9, 12, 255)
FRAME = (62, 68, 80, 255)
FRAME_LIGHT = (100, 108, 122, 255)
FRAME_DARK = (30, 34, 42, 255)
SCREW = (146, 156, 170, 255)
WHITE = (240, 255, 252, 255)
TIER = (168, 186, 206, 255)


def blank():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def battery(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    # terminal
    d.rectangle([6, 0, 9, 2], fill=OUTLINE)
    d.rectangle([7, 1, 8, 1], fill=SCREW)
    # top cap
    d.rectangle([3, 2, 12, 5], fill=OUTLINE)
    d.rectangle([4, 2, 11, 4], fill=FRAME)
    d.line([4, 2, 11, 2], fill=FRAME_LIGHT)
    d.line([4, 4, 11, 4], fill=FRAME_DARK)
    # body
    d.rectangle([3, 5, 12, 13], fill=OUTLINE)
    d.rectangle([4, 5, 11, 12], fill=FRAME_DARK)
    d.line([4, 5, 4, 12], fill=FRAME)
    d.line([11, 5, 11, 12], fill=FRAME_DARK)
    # window
    d.rectangle([5, 6, 10, 11], fill=(14, 16, 21, 255))
    if filled:
        d.rectangle([5, 6, 10, 11], fill=TIER)
        d.rectangle([6, 7, 9, 10], fill=WHITE)
        d.point((5, 6), fill=WHITE)
        d.point((10, 10), fill=WHITE)
    else:
        d.rectangle([6, 9, 9, 10], fill=(TIER[0] // 3, TIER[1] // 3, TIER[2] // 3, 255))
        for i, (x, y) in enumerate(((6, 8), (7, 7), (8, 7), (9, 8), (8, 9), (7, 10))):
            d.point((x, y), fill=TIER if i % 2 == 0 else (TIER[0] // 2, TIER[1] // 2, TIER[2] // 2, 255))
        d.point((8, 8), fill=WHITE)
    # bottom cap
    d.rectangle([3, 13, 12, 14], fill=OUTLINE)
    d.line([4, 13, 11, 13], fill=SCREW)
    return im


def crate(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    d.rectangle([1, 1, 14, 14], fill=OUTLINE)
    d.rectangle([2, 2, 13, 13], fill=FRAME)
    d.line([2, 2, 13, 2], fill=FRAME_LIGHT)
    d.line([2, 2, 2, 13], fill=FRAME_LIGHT)
    d.line([2, 13, 13, 13], fill=FRAME_DARK)
    d.line([13, 2, 13, 13], fill=FRAME_DARK)
    # metal bands
    for x in (3, 12):
        d.line([x, 3, x, 12], fill=FRAME_DARK)
    # center gem
    d.rectangle([5, 5, 10, 10], fill=OUTLINE)
    d.rectangle([6, 6, 9, 9], fill=(20, 17, 28, 255))
    if filled:
        d.rectangle([6, 6, 9, 9], fill=TIER)
        d.rectangle([7, 7, 8, 8], fill=WHITE)
        for x, y in ((5, 5), (10, 5), (5, 10), (10, 10)):
            d.point((x, y), fill=TIER)
    else:
        d.point((7, 7), fill=TIER)
        d.point((8, 8), fill=TIER)
        d.point((8, 7), fill=WHITE)
    # corners screws
    for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)):
        d.point((x, y), fill=SCREW)
    # lid slot
    d.line([4, 3, 11, 3], fill=FRAME_LIGHT)
    return im


def gem(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    shell = [(8, 0), (14, 5), (14, 11), (8, 15), (1, 11), (1, 5)]
    inner = [(8, 1), (13, 5), (13, 10), (8, 14), (2, 10), (2, 5)]
    core = [(8, 3), (12, 6), (12, 9), (8, 13), (3, 9), (3, 6)]
    d.polygon(shell, fill=OUTLINE)
    d.polygon(inner, fill=(30, 27, 42, 255))
    d.polygon(core, fill=(18, 16, 26, 255))
    if filled:
        d.polygon([(8, 4), (11, 7), (11, 9), (8, 12), (4, 9), (4, 7)], fill=TIER)
        d.polygon([(8, 6), (9, 7), (9, 9), (8, 10), (6, 9), (6, 7)], fill=WHITE)
        d.point((2, 7), fill=TIER)
        d.point((13, 8), fill=TIER)
    else:
        d.point((8, 6), fill=TIER)
        d.point((7, 8), fill=TIER)
        d.point((9, 9), fill=(TIER[0] // 2, TIER[1] // 2, TIER[2] // 2, 255))
        d.point((8, 10), fill=WHITE)
    d.point((8, 0), fill=SCREW)
    d.point((8, 15), fill=SCREW)
    return im


CONCEPTS = [("battery", battery), ("crate", crate), ("gem", gem)]

if __name__ == "__main__":
    scale = 10
    cell = 16 * scale
    pad = 14
    img = Image.new("RGBA", (pad + 2 * (cell + pad), pad + len(CONCEPTS) * (cell + pad)), (20, 22, 28, 255))
    for row, (name, fn) in enumerate(CONCEPTS):
        for col, filled in enumerate((False, True)):
            tile = fn(filled).resize((cell, cell), Image.NEAREST)
            x = pad + col * (cell + pad)
            y = pad + row * (cell + pad)
            img.alpha_composite(tile, (x, y))
    img.save(OUT)
    print("saved", OUT, img.size)
