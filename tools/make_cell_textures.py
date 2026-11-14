"""Draw the void-ingot / component / housing / 1K..256M void disk item textures (16x16 RGBA)."""
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")

OUTLINE = (8, 9, 12, 255)
FRAME = (62, 68, 80, 255)
FRAME_LIGHT = (104, 112, 126, 255)
FRAME_DARK = (30, 34, 42, 255)
INSET = (14, 16, 21, 255)
SCREW = (150, 160, 174, 255)
WHITE = (240, 255, 252, 255)

TIERS = [
    (168, 186, 206), (246, 200, 66), (92, 228, 244), (78, 220, 132), (224, 92, 255),
    (255, 158, 66), (255, 90, 90), (124, 156, 255), (47, 255, 203), (250, 250, 255),
]


def img():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def shell(d, band_rgba, band_diagonal=True):
    d.rectangle([1, 1, 14, 14], fill=OUTLINE)
    d.rectangle([2, 2, 13, 13], fill=FRAME)
    d.line([2, 2, 13, 2], fill=FRAME_LIGHT)
    d.line([2, 2, 2, 13], fill=FRAME_LIGHT)
    d.line([2, 13, 13, 13], fill=FRAME_DARK)
    d.line([13, 2, 13, 13], fill=FRAME_DARK)
    # top handle notch
    d.rectangle([5, 0, 10, 1], fill=OUTLINE)
    d.rectangle([6, 1, 9, 1], fill=FRAME_DARK)
    if band_diagonal:
        for i in range(9):
            x, y = 3 + i, 11 - i
            d.point((x, y), fill=band_rgba)
            d.point((x + 1, y), fill=band_rgba)
            d.point((x, y + 1), fill=band_rgba)


def disk(index):
    im = img()
    d = ImageDraw.Draw(im)
    a = TIERS[index]
    shell(d, a + (255,))
    # dark port with capacity dots
    d.rectangle([3, 7, 8, 12], fill=INSET)
    d.line([3, 7, 8, 7], fill=FRAME_DARK)
    for row in range(2):
        for col in range(3):
            x = 4 + col * 2
            y = 9 + row * 2
            d.point((x, y), fill=a + (255,) if (index // 3) >= row + col else (a[0] // 2, a[1] // 2, a[2] // 2, 255))
    # sparkle effects around the cell
    d.point((12, 5), fill=WHITE)
    d.point((13, 7), fill=a + (200,))
    d.point((10, 3), fill=WHITE)
    d.point((2, 6), fill=WHITE)
    # screws
    d.point((2, 2), fill=SCREW)
    d.point((13, 13), fill=SCREW)
    return im


def housing():
    im = img()
    d = ImageDraw.Draw(im)
    shell(d, (110, 118, 132, 255))
    d.rectangle([3, 6, 12, 11], fill=INSET)
    d.line([3, 6, 12, 6], fill=FRAME_DARK)
    d.line([3, 11, 12, 11], fill=FRAME_LIGHT)
    # connector pins at the bottom
    for x in (4, 6, 8, 10, 12):
        d.point((x, 12), fill=SCREW)
    d.point((2, 2), fill=SCREW)
    d.point((13, 2), fill=SCREW)
    return im


def component():
    im = img()
    d = ImageDraw.Draw(im)
    d.rectangle([2, 2, 13, 13], fill=OUTLINE)
    d.rectangle([3, 3, 12, 12], fill=(22, 40, 38, 255))
    d.line([3, 3, 12, 3], fill=(52, 120, 110, 255))
    # traces
    d.line([4, 10, 7, 10], fill=(60, 214, 194, 255))
    d.line([7, 10, 7, 8], fill=(60, 214, 194, 255))
    d.line([9, 4, 9, 7], fill=(60, 214, 194, 255))
    d.line([9, 7, 11, 7], fill=(60, 214, 194, 255))
    # chip
    d.rectangle([5, 5, 8, 7], fill=(14, 20, 24, 255))
    d.rectangle([5, 5, 8, 5], fill=(40, 52, 60, 255))
    d.point((6, 6), fill=(120, 255, 230, 255))
    # gold pins
    for y in (4, 6, 8, 10):
        d.point((1, y), fill=(226, 186, 92, 255))
        d.point((14, y), fill=(226, 186, 92, 255))
    d.point((11, 11), fill=(120, 255, 230, 255))
    return im


def ingot():
    im = img()
    d = ImageDraw.Draw(im)
    # isometric ingot: dark void metal with cyan sheen
    d.polygon([(3, 9), (7, 5), (12, 6), (12, 10), (8, 13), (3, 12)], fill=OUTLINE)
    d.polygon([(4, 9), (7, 6), (11, 7), (11, 9), (8, 12), (4, 11)], fill=(46, 40, 66, 255))
    d.polygon([(4, 9), (7, 6), (11, 7), (8, 9), (5, 10)], fill=(86, 72, 128, 255))
    d.line([5, 10, 10, 9], fill=(38, 32, 56, 255))
    d.point((6, 8), fill=(160, 250, 255, 255))
    d.point((9, 8), fill=(120, 230, 255, 255))
    d.point((7, 12), fill=(90, 200, 240, 255))
    d.point((2, 5), fill=WHITE)
    d.point((13, 4), fill=(120, 230, 255, 220))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    ingot().save(os.path.join(OUT, "void_ingot.png"))
    component().save(os.path.join(OUT, "void_component.png"))
    housing().save(os.path.join(OUT, "void_cell_housing.png"))
    names = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
    for i, name in enumerate(names):
        disk(i).save(os.path.join(OUT, "void_cell_%s.png" % name))
    print("textures written to", OUT)


if __name__ == "__main__":
    main()
