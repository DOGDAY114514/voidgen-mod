"""Derive void storage components from the real AE2 / MEGA Cells component sprites."""
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
REF = os.path.join(ROOT, "docs", "ref_components")
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")

TIERS = [
    ("1k", (168, 186, 206), (255, 255, 255), "ref_component_1k.png"),
    ("4k", (246, 200, 66), (255, 236, 160), "ref_component_4k.png"),
    ("16k", (92, 228, 244), (200, 250, 255), "ref_component_16k.png"),
    ("64k", (78, 220, 132), (190, 255, 220), "ref_component_64k.png"),
    ("256k", (224, 92, 255), (250, 200, 255), "ref_component_256k.png"),
    ("1m", (255, 150, 60), (255, 220, 160), "ref_component_1m.png"),
    ("4m", (255, 90, 90), (255, 190, 190), "ref_component_4m.png"),
    ("16m", (90, 150, 255), (200, 220, 255), "ref_component_16m.png"),
    ("64m", (40, 230, 200), (190, 255, 245), "ref_component_64m.png"),
    ("256m", (235, 240, 255), (255, 255, 255), "ref_component_256m.png"),
]

SPARKLES = [(1, 4), (14, 5), (3, 14), (13, 13)]


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def main():
    os.makedirs(OUT, exist_ok=True)
    for key, tier, light, fname in TIERS:
        img = Image.open(os.path.join(REF, fname)).convert("RGBA")
        px = img.load()
        for y in range(16):
            for x in range(16):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                mx, mn = max(r, g, b), min(r, g, b)
                lum = (r * 30 + g * 59 + b * 11) // 100
                if mx - mn >= 38 and mx > 60:
                    # coloured accent: repaint in the tier colour, keep brightness
                    factor = 0.62 + 0.5 * (lum / 255.0)
                    col = tuple(min(255, int(c * factor)) for c in tier)
                    if lum > 165:
                        col = mix(col, light, 0.35)
                    px[x, y] = (col[0], col[1], col[2], a)
                else:
                    if lum >= 150:
                        col = mix((r, g, b), light, 0.10)
                        px[x, y] = (col[0], col[1], col[2], a)
                    else:
                        # dark MEGA shell: push slightly violet so it reads as void material
                        rr = min(255, r + 6)
                        bb = min(255, b + 12)
                        px[x, y] = (rr, g, bb, a)

        for (sx, sy) in SPARKLES:
            if 0 <= sx < 16 and 0 <= sy < 16 and px[sx, sy][3] == 0:
                px[sx, sy] = (light[0], light[1], light[2], 235)

        img.save(os.path.join(OUT, "void_component_%s.png" % key))
        print("wrote void_component_%s.png" % key)


if __name__ == "__main__":
    main()
