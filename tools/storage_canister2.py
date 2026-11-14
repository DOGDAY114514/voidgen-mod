"""Storage canister v2: detailed glass canister with tier liquid + void gas."""
from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\storage_canister2.png"
OUTLINE = (8, 9, 12, 255)
FRAME = (64, 70, 82, 255)
FRAME_LIGHT = (104, 112, 126, 255)
FRAME_DARK = (30, 34, 42, 255)
GLASS = (16, 19, 26, 255)
GLASS_EDGE = (44, 52, 64, 255)
SCREW = (150, 160, 174, 255)
WHITE = (240, 255, 252, 255)
TIER = (168, 186, 206, 255)


def canister(filled):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tier_dim = (TIER[0] * 2 // 3, TIER[1] * 2 // 3, TIER[2] * 2 // 3, 255)

    # top cap
    d.rectangle([4, 0, 11, 3], fill=OUTLINE)
    d.rectangle([5, 1, 10, 2], fill=FRAME)
    d.line([5, 1, 10, 1], fill=FRAME_LIGHT)
    d.line([5, 2, 10, 2], fill=TIER if filled else tier_dim)

    # glass body with clipped corners
    d.rectangle([2, 3, 13, 15], fill=OUTLINE)
    d.rectangle([3, 4, 12, 14], fill=GLASS)
    d.point((3, 4), fill=(0, 0, 0, 0))
    d.point((12, 4), fill=(0, 0, 0, 0))
    d.line([3, 4, 12, 4], fill=GLASS_EDGE)
    d.line([3, 14, 12, 14], fill=FRAME_DARK)

    # liquid
    surface = 5 if filled else 8
    liquid = TIER if filled else (TIER[0] * 3 // 4, TIER[1] * 3 // 4, TIER[2] * 3 // 4, 255)
    d.rectangle([4, surface, 11, 13], fill=liquid)
    d.line([4, surface, 11, surface], fill=WHITE if filled else tier_dim)

    # void gas swirl above the liquid (normal) / bright core (filled)
    if filled:
        d.rectangle([6, 6, 9, 11], fill=WHITE)
        d.point((5, 5), fill=WHITE)
        d.point((10, 9), fill=WHITE)
        d.point((5, 11), fill=WHITE)
    else:
        for x, y in ((5, 6), (6, 6), (9, 7), (10, 7), (6, 5)):
            d.point((x, y), fill=TIER)
        d.point((8, 6), fill=WHITE)

    # glass shine + edge
    d.line([4, 4, 4, 13], fill=(150, 190, 205, 90))
    d.line([5, 4, 5, 12], fill=(120, 160, 175, 45))
    d.point((11, 5), fill=(200, 230, 240, 120))
    d.line([3, 5, 3, 13], fill=GLASS_EDGE)

    # base
    d.rectangle([3, 14, 12, 15], fill=OUTLINE)
    d.line([4, 14, 11, 14], fill=SCREW)
    return im


if __name__ == "__main__":
    scale = 12
    cell = 16 * scale
    pad = 14
    img = Image.new("RGBA", (pad + 2 * (cell + pad), pad + cell + pad), (20, 22, 28, 255))
    for col, filled in enumerate((False, True)):
        img.alpha_composite(canister(filled).resize((cell, cell), Image.NEAREST), (pad + col * (cell + pad), pad))
    img.save(OUT)
    print("saved", OUT, img.size)
