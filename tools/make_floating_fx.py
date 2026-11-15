"""Floating crystal & dust with FX: animated 8-frame strips + mcmeta (v2.5.2)."""
import json
import math
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")
FRAMES = 8
FRAMETIME = 3

DEEP = (44, 22, 84, 255)
BODY = (136, 104, 226, 255)
LIGHT = (198, 182, 255, 255)
WHITE = (240, 238, 255, 255)
CYAN = (118, 244, 255, 255)
CYAN_DIM = (70, 160, 220, 255)
GLOW = (118, 244, 255, 60)


def draw_crystal() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # tilted shard, amethyst-shard style silhouette
    n = 13
    for i in range(n):
        t = i / (n - 1)
        x = int(round(10.5 - 5.5 * t))
        y = int(round(2 + 11 * t))
        d.point((x - 1, y), fill=DEEP)
        d.point((x, y), fill=BODY)
        d.point((x + 1, y), fill=DEEP)
    # facet highlight along the upper edge
    for i in range(2, n - 2):
        t = i / (n - 1)
        x = int(round(10.5 - 5.5 * t))
        y = int(round(2 + 11 * t))
        d.point((x, y - 1), fill=LIGHT)
    d.point((9, 4), fill=WHITE)
    d.point((8, 5), fill=WHITE)
    # glowing cyan core near the middle
    d.point((7, 8), fill=CYAN)
    d.point((6, 9), fill=CYAN)
    d.point((7, 9), fill=WHITE)
    return img


def draw_dust(phase: float) -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 7.5, 7.5
    for i in range(11):
        ang = phase + i * 0.62
        r = 1.6 + i * 0.32
        x = int(round(cx + math.cos(ang) * r))
        y = int(round(cy + math.sin(ang) * r))
        t = i / 10.0
        if i in (3, 8):
            col = CYAN
        else:
            col = (
                int(BODY[0] + (LIGHT[0] - BODY[0]) * t),
                int(BODY[1] + (LIGHT[1] - BODY[1]) * t),
                int(BODY[2] + (LIGHT[2] - BODY[2]) * t),
                255,
            )
        d.point((x, y), fill=col)
        if i % 3 == 0:
            d.point((x + 1, y), fill=(col[0], col[1], col[2], 120))
    d.point((7, 7), fill=WHITE)
    d.point((8, 8), fill=CYAN)
    d.point((8, 6), fill=CYAN_DIM)
    return img


def sparkles(d, frame: int):
    cx, cy = 7.5, 7.5
    for k in range(3):
        ang = frame / FRAMES * 2 * math.pi + k * 2 * math.pi / 3
        r = 7.2
        x = int(round(cx + math.cos(ang) * r))
        y = int(round(cy + math.sin(ang) * r))
        d.point((x, y), fill=CYAN)
        d.point((x + 1, y), fill=(CYAN[0], CYAN[1], CYAN[2], 120))
        d.point((x, y + 1), fill=(CYAN[0], CYAN[1], CYAN[2], 90))


def build(kind: str):
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        base = draw_crystal() if kind == "crystal" else draw_dust(f / FRAMES * 2 * math.pi)
        d = ImageDraw.Draw(base)
        sparkles(d, f)
        strip.paste(base, (0, f * 16))
    names = {"crystal": "floating_crystal", "dust": "floating_crystal_dust"}
    base = names[kind]
    out = os.path.join(TEX, base + ".png")
    strip.save(out)
    meta = os.path.join(TEX, base + ".png.mcmeta")
    with open(meta, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"animation": {"frametime": FRAMETIME, "interpolate": True}}, fh)
    return strip


def preview(crystal: Image.Image, dust: Image.Image):
    scale = 8
    cell = 16 * scale
    gap = 10
    img = Image.new("RGBA", (FRAMES * (cell + gap) + gap, 2 * (cell + gap) + gap), (22, 24, 30, 255))
    for f in range(FRAMES):
        c = crystal.crop((0, f * 16, 16, f * 16 + 16)).resize((cell, cell), Image.NEAREST)
        d = dust.crop((0, f * 16, 16, f * 16 + 16)).resize((cell, cell), Image.NEAREST)
        img.alpha_composite(c, (gap + f * (cell + gap), gap))
        img.alpha_composite(d, (gap + f * (cell + gap), gap * 2 + cell))
    out = os.path.join(ROOT, "docs", "floating_fx_frames.png")
    img.save(out)
    print("saved", out, img.size)


crystal = build("crystal")
dust = build("dust")
preview(crystal, dust)
print("done")
