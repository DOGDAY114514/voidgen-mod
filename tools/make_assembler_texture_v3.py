"""Void assembler texture v3: AE2 pattern-provider composition (white casing,
dark ring, amber concentric core) with light pattern edits + animated colors.

Edits vs AE2 reference: chamfered amber core corners, four outer corner screws,
glowing 2x2 void core, hue-cycled core colors (8 frames).
"""
import colorsys
import io
import json
import os
import sys

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
REF = os.path.join(ROOT, "docs", "assembler_ref", "pattern_provider_block.png")
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "block")
OUT = os.path.join(TEX, "void_assembler.png")
FRAMES = 8
FRAME_TIME = 3
DARK_RING = (65, 63, 84, 255)


def is_amber(r, g, b, a):
    if a == 0:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return s > 0.45 and 0.02 <= h <= 0.16 and v > 0.3


def main():
    if not os.path.exists(REF):
        sys.exit("missing ref " + REF)
    base = Image.open(REF).convert("RGBA")
    if base.size != (16, 16):
        base = base.resize((16, 16), Image.NEAREST)

    edited = base.copy()
    px = edited.load()
    # chamfer core corners
    for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        px[x, y] = DARK_RING
    # outer corner screws
    for (x, y) in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        px[x, y] = (120, 124, 138, 255)
    # mark glowing centre (2x2) with a sentinel colour
    for y in (7, 8):
        for x in (7, 8):
            px[x, y] = (255, 0, 255, 255)

    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        frame = edited.copy()
        fp = frame.load()
        hue = f / float(FRAMES)
        pulse = 0.92 + 0.08 * abs(1.0 - 2.0 * ((f % 4) / 3.0))
        for y in range(16):
            for x in range(16):
                r, g, b, a = fp[x, y]
                if (r, g, b) == (255, 0, 255):
                    cr, cg, cb = colorsys.hsv_to_rgb((hue + 0.06) % 1.0, 0.18, 1.0)
                    fp[x, y] = (int(cr * 255), int(cg * 255), int(cb * 255), 255)
                elif is_amber(r, g, b, a):
                    _, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                    nv = min(1.0, (0.55 + 0.45 * (v - 0.55) / 0.40) * pulse)
                    if v > 0.88:
                        nv = min(1.0, nv + 0.05)
                    cr, cg, cb = colorsys.hsv_to_rgb(hue, 0.82, nv)
                    fp[x, y] = (int(cr * 255), int(cg * 255), int(cb * 255), a)
        strip.alpha_composite(frame, (0, f * 16))

    os.makedirs(TEX, exist_ok=True)
    strip.save(OUT)
    with io.open(OUT + ".mcmeta", "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"animation": {"frametime": FRAME_TIME, "interpolate": True}}, fh)
        fh.write("\n")
    print("saved", OUT, strip.size)


if __name__ == "__main__":
    main()
