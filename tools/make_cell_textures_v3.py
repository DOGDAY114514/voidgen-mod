"""v3: build the void disks directly from AE2's own cell pixel templates
(1K for the ribbon silhouette), recolor the tier strap (including its specular
highlight pixels), tint the plates toward void-lavender, and add sparkles.

This guarantees the silhouette / ribbon / LED layout exactly match AE2."""
import os

from PIL import Image

REF = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
OUT = r"D:\AI\voidgen-mod\docs\cells_v3"
os.makedirs(OUT, exist_ok=True)

SPARK = (186, 252, 255, 255)
SPARK_DIM = (110, 200, 240, 255)

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


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def strap_mask(px, w, h):
    """Mask of blue strap pixels plus the desaturated specular pixels around them."""
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
                # only absorb near-neutral highlights (specular white on the strap)
                if mx - mn <= 40 and mx > 150:
                    grown.add((nx, ny))
    return grown


def recolor_template(path, tier_rgb, sparkle=True, tint=0.05):
    img = Image.open(path).convert("RGBA")
    px = img.load()
    w, h = img.size
    deep = tuple(int(c * 0.55) for c in tier_rgb)
    light = mix(tier_rgb, (255, 255, 255), 0.45)
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
            elif 40 < lum and lum > 170:
                px[x, y] = (mix((r, g, b), (232, 222, 255), tint)[0],
                            mix((r, g, b), (232, 222, 255), tint)[1],
                            mix((r, g, b), (232, 222, 255), tint)[2], a)

    if sparkle:
        for (x, y) in [(1, 2), (14, 2), (2, 13), (13, 13), (8, 0), (0, 8), (15, 7), (7, 15)]:
            if px[x, y][3] == 0:
                px[x, y] = SPARK
                for (dx, dy) in [(1, 0), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
                        px[nx, ny] = SPARK_DIM
    return img


def main():
    base = os.path.join(REF, "item_storage_cell_1k.png")
    for tier, rgb in TIERS.items():
        recolor_template(base, rgb).save(os.path.join(OUT, f"void_cell_{tier}.png"))

    recolor_template(os.path.join(REF, "item_cell_housing.png"), (150, 150, 165), sparkle=True) \
        .save(os.path.join(OUT, "void_cell_housing.png"))

    # component: clean AE2-256k-style grey frame + dark socket + 4 cyan dots
    from PIL import ImageDraw
    comp = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(comp)
    d.rectangle([3, 3, 12, 12], fill=(58, 62, 72, 255))
    d.rectangle([2, 4, 13, 11], fill=(58, 62, 72, 255))
    d.rectangle([4, 2, 11, 13], fill=(58, 62, 72, 255))
    d.rectangle([4, 4, 11, 11], fill=(205, 211, 222, 255))
    d.line([4, 4, 11, 4], fill=(246, 248, 252, 255))
    d.line([4, 4, 4, 11], fill=(246, 248, 252, 255))
    d.line([4, 11, 11, 11], fill=(158, 164, 178, 255))
    d.line([11, 4, 11, 11], fill=(158, 164, 178, 255))
    d.rectangle([5, 5, 10, 10], fill=(40, 52, 68, 255))
    for (x, y) in [(6, 6), (9, 6), (6, 9), (9, 9)]:
        d.point((x, y), fill=(150, 226, 255, 255))
    d.point((7, 8), fill=(220, 250, 255, 255))
    d.point((8, 7), fill=(220, 250, 255, 255))
    for (x, y) in [(1, 1), (14, 14)]:
        d.point((x, y), fill=SPARK)
    comp.save(os.path.join(OUT, "void_component.png"))
    print("wrote", len(os.listdir(OUT)), "previews to", OUT)


if __name__ == "__main__":
    main()
