"""Redraw the void assembler block texture: AE2-flavoured frame, hex void sigil,
animated color cycling. Not a straight recolor of AE2's pattern provider."""
import colorsys
import io
import json
import os
import sys

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "block")
OUT = os.path.join(TEX, "void_assembler.png")
FRAMES = 8
FRAME_TIME = 3


def hsv(h, s=0.88, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def frame(f):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    hue = f / float(FRAMES)
    c = hsv(hue)
    c2 = hsv(hue + 0.10)
    bright = 0.55 + 0.45 * abs(1.0 - 2.0 * (f / float(FRAMES) - 0.5))  # pulse

    # ---- frame: dark outline / bevelled metal / dark inset ----
    d.rectangle([0, 0, 15, 15], fill=(10, 12, 18, 255))
    d.rectangle([1, 1, 14, 14], fill=(52, 56, 68, 255))
    d.line([1, 1, 14, 1], fill=(190, 198, 214, 255))
    d.line([1, 1, 1, 14], fill=(190, 198, 214, 255))
    d.line([1, 14, 14, 14], fill=(64, 70, 84, 255))
    d.line([14, 1, 14, 14], fill=(64, 70, 84, 255))
    d.rectangle([2, 2, 13, 13], fill=(24, 27, 36, 255))
    d.rectangle([3, 3, 12, 12], fill=(36, 40, 52, 255))

    # ---- corner void runes ----
    for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        d.point((x, y), fill=(14, 16, 24, 255))
    for (x, y) in [(4, 4), (11, 4), (4, 11), (11, 11)]:
        d.point((x, y), fill=c + (110,))

    # ---- hex sigil ----
    hex_rows = {
        4: [6, 7, 8, 9],
        5: [4, 5, 10, 11],
        6: [3, 12],
        7: [3, 12],
        8: [3, 12],
        9: [3, 12],
        10: [4, 5, 10, 11],
        11: [6, 7, 8, 9],
    }
    for y, xs in hex_rows.items():
        for x in xs:
            d.point((x, y), fill=c + (255,))

    # ---- top/bottom conduit ----
    for (x, y) in [(7, 3), (8, 3), (7, 12), (8, 12)]:
        d.point((x, y), fill=c2 + (255,))

    # ---- core ----
    core = hsv(hue + 0.02, 0.35, bright)
    d.rectangle([7, 7, 8, 8], fill=core + (255,))
    d.point((7, 7), fill=(255, 255, 255, 255))

    return img


def main():
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for i in range(FRAMES):
        strip.alpha_composite(frame(i), (0, i * 16))
    os.makedirs(TEX, exist_ok=True)
    strip.save(OUT)
    with io.open(OUT + ".mcmeta", "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"animation": {"frametime": FRAME_TIME, "interpolate": True}}, fh)
        fh.write("\n")
    print("saved", OUT, strip.size)


if __name__ == "__main__":
    main()
