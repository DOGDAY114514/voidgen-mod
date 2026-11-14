"""Void storage disks v2: closely mirror AE2's cell silhouette (white-ish beveled
plates + diagonal tier ribbon + corner LED), recolored to the void palette with
sparkles. Generates preview PNGs into docs/cells_v2 first."""
import os

from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\cells_v2"
os.makedirs(OUT, exist_ok=True)

PLATE_LIGHT = (246, 248, 252, 255)
PLATE = (228, 232, 240, 255)
PLATE_MID = (204, 210, 220, 255)
PLATE_DARK = (158, 164, 178, 255)
RIM = (58, 62, 72, 255)
RIM_DARK = (34, 37, 45, 255)
SLOT = (46, 49, 58, 255)
SLOT_DARK = (28, 30, 37, 255)
LED = (98, 255, 190, 255)
SPARK = (188, 250, 255, 255)

TIERS = {
    "1k": (64, 150, 255),
    "4k": (94, 200, 255),
    "16k": (86, 224, 206),
    "64k": (94, 226, 150),
    "256k": (150, 222, 96),
    "1m": (226, 196, 84),
    "4m": (242, 152, 72),
    "16m": (238, 108, 108),
    "64m": (188, 128, 255),
    "256m": (226, 232, 240),
}


def silhouette(d, fill):
    d.rectangle([4, 2, 11, 13], fill=fill)
    d.rectangle([2, 4, 13, 11], fill=fill)
    d.rectangle([3, 3, 12, 12], fill=fill)


def plate(d, base, light, dark):
    silhouette(d, (44, 47, 56, 255))
    # fill plate with 1px rim
    silhouette(d, base)
    d.rectangle([4, 2, 11, 2], fill=light)
    d.line([3, 3, 3, 12], fill=light)
    d.line([2, 4, 2, 11], fill=light)
    d.line([4, 3, 11, 3], fill=light)
    d.line([4, 12, 11, 12], fill=dark)
    d.line([12, 4, 12, 11], fill=dark)
    d.line([13, 4, 13, 11], fill=dark)
    d.line([4, 13, 11, 13], fill=dark)


def ribbon(d, color):
    top = tuple(min(255, c + 60) for c in color[:3]) + (255,)
    deep = tuple(max(0, c - 75) for c in color[:3]) + (255,)
    # main band top-right -> bottom-left
    for i in range(6):
        x = 10 - i
        y = 4 + i
        d.point((x, y), fill=color)
        d.point((x + 1, y), fill=top)
        d.point((x + 1, y + 1), fill=top)
        d.point((x, y + 1), fill=deep)
    # short parallel band bottom-right
    for i in range(3):
        x = 10 - i
        y = 8 + i
        d.point((x, y), fill=deep)
        d.point((x, y + 1), fill=color)


def led(d, color=LED):
    d.point((11, 11), fill=(40, 44, 52, 255))
    d.point((11, 12), fill=color)


def sparkle(d):
    for (x, y) in [(1, 2), (14, 10), (2, 13), (12, 1), (8, 0), (15, 6)]:
        d.point((x, y), fill=SPARK)


def cell(tier):
    color = TIERS[tier]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    plate(d, PLATE, PLATE_LIGHT, PLATE_DARK)
    d.rectangle([4, 4, 11, 11], fill=PLATE_MID)
    d.line([4, 4, 11, 4], fill=PLATE)
    d.line([4, 4, 4, 11], fill=PLATE)
    ribbon(d, color)
    led(d)
    sparkle(d)
    return img


def housing():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    plate(d, PLATE, PLATE_LIGHT, PLATE_DARK)
    d.rectangle([4, 4, 11, 11], fill=PLATE_MID)
    for i in range(5):
        d.point((9 - i, 5 + i), fill=SLOT)
        d.point((10 - i, 5 + i), fill=SLOT_DARK)
        d.point((9 - i, 6 + i), fill=SLOT_DARK)
    d.rectangle([4, 8, 6, 9], fill=SLOT_DARK)
    d.point((11, 11), fill=SLOT_DARK)
    d.point((11, 12), fill=PLATE_DARK)
    sparkle(d)
    return img


def component():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([3, 3, 12, 12], fill=RIM)
    d.rectangle([2, 4, 13, 11], fill=RIM)
    d.rectangle([4, 2, 11, 13], fill=RIM)
    d.rectangle([4, 4, 11, 11], fill=PLATE)
    d.line([4, 4, 11, 4], fill=PLATE_LIGHT)
    d.line([4, 4, 4, 11], fill=PLATE_LIGHT)
    d.line([4, 11, 11, 11], fill=PLATE_DARK)
    d.line([11, 4, 11, 11], fill=PLATE_DARK)
    d.rectangle([5, 5, 10, 10], fill=(40, 52, 68, 255))
    for (x, y) in [(6, 6), (9, 6), (6, 9), (9, 9)]:
        d.point((x, y), fill=(120, 226, 255, 255))
    d.point((7, 8), fill=(200, 250, 255, 255))
    d.point((8, 7), fill=(200, 250, 255, 255))
    sparkle(d)
    return img


def ingot():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(2, 10), (4, 6), (12, 6), (14, 10), (12, 12), (4, 12)], fill=RIM)
    d.polygon([(3, 9), (5, 7), (11, 7), (13, 9), (11, 11), (5, 11)], fill=(74, 78, 92, 255))
    d.line([5, 7, 11, 7], fill=(150, 158, 176, 255))
    d.line([3, 9, 5, 7], fill=(120, 126, 142, 255))
    d.rectangle([6, 8, 10, 9], fill=(156, 116, 238, 255))
    d.point((7, 8), fill=(214, 186, 255, 255))
    sparkle(d)
    return img


def main():
    for tier in TIERS:
        cell(tier).save(os.path.join(OUT, f"void_cell_{tier}.png"))
    housing().save(os.path.join(OUT, "void_cell_housing.png"))
    component().save(os.path.join(OUT, "void_component.png"))
    ingot().save(os.path.join(OUT, "void_ingot.png"))
    print("wrote", len(os.listdir(OUT)), "previews to", OUT)


if __name__ == "__main__":
    main()
