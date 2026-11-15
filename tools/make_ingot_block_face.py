import io, json, os
from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
TEX = os.path.join(RES, "assets", "voidgen", "textures")
MODELS = os.path.join(RES, "assets", "voidgen", "models")
DATA = os.path.join(RES, "data", "voidgen")

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

# ---- block face texture ----
W = 16
img = Image.new("RGBA", (W, W), (62, 40, 112, 255))
d = ImageDraw.Draw(img)
OUTLINE = (26, 15, 48, 255)
BEVEL_L = (152, 122, 222, 255)
BEVEL_D = (34, 21, 60, 255)
PANEL = (74, 48, 128, 255)
PANEL_D = (55, 35, 98, 255)
CYAN = (110, 240, 255, 255)
CYAN_D = (58, 160, 184, 255)
CENTER = (206, 255, 255, 255)

d.rectangle([0, 0, 15, 15], fill=OUTLINE)
d.rectangle([1, 1, 14, 14], fill=BEVEL_L)
d.rectangle([1, 1, 13, 13], fill=PANEL)
d.rectangle([2, 2, 13, 13], fill=PANEL)
d.rectangle([14, 1, 14, 14], fill=BEVEL_D)
d.rectangle([1, 14, 14, 14], fill=BEVEL_D)
d.rectangle([2, 2, 13, 13], outline=CYAN_D)
# diamond inlay
for x in range(16):
    for y in range(16):
        dx, dy = abs(x - 7.5), abs(y - 7.5)
        dist = dx + dy
        if 5.0 <= dist <= 5.9:
            img.putpixel((x, y), CYAN)
        elif dist <= 1.6:
            img.putpixel((x, y), CENTER)
        elif 2.0 <= dist <= 2.9:
            img.putpixel((x, y), CYAN_D)
# corner studs
for (cx, cy) in ((3, 3), (12, 3), (3, 12), (12, 12)):
    img.putpixel((cx, cy), (150, 120, 220, 255))
    img.putpixel((cx + (1 if cx < 8 else -1), cy), BEVEL_D)
tex_dir = os.path.join(TEX, "block")
os.makedirs(tex_dir, exist_ok=True)
img.save(os.path.join(tex_dir, "void_ingot_block.png"))

# ---- blockstate / models ----
write_json(os.path.join(RES, "assets", "voidgen", "blockstates", "void_ingot_block.json"),
           {"variants": {"": {"model": "voidgen:block/void_ingot_block"}}})
write_json(os.path.join(MODELS, "block", "void_ingot_block.json"),
           {"parent": "minecraft:block/cube_all", "textures": {"all": "voidgen:block/void_ingot_block"}})
write_json(os.path.join(MODELS, "item", "void_ingot_block.json"),
           {"parent": "voidgen:block/void_ingot_block"})

# ---- loot table ----
write_json(os.path.join(DATA, "loot_table", "blocks", "void_ingot_block.json"), {
    "type": "minecraft:block",
    "pools": [{
        "bonus_rolls": 0.0,
        "entries": [{"type": "minecraft:item", "name": "voidgen:void_ingot_block"}],
        "rolls": 1.0
    }],
    "random_sequence": "voidgen:blocks/void_ingot_block"
})

# ---- pickaxe tag ----
tag_path = os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "pickaxe.json")
tag = json.load(io.open(tag_path, encoding="utf-8"))
vals = tag.setdefault("values", [])
if "voidgen:void_ingot_block" not in vals:
    vals.append("voidgen:void_ingot_block")
write_json(tag_path, tag)

# ---- remove unused item texture ----
old = os.path.join(TEX, "item", "void_ingot_block.png")
if os.path.exists(old):
    os.remove(old)

# ---- lang: item key -> block key ----
for loc in ("en_us", "zh_cn"):
    p = os.path.join(RES, "assets", "voidgen", "lang", loc + ".json")
    data = json.load(io.open(p, encoding="utf-8"))
    name = data.pop("item.voidgen.void_ingot_block", None)
    if name is not None:
        data["block.voidgen.void_ingot_block"] = name
    order = {k: i for i, k in enumerate(sorted(data))}
    data = dict(sorted(data.items()))
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("block face + assets written")