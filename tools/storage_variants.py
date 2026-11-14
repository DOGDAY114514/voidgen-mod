"""Storage texture variants: pick the best-looking canister design."""
import os

from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\storage_variants.png"
OUTLINE = (8, 9, 12, 255)
FRAME = (60, 66, 78, 255)
FRAME_LIGHT = (96, 104, 118, 255)
FRAME_DARK = (30, 34, 42, 255)
PLATE = (40, 45, 54, 255)
INSET = (9, 11, 15, 255)
WHITE = (240, 255, 252, 255)
SCREW = (140, 150, 164, 255)

TIER = (168, 186, 206, 255)


def blank():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def variant_cell(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    # shell
    d.rectangle([1, 1, 14, 15], fill=OUTLINE)
    d.rectangle([2, 2, 13, 14], fill=FRAME)
    d.line([2, 2, 13, 2], fill=FRAME_LIGHT)
    d.line([2, 2, 2, 14], fill=FRAME_LIGHT)
    d.line([2, 14, 13, 14], fill=FRAME_DARK)
    d.line([13, 2, 13, 14], fill=FRAME_DARK)
    # top lid slot
    d.rectangle([4, 3, 11, 4], fill=FRAME_DARK)
    d.line([4, 3, 11, 3], fill=SCREW)
    # side vents
    for y in (7, 9, 11):
        d.point((2, y), fill=OUTLINE)
        d.point((13, y), fill=OUTLINE)
    # window frame
    d.rectangle([3, 5, 12, 13], fill=INSET)
    d.line([4, 6, 11, 6], fill=PLATE)
    d.rectangle([4, 6, 11, 12], fill=(15, 17, 22, 255))
    if filled:
        for row, y in enumerate(range(7, 12)):
            k = 0.5 + row * 0.12
            col = tuple(min(255, int(c * k)) for c in TIER[:3]) + (255,)
            d.line([5, y, 10, y], fill=col)
        d.rectangle([6, 8, 9, 11], fill=WHITE)
        d.point((5, 7), fill=WHITE)
        d.point((10, 9), fill=WHITE)
        d.point((5, 11), fill=TIER)
        d.point((10, 12), fill=TIER)
    else:
        glow = (TIER[0] // 3, TIER[1] // 3, TIER[2] // 3, 255)
        d.rectangle([5, 10, 10, 11], fill=glow)
        for i, (x, y) in enumerate(((5, 9), (6, 8), (7, 8), (8, 7), (9, 8), (10, 9), (8, 10), (7, 10))):
            d.point((x, y), fill=TIER if i % 2 == 0 else (TIER[0] // 2, TIER[1] // 2, TIER[2] // 2, 255))
        d.point((8, 8), fill=WHITE)
    # bottom strip + led
    d.line([4, 13, 11, 13], fill=SCREW)
    d.point((12, 4), fill=TIER)
    # tier pips bottom-right
    d.point((5, 13), fill=FRAME_DARK)
    return im


def variant_tank(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    # cap
    d.rectangle([4, 1, 11, 4], fill=OUTLINE)
    d.rectangle([5, 1, 10, 3], fill=FRAME)
    d.line([5, 1, 10, 1], fill=FRAME_LIGHT)
    d.line([5, 2, 10, 2], fill=SCREW)
    # glass body with cut corners
    d.rectangle([3, 5, 12, 13], fill=OUTLINE)
    d.rectangle([4, 5, 11, 12], fill=(16, 18, 24, 255))
    d.point((4, 5), fill=(0, 0, 0, 0))
    # liquid
    top = 7 if filled else 9
    d.rectangle([5, top, 10, 12], fill=TIER)
    if filled:
        d.rectangle([6, top + 1, 9, 11], fill=WHITE)
        d.point((5, 6), fill=WHITE)
        d.point((10, 9), fill=WHITE)
        d.point((7, 5), fill=TIER)
    else:
        d.line([5, top, 10, top], fill=(min(255, TIER[0] + 30), min(255, TIER[1] + 30), TIER[2], 255))
        d.point((6, top + 1), fill=WHITE)
    # glass highlight
    d.line([4, 6, 4, 11], fill=(200, 230, 240, 90))
    # base
    d.rectangle([4, 13, 11, 14], fill=OUTLINE)
    d.line([4, 13, 11, 13], fill=SCREW)
    return im


def variant_shard(filled):
    im = blank()
    d = ImageDraw.Draw(im)
    # obsidian diamond shell
    pts = [(8, 1), (13, 6), (13, 11), (8, 15), (3, 11), (3, 6)]
    d.polygon(pts, fill=OUTLINE)
    inner = [(8, 2), (12, 6), (12, 10), (8, 14), (4, 10), (4, 6)]
    d.polygon(inner, fill=(24, 20, 34, 255))
    # core
    core = [(8, 5), (10, 7), (10, 10), (8, 12), (6, 10), (6, 7)]
    if filled:
        d.polygon(core, fill=TIER)
        d.polygon([(8, 6), (9, 8), (9, 10), (8, 11), (7, 10), (7, 8)], fill=WHITE)
        d.point((5, 8), fill=TIER)
        d.point((11, 9), fill=TIER)
    else:
        d.polygon(core, fill=(TIER[0] // 3, TIER[1] // 3, TIER[2] // 3, 255))
        d.point((8, 8), fill=TIER)
        d.point((7, 9), fill=TIER)
    # rune notches
    d.point((8, 1), fill=SCREW)
    d.point((8, 15), fill=SCREW)
    return im


VARIANTS = [("cell", variant_cell), ("tank", variant_tank), ("shard", variant_shard)]

if __name__ == "__main__":
    scale = 10
    cell = 16 * scale
    pad = 14
    img = Image.new("RGBA", (pad + 2 * (cell + pad), pad + len(VARIANTS) * 2 * (cell + pad)), (20, 22, 28, 255))
    for row, (name, fn) in enumerate(VARIANTS):
        for col, filled in enumerate((False, True)):
            tile = fn(filled).resize((cell, cell), Image.NEAREST)
            x = pad + col * (cell + pad)
            y = pad + (row * 2 + (1 if filled else 0)) * (cell + pad)
            img.alpha_composite(tile, (x, y))
    img.save(OUT)
    print("saved", OUT, img.size)
