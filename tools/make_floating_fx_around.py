"""Add orbiting FX *around* the original floating crystal / dust sprites (v2.5.3)."""
import json
import math
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")
FRAMES = 8
FRAMETIME = 3

CYAN = (118, 244, 255)
VIOLET = (196, 176, 255)
WHITE = (240, 238, 255)


def halo_mask(base: Image.Image):
    """Positions of transparent pixels touching the opaque silhouette."""
    dark = base.load()
    w, h = base.size
    out = []
    for y in range(h):
        for x in range(w):
            if dark[x, y][3] > 0:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and dark[nx, ny][3] > 0:
                        out.append((x, y))
                        break
                else:
                    continue
                break
    return out


def sparkle(d, x, y, color, big=False):
    if not (0 <= x < 16 and 0 <= y < 16):
        return
    d.point((x, y), fill=color + (255,))
    if big:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 16 and 0 <= ny < 16:
                d.point((nx, ny), fill=color + (140,))


def build(kind: str):
    base = Image.open(os.path.join(ROOT, "docs", "item_base", kind + ".png")).convert("RGBA")
    if base.size != (16, 16):
        base = base.crop((0, 0, 16, 16))
    mask = []  # keep the original sprite pristine; FX are the orbiting sparkles
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        frame = base.copy()
        px = frame.load()
        alpha = int(90 + 60 * abs(math.sin(math.pi * f / FRAMES)))
        for (hx, hy) in mask:
            if (hx + hy + f) % 3 != 0:
                continue
            px[hx, hy] = (150, 246, 255, alpha)
        d = ImageDraw.Draw(frame)
        for k in range(3):
            ang = f / FRAMES * 2 * math.pi + k * 2 * math.pi / 3
            x = int(round(7.5 + math.cos(ang) * 7.2))
            y = int(round(7.5 + math.sin(ang) * 7.2))
            color = CYAN if k != 1 else VIOLET
            sparkle(d, x, y, color, big=(k == f % 3))
        # extra faint mote drifting close to the sprite
        ang = f / FRAMES * 2 * math.pi * 2 + 1.1
        mx = int(round(7.5 + math.cos(ang) * 5.0))
        my = int(round(7.5 + math.sin(ang) * 5.0))
        if 0 <= mx < 16 and 0 <= my < 16 and frame.getpixel((mx, my))[3] == 0:
            d.point((mx, my), fill=WHITE + (70,))
        strip.paste(frame, (0, f * 16))
    strip.save(os.path.join(TEX, kind + ".png"))
    with open(os.path.join(TEX, kind + ".png.mcmeta"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"animation": {"frametime": FRAMETIME, "interpolate": True}}, fh)
    return strip


def preview(crystal, dust):
    scale = 8
    cell = 16 * scale
    gap = 10
    img = Image.new("RGBA", (FRAMES * (cell + gap) + gap, 2 * (cell + gap) + gap), (22, 24, 30, 255))
    for f in range(FRAMES):
        c = crystal.crop((0, f * 16, 16, f * 16 + 16)).resize((cell, cell), Image.NEAREST)
        d = dust.crop((0, f * 16, 16, f * 16 + 16)).resize((cell, cell), Image.NEAREST)
        img.alpha_composite(c, (gap + f * (cell + gap), gap))
        img.alpha_composite(d, (gap + f * (cell + gap), gap * 2 + cell))
    out = os.path.join(ROOT, "docs", "floating_fx_around.png")
    img.save(out)
    print("saved", out, img.size)


crystal = build("floating_crystal")
dust = build("floating_crystal_dust")
preview(crystal, dust)
print("done")
