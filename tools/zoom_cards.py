"""Temporary close-up of the five card textures (10x)."""
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures", "item")
CARDS = ["accel_card", "overclock_card", "capacity_card", "range_card", "binding_card"]

SCALE = 10
CELL = 16 * SCALE
GAP = 12
PAD = 16

bg = Image.new("RGBA", (PAD * 2 + len(CARDS) * CELL + (len(CARDS) - 1) * GAP, PAD * 2 + CELL), (18, 20, 24, 255))
for i, card in enumerate(CARDS):
    img = Image.open(os.path.join(TEX, card + ".png")).convert("RGBA").resize((CELL, CELL), Image.NEAREST)
    bg.alpha_composite(img, (PAD + i * (CELL + GAP), PAD))

out = os.path.join(ROOT, "docs", "zoom_cards.png")
bg.save(out)
print("saved", out, bg.size)
