"""Voidgen v3 texture pass: nicer collector/distributor blocks + canister-style storages.

Only rewrites the PNGs listed in OUT; models/blockstates are unchanged (cube_all /
item generated models already point at these file names).
"""
import os

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX_BLOCK = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "block")
TEX_ITEM = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")

# --- palette -----------------------------------------------------------------
OUTLINE = (8, 9, 12, 255)
FRAME = (46, 52, 62, 255)
FRAME_LIGHT = (78, 86, 99, 255)
FRAME_DARK = (24, 28, 34, 255)
PLATE = (32, 37, 45, 255)
PLATE_LIGHT = (42, 48, 58, 255)
PLATE_DARK = (18, 21, 27, 255)
INSET = (9, 11, 15, 255)
SCREW = (142, 152, 166, 255)
SCREW_DARK = (70, 78, 90, 255)
CYAN = (84, 232, 224, 255)
WHITE = (236, 255, 253, 255)

TIERS = {
    1: (168, 186, 206, 255),   # iron
    2: (246, 200, 66, 255),    # gold
    3: (92, 228, 244, 255),    # diamond
    4: (78, 220, 132, 255),    # emerald
    5: (224, 92, 255, 255),    # nether star
}


def img():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def bevel_frame(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=FRAME)
    d.line([x0, y0, x1, y0], fill=FRAME_LIGHT)
    d.line([x0, y0, x0, y1], fill=FRAME_LIGHT)
    d.line([x0, y1, x1, y1], fill=FRAME_DARK)
    d.line([x1, y0, x1, y1], fill=FRAME_DARK)


def screws(d):
    for x, y in ((1, 1), (14, 1), (1, 14), (14, 14)):
        d.point((x, y), fill=SCREW_DARK)
        d.point((x + 1, y + 1) if x < 8 and y < 8 else (x - 1, y - 1), fill=SCREW)


