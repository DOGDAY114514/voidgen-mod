"""Temporary close-up check for the three furnace faces (12x)."""
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "block")
FACES = ["void_furnace_top", "void_furnace_side", "void_furnace_bottom"]

SCALE = 12
CELL = 16 * SCALE
GAP = 12
PAD = 16

img = Image.new("RGBA", (PAD * 2 + len(FACES) * CELL + (len(FACES) - 1) * GAP, PAD * 2 + CELL), (18, 20, 24, 255))
for i, face in enumerate(FACES):
    tile = Image.open(os.path.join(TEX, face + ".png")).convert("RGBA").resize((CELL, CELL), Image.NEAREST)
    img.alpha_composite(tile, (PAD + i * (CELL + GAP), PAD))

out = os.path.join(ROOT, "docs", "zoom_furnace.png")
img.save(out)
print("saved", out, img.size)
