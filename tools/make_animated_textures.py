"""Build animated 8-frame strips (+ .mcmeta) for the void disks and components."""
import json
import math
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
REF_CELL = os.path.join(ROOT, "docs", "ae2_ref", "assets", "ae2", "textures", "item", "item_storage_cell_1k.png")
REF_COMP = os.path.join(ROOT, "docs", "ref_components")
OUT = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")

FRAMES = 8
FRAMETIME = 2

GEM_KEYS = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]

# per-tier disk accent (same as prior cell palette)
DISK_COLORS = {
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

# per-tier component accent + sparkle colour
COMP_COLORS = {
    "1k": ((168, 186, 206), (240, 250, 255)),
    "4k": ((246, 200, 66), (255, 236, 160)),
    "16k": ((92, 228, 244), (200, 250, 255)),
    "64k": ((78, 220, 132), (190, 255, 220)),
    "256k": ((224, 92, 255), (250, 200, 255)),
    "1m": ((255, 150, 60), (255, 220, 160)),
    "4m": ((255, 90, 90), (255, 190, 190)),
    "16m": ((90, 150, 255), (200, 220, 255)),
    "64m": ((40, 230, 200), (190, 255, 245)),
    "256m": ((235, 240, 255), (255, 255, 255)),
}

RING = [(1, 3), (3, 1), (6, 0), (9, 0), (13, 2), (15, 5), (15, 9), (13, 14),
        (9, 15), (6, 15), (2, 13), (0, 10), (0, 6), (3, 13), (12, 1), (12, 14)]


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def strap_mask(px, w, h):
    mask = set()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            if mx - mn >= 45 and b > r and b >= g - 10:
                mask.add((x, y))
    grown = set(mask)
    for (x, y) in mask:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                r, g, b, a = px[nx, ny]
                if a == 0:
                    continue
                mx, mn = max(r, g, b), min(r, g, b)
                if mx - mn <= 40 and mx > 150:
                    grown.add((nx, ny))
    return grown


def base_cell(tier):
    tier_rgb = DISK_COLORS[tier]
    img = Image.open(REF_CELL).convert("RGBA")
    px = img.load()
    w, h = img.size
    mask = strap_mask(px, w, h)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            lum = (r + g + b) / 3.0
            if (x, y) in mask:
                factor = 0.72 + 0.32 * (lum / 255.0)
                col = tuple(min(255, int(c * factor)) for c in tier_rgb)
                if lum > 150:
                    col = mix(col, (255, 255, 255), 0.18)
                px[x, y] = (col[0], col[1], col[2], a)
            elif lum > 170:
                col = mix((r, g, b), (232, 222, 255), 0.05)
                px[x, y] = (col[0], col[1], col[2], a)
    return img, mask


def base_component(tier):
    tier_rgb, light = COMP_COLORS[tier]
    img = Image.open(os.path.join(REF_COMP, "ref_component_%s.png" % tier)).convert("RGBA")
    px = img.load()
    mask = set()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            lum = (r * 30 + g * 59 + b * 11) // 100
            if mx - mn >= 38 and mx > 60:
                mask.add((x, y))
                factor = 0.62 + 0.5 * (lum / 255.0)
                col = tuple(min(255, int(c * factor)) for c in tier_rgb)
                if lum > 165:
                    col = mix(col, light, 0.35)
                px[x, y] = (col[0], col[1], col[2], a)
            elif lum >= 150:
                col = mix((r, g, b), light, 0.10)
                px[x, y] = (col[0], col[1], col[2], a)
            else:
                px[x, y] = (min(255, r + 6), g, min(255, b + 12), a)
    return img, mask


def animated_strip(base, accent_mask, spark_rgb, prefix):
    frames = []
    w, h = base.size
    for f in range(FRAMES):
        frame = base.copy()
        px = frame.load()
        pulse = 1.0 + 0.10 * math.sin(2 * math.pi * f / FRAMES)
        for (x, y) in accent_mask:
            r, g, b, a = px[x, y]
            px[x, y] = (min(255, int(r * pulse)), min(255, int(g * pulse)),
                        min(255, int(b * pulse)), a)
        for i in (0, 3, 6):
            sx, sy = RING[(f * 2 + i) % len(RING)]
            if 0 <= sx < w and 0 <= sy < h and px[sx, sy][3] == 0:
                px[sx, sy] = (spark_rgb[0], spark_rgb[1], spark_rgb[2], 255)
        frames.append(frame)

    strip = Image.new("RGBA", (w, h * FRAMES), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        strip.paste(frame, (0, i * h))
    strip.save(os.path.join(OUT, prefix + ".png"))
    with open(os.path.join(OUT, prefix + ".png.mcmeta"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"animation": {"frametime": FRAMETIME, "interpolate": True}}, fh)
        fh.write("\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    for tier in GEM_KEYS:
        img, mask = base_cell(tier)
        animated_strip(img, mask, (200, 240, 255), "void_cell_%s" % tier)
        img, mask = base_component(tier)
        animated_strip(img, mask, COMP_COLORS[tier][1], "void_component_%s" % tier)
        print("animated", tier)


if __name__ == "__main__":
    main()
