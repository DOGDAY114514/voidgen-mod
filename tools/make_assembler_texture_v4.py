"""Void assembler texture v4: pattern-provider composition with a *gradient*
rainbow core, sampled into many animation frames for a smooth in-game fade.

- 32 frames, frametime 2, interpolate=true (one full hue cycle = 64 ticks).
- Each frame shifts hue, and the hue also varies across the core pixels
  (diagonal rainbow gradient) instead of a flat colour.
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
FRAMES = 32
FRAME_TIME = 2
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
    for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        px[x, y] = DARK_RING
    for (x, y) in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        px[x, y] = (120, 124, 138, 255)
    for y in (7, 8):
        for x in (7, 8):
            px[x, y] = (255, 0, 255, 255)

    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        frame = edited.copy()
        fp = frame.load()
        hue0 = f / float(FRAMES)
        pulse = 0.9 + 0.1 * (0.5 + 0.5 * __import__("math").sin(2.0 * __import__("math").pi * f / FRAMES))
        for y in range(16):
            for x in range(16):
                r, g, b, a = fp[x, y]
                if (r, g, b) == (255, 0, 255):
                    hue = (hue0 + 0.05) % 1.0
                    cr, cg, cb = colorsys.hsv_to_rgb(hue, 0.16, 1.0)
                    fp[x, y] = (int(cr * 255), int(cg * 255), int(cb * 255), 255)
                elif is_amber(r, g, b, a):
                    _, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                    # diagonal gradient: hue advances toward the lower-right of the core
                    grad = 0.10 * ((x - 3) + (y - 3)) / 18.0
                    hue = (hue0 + grad) % 1.0
                    nv = min(1.0, (0.55 + 0.45 * (v - 0.55) / 0.40) * pulse)
                    if v > 0.88:
                        nv = min(1.0, nv + 0.05)
                    cr, cg, cb = colorsys.hsv_to_rgb(hue, 0.80, nv)
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
