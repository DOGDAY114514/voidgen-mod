"""Storage cell concept: AE-style storage cell with tier label band."""
from PIL import Image, ImageDraw

OUT = r"D:\AI\voidgen-mod\docs\storage_cell_ae.png"
OUTLINE = (8, 9, 12, 255)
FRAME = (66, 72, 84, 255)
FRAME_LIGHT = (104, 112, 126, 255)
FRAME_DARK = (30, 34, 42, 255)
INSET = (14, 16, 21, 255)
SCREW = (150, 160, 174, 255)
WHITE = (240, 255, 252, 255)
TIER = (168, 186, 206, 255)


def cell(filled):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # handle
    d.rectangle([5, 0, 10, 2], fill=OUTLINE)
    d.rectangle([6, 1, 9, 1], fill=FRAME_DARK)
    # shell
    d.rectangle([0, 2, 15, 14], fill=OUTLINE)
    d.rectangle([1, 3, 14, 13], fill=FRAME)
    d.line([1, 3, 14, 3], fill=FRAME_LIGHT)
    d.line([1, 3, 1, 13], fill=FRAME_LIGHT)
    d.line([1, 13, 14, 13], fill=FRAME_DARK)
    d.line([14, 3, 14, 13], fill=FRAME_DARK)
    # tier label band
    d.rectangle([2, 4, 13, 6], fill=TIER if filled else (TIER[0] * 3 // 4, TIER[1] * 3 // 4, TIER[2] * 3 // 4, 255))
    d.line([2, 4, 13, 4], fill=WHITE if filled else (TIER[0], TIER[1], TIER[2], 255))
    if filled:
        d.line([2, 6, 13, 6], fill=WHITE)
        d.point((4, 5), fill=FRAME_DARK)
        d.point((7, 5), fill=FRAME_DARK)
        d.point((10, 5), fill=FRAME_DARK)
    else:
        for x in (4, 7, 10):
            d.point((x, 5), fill=FRAME_DARK)
    # led grid (2 rows x 4 cols)
    for row in range(2):
        for col in range(4):
            x = 3 + col * 3
            y = 8 + row * 2
            colr = TIER if filled else (TIER[0] // 2, TIER[1] // 2, TIER[2] // 2, 255)
            d.rectangle([x, y, x + 1, y], fill=colr)
    if filled:
        d.point((7, 9), fill=WHITE)
        d.point((10, 9), fill=WHITE)
    # bottom trim + screws
    d.line([2, 12, 13, 12], fill=FRAME_DARK)
    d.point((2, 12), fill=SCREW)
    d.point((13, 12), fill=SCREW)
    return im


if __name__ == "__main__":
    scale = 10
    cell_px = 16 * scale
    pad = 14
    img = Image.new("RGBA", (pad + 2 * (cell_px + pad), pad + cell_px + pad), (20, 22, 28, 255))
    for col, filled in enumerate((False, True)):
        img.alpha_composite(cell(filled).resize((cell_px, cell_px), Image.NEAREST), (pad + col * (cell_px + pad), pad))
    img.save(OUT)
    print("saved", OUT, img.size)
