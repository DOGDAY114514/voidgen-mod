"""Recolor AE2 logic processor / printed logic circuit board into void palette."""
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
REF = os.path.join(ROOT, "docs", "ref_processor")
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")

DEEP = (38, 22, 66)
MID = (74, 48, 126)
LIGHT = (150, 128, 214)
WHITE = (226, 218, 248)
CYAN = (130, 246, 255)
GOLD = (212, 178, 88)
GOLD_LIGHT = (238, 210, 128)
GOLD_DARK = (120, 88, 36)


def clamp(v):
    return max(0, min(255, int(v)))


def gold_shade(r, g, b):
    lum = (r * 299 + g * 587 + b * 114) // 1000
    if lum > 200:
        return GOLD_LIGHT
    if lum > 120:
        return GOLD
    return GOLD_DARK


def void_shade(r, g, b):
    lum = (r * 299 + g * 587 + b * 114) // 1000
    if lum < 80:
        return DEEP
    if lum < 140:
        return MID
    if lum < 200:
        return LIGHT
    return WHITE


def px_color_processor(r, g, b, y):
    if r > 140 and g < 90 and b < 90:
        return CYAN
    if y >= 10:
        return gold_shade(r, g, b)
    return void_shade(r, g, b)


def px_color_board(r, g, b, y):
    if y >= 10:
        return gold_shade(r, g, b)
    return void_shade(r, g, b)


def convert(src_name, dst_name, fn):
    src = Image.open(os.path.join(REF, src_name)).convert("RGBA")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = sp[x, y]
            if a == 0:
                continue
            if r < 18 and g < 18 and b < 18:
                continue
            op[x, y] = (*fn(r, g, b, y), a)
    out.save(os.path.join(OUT, dst_name + ".png"))


convert("logic_processor.png", "void_processor", px_color_processor)
convert("printed_logic_processor.png", "void_circuit_board", px_color_board)

# comparison sheet: ours on top, AE2 reference below
scale = 10
cell = 16 * scale
pad = 12
names = [("void_processor", "void_circuit_board")]
sheet = Image.new("RGBA", (2 * cell + 3 * pad, 2 * cell + 3 * pad), (22, 24, 30, 255))
for i, n in enumerate(names[0]):
    ours = Image.open(os.path.join(OUT, n + ".png")).convert("RGBA").resize((cell, cell), Image.NEAREST)
    sheet.alpha_composite(ours, (pad + i * (cell + pad), pad))
refs = ["logic_processor.png", "printed_logic_processor.png"]
for i, n in enumerate(refs):
    ref = Image.open(os.path.join(REF, n)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    sheet.alpha_composite(ref, (pad + i * (cell + pad), cell + 2 * pad))
sheet.save(os.path.join(ROOT, "docs", "void_processor_refs.png"))
print("done")
