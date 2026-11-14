"""Derive the ME Void Supplier block texture from AE2's ME Interface texture (interface.png),
recolor to the void palette and add an 8-frame animated pulse. Also draw a void value shard item."""
import io
import math
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
AE2 = r"D:\AI\voidgen-mod\docs\ae2_interface_ref\interface.png"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures")


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def scale(c, f):
    return (min(255, int(c[0] * f)), min(255, int(c[1] * f)), min(255, int(c[2] * f)))


def frame(base, t):
    img = base.copy()
    px = img.load()
    w, h = img.size
    pulse = 0.5 + 0.5 * math.sin(t / 8.0 * math.pi * 2.0)
    ring_a = (120, 236, 250)
    ring_b = (196, 140, 255)
    ring = mix(ring_a, ring_b, pulse)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum < 42:
                px[x, y] = (26, 22, 34, a)
            elif lum > 226:
                px[x, y] = (244, 242, 250, a)
            elif b > r + 10:
                if lum > 188:
                    px[x, y] = ring
                elif lum > 128:
                    px[x, y] = (104, 78, 176, a)
                else:
                    px[x, y] = (60, 42, 112, a)
            else:
                px[x, y] = (150, 146, 176, a)
    # pulsing center (the AE interface motif's middle block)
    d = ImageDraw.Draw(img)
    core = mix((150, 250, 255), (220, 170, 255), pulse)
    d.rectangle([6, 6, 9, 9], fill=scale(core, 0.55))
    d.rectangle([7, 7, 8, 8], fill=core)
    # two sparks travelling around the inner ring
    for k in range(2):
        ang = t / 8.0 * math.pi * 2.0 + k * math.pi
        cx = 8 + int(round(6.2 * math.cos(ang)))
        cy = 8 + int(round(6.2 * math.sin(ang)))
        if 0 <= cx < 16 and 0 <= cy < 16:
            d.point((cx, cy), fill=(235, 250, 255, 255))
    return img


def main():
    base = Image.open(AE2).convert("RGBA")
    strip = Image.new("RGBA", (16, 16 * 8), (0, 0, 0, 0))
    for i in range(8):
        strip.alpha_composite(frame(base, i), (0, i * 16))
    out = os.path.join(TEX, "block", "me_void_supplier.png")
    strip.save(out)
    io.open(out + ".mcmeta", "w", encoding="utf-8", newline="\n").write(
        '{\n  "animation": {\n    "frametime": 3,\n    "interpolate": true\n  }\n}\n'
    )

    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # shard: elongated diamond
    d.polygon([(8, 1), (12, 6), (11, 12), (8, 15), (5, 12), (4, 6)], fill=(86, 62, 150, 255))
    d.polygon([(8, 2), (11, 6), (10, 11), (8, 14), (6, 11), (5, 6)], fill=(140, 104, 220, 255))
    d.polygon([(8, 4), (10, 7), (9, 10), (8, 12), (7, 10), (6, 7)], fill=(196, 160, 255, 255))
    d.line([(8, 5), (8, 11)], fill=(250, 245, 255, 255))
    d.point((8, 6), fill=(255, 255, 255, 255))
    for x, y in ((2, 3), (13, 8), (11, 14)):
        d.point((x, y), fill=(180, 240, 255, 255))
    img.save(os.path.join(TEX, "item", "void_value.png"))
    print("supplier texture v2 + void value shard OK")


if __name__ == "__main__":
    main()
