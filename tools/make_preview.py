"""Compose docs/preview.png: v1.4 textures at 6x on a dark background."""
import os

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
TEX = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "textures")

TILES = [
    ("block", "void_generator_top"),
    ("block", "void_generator_side"),
    ("block", "void_generator_bottom"),
    ("block", "void_furnace_top"),
    ("block", "void_furnace_side"),
    ("block", "void_furnace_bottom"),
    ("item", "nest_upgrade_1"),
    ("item", "nest_upgrade_2"),
    ("item", "nest_upgrade_3"),
    ("item", "nest_upgrade_4"),
    ("item", "nest_upgrade_5"),
    ("item", "accel_card"),
    ("item", "overclock_card"),
    ("item", "capacity_card"),
    ("item", "range_card"),
    ("item", "binding_card"),
    ("item", "void_configurator"),
]

SCALE = 6
GAP = 10
PAD = 16
CELL = 16 * SCALE

bg = Image.new("RGBA", (PAD * 2 + len(TILES) * CELL + (len(TILES) - 1) * GAP, PAD * 2 + CELL), (22, 16, 32, 255))

for index, (folder, name) in enumerate(TILES):
    path = os.path.join(TEX, folder, name + ".png")
    img = Image.open(path).convert("RGBA")
    img = img.resize((CELL, CELL), Image.NEAREST)
    x = PAD + index * (CELL + GAP)
    bg.alpha_composite(img, (x, PAD))

out = os.path.join(ROOT, "docs", "preview.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
bg.save(out)
print("saved", out, bg.size)