def base_plate(d, inset=3):
    d.rectangle([0, 0, 15, 15], fill=OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([inset, inset, 15 - inset, 15 - inset], fill=PLATE_DARK)
    d.line([inset, inset, 15 - inset, inset], fill=PLATE)
    d.line([inset, inset, inset, 15 - inset], fill=PLATE)
    screws(d)


def pip_row(d, y, tier):
    color = TIERS[tier]
    for i in range(tier):
        x = 3 + i * 2
        d.point((x, y), fill=color)
        d.point((x, y + 1), fill=OUTLINE)


def collector(tier):
    a = TIERS[tier]
    im = img()
    d = ImageDraw.Draw(im)
    base_plate(d)
    # intake ring + void hole
    d.rectangle([5, 5, 10, 10], outline=a)
    d.rectangle([6, 6, 9, 9], fill=INSET)
    d.rectangle([7, 7, 8, 8], fill=a)
    d.point((7, 7), fill=WHITE)
    # vent slits top/bottom
    for x in (4, 7, 10):
        d.point((x, 2), fill=OUTLINE)
        d.point((x + 1, 2), fill=a)
        d.point((x, 13), fill=OUTLINE)
        d.point((x + 1, 13), fill=a)
    # tier pips
    pip_row(d, 12, tier)
    return im


def distributor():
    im = img()
    d = ImageDraw.Draw(im)
    base_plate(d)
    # emitter core
    d.rectangle([6, 6, 9, 9], fill=INSET)
    d.rectangle([7, 7, 8, 8], fill=CYAN)
    d.point((7, 7), fill=WHITE)
    # four emitter arms
    d.line([7, 3, 7, 6], fill=CYAN)
    d.line([8, 9, 8, 12], fill=CYAN)
    d.line([3, 7, 6, 7], fill=CYAN)
    d.line([9, 8, 12, 8], fill=CYAN)
    d.point((3, 3), fill=(235, 120, 96, 255))
    d.point((12, 3), fill=(120, 235, 150, 255))
    d.point((3, 12), fill=(120, 235, 150, 255))
    d.point((12, 12), fill=(235, 120, 96, 255))
    # antenna tip on the top edge
    d.point((8, 2), fill=WHITE)
    return im


def canister(tier, filled=False):
    a = TIERS[tier]
    dk = tuple(int(c * 0.6) for c in a[:3]) + (255,)
    lo = tuple(int(c * 0.85) for c in a[:3]) + (255,)
    im = img()
    d = ImageDraw.Draw(im)
    # top cap
    d.rectangle([4, 0, 11, 3], fill=OUTLINE)
    d.rectangle([5, 1, 10, 2], fill=FRAME)
    d.line([5, 1, 10, 1], fill=FRAME_LIGHT)
    d.line([6, 2, 9, 2], fill=WHITE if filled else a)
    # glass body
    d.rectangle([2, 3, 13, 14], fill=OUTLINE)
    d.rectangle([3, 4, 12, 13], fill=(16, 19, 26, 255))
    d.line([3, 4, 12, 4], fill=(44, 52, 64, 255))
    d.line([3, 13, 12, 13], fill=FRAME_DARK)
    if filled:
        d.rectangle([4, 5, 11, 12], fill=a)
        d.rectangle([6, 7, 9, 10], fill=WHITE)
        d.point((5, 6), fill=WHITE)
        d.point((10, 6), fill=WHITE)
        d.point((7, 11), fill=WHITE)
        d.point((5, 11), fill=lo)
    else:
        # void gas above the liquid
        for x, y in ((5, 6), (6, 5), (9, 6), (10, 5), (6, 7), (9, 7)):
            d.point((x, y), fill=dk if (x + y) % 2 else a)
        d.point((8, 6), fill=WHITE)
        # wavy liquid surface + body
        d.rectangle([4, 9, 11, 12], fill=lo)
        for x in (4, 6, 8, 10):
            d.line([x, 8, x + 1, 8], fill=a)
        d.line([4, 9, 11, 9], fill=a)
        d.line([4, 12, 11, 12], fill=dk)
        d.point((6, 10), fill=WHITE)
        d.point((9, 11), fill=lo)
    # glass shine
    d.line([4, 5, 4, 12], fill=(160, 200, 215, 100))
    d.point((11, 5), fill=(210, 235, 245, 130))
    # base
    d.rectangle([3, 13, 12, 14], fill=OUTLINE)
    d.line([4, 13, 11, 13], fill=SCREW)
    return im


def mob_spawner():
    im = img()
    d = ImageDraw.Draw(im)
    d.rectangle([2, 3, 13, 13], fill=OUTLINE)
    d.rectangle([3, 4, 12, 12], fill=(26, 22, 36, 255))
    # cage bars
    for x in (4, 6, 8, 10, 12):
        d.line([x, 4, x, 12], fill=(96, 92, 118, 255))
    # glowing orb
    d.rectangle([6, 6, 9, 9], fill=(52, 30, 74, 255))
    d.point((7, 7), fill=(120, 255, 170, 255))
    d.point((8, 7), fill=(120, 255, 170, 255))
    d.point((7, 8), fill=(70, 170, 110, 255))
    d.point((8, 8), fill=(70, 170, 110, 255))
    # particles
    d.point((3, 2), fill=(200, 120, 255, 255))
    d.point((12, 2), fill=(120, 255, 200, 255))
    d.point((2, 8), fill=(200, 120, 255, 255))
    d.point((13, 9), fill=(120, 255, 200, 255))
    # top hook
    d.line([7, 0, 8, 0], fill=(120, 120, 140, 255))
    return im


def configurator():
    im = img()
    d = ImageDraw.Draw(im)
    # grip
    d.line([3, 13, 6, 9], fill=OUTLINE)
    d.line([4, 13, 7, 9], fill=FRAME_DARK)
    d.line([3, 12, 6, 8], fill=FRAME)
    # body
    d.rectangle([6, 6, 11, 10], fill=FRAME)
    d.rectangle([7, 7, 10, 9], fill=INSET)
    d.point((8, 8), fill=CYAN)
    d.point((9, 8), fill=WHITE)
    # antenna
    d.line([11, 6, 13, 3], fill=FRAME_LIGHT)
    d.point((13, 2), fill=(240, 90, 90, 255))
    d.point((12, 3), fill=(120, 255, 200, 255))
    # side buttons
    d.point((7, 10), fill=FRAME_LIGHT)
    d.point((9, 10), fill=(240, 160, 80, 255))
    return im


def save(im, folder, name):
    im.save(os.path.join(folder, name))
    print("wrote", name)


def main():
    for tier in range(1, 6):
        save(collector(tier), TEX_BLOCK, f"nothing_collector_{tier}.png")
    save(distributor(), TEX_BLOCK, "nothing_distributor.png")
    for tier, name in ((1, "iron"), (2, "gold"), (3, "diamond"), (4, "emerald"), (5, "nether")):
        save(canister(tier, False), TEX_ITEM, f"void_storage_{name}.png")
    for tier, name in ((1, "iron"), (2, "gold"), (3, "diamond"), (4, "emerald")):
        save(canister(tier, True), TEX_ITEM, f"filled_void_storage_{name}.png")
    save(mob_spawner(), TEX_ITEM, "mob_spawner.png")
    save(configurator(), TEX_ITEM, "void_configurator.png")


if __name__ == "__main__":
    main()
