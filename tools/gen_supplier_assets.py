"""Generate assets for the ME Void Supplier (v2.2.0): animated block texture, models, recipe, loot, tag."""
import io
import json
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
TEX = os.path.join(RES, "assets", "voidgen", "textures")
MODEL = os.path.join(RES, "assets", "voidgen", "models", "block")
ITEM_MODEL = os.path.join(RES, "assets", "voidgen", "models", "item")
BLOCKSTATE = os.path.join(RES, "assets", "voidgen", "blockstates")
DATA = os.path.join(RES, "data", "voidgen")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


PANEL = (36, 38, 46, 255)
PANEL_LIGHT = (58, 62, 74, 255)
PANEL_DARK = (24, 26, 32, 255)
FRAME = (78, 84, 98, 255)
CORE = (44, 210, 200, 255)
CORE2 = (150, 90, 230, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def frame(t):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=PANEL)
    d.rectangle([0, 0, 15, 15], outline=FRAME)
    d.rectangle([1, 1, 14, 14], outline=PANEL_LIGHT)
    d.rectangle([1, 14, 14, 14], fill=PANEL_DARK)
    # three ports on the face
    for i, color in enumerate(((60, 220, 210), (150, 96, 235), (235, 96, 190))):
        x = 3 + i * 4
        d.rectangle([x, 3, x + 2, 9], fill=lerp(color, (255, 255, 255), 0.15))
        d.rectangle([x, 9, x + 2, 10], fill=lerp(color, (20, 20, 24), 0.35))
    # pulsing core wave
    phase = t / 8.0
    glow = lerp(CORE, CORE2, (1 + __import__("math").sin(phase * 6.283)) / 2)
    d.rectangle([5, 11, 10, 12], fill=glow)
    d.point((5, 11), fill=(255, 255, 255, 255))
    # travelling spark
    sx = 2 + int(12 * ((t * 3) % 8) / 8.0)
    d.point((sx, 13), fill=(220, 240, 255, 255))
    return img


def save_texture(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def make_block_texture():
    strips = [frame(i) for i in range(8)]
    out = Image.new("RGBA", (16, 16 * 8), (0, 0, 0, 0))
    for i, strip in enumerate(strips):
        out.alpha_composite(strip, (0, i * 16))
    save_texture(os.path.join(TEX, "block", "me_void_supplier.png"), out)
    io.open(os.path.join(TEX, "block", "me_void_supplier.png.mcmeta"), "w", encoding="utf-8", newline="\n").write(
        json.dumps({"animation": {"frametime": 3, "interpolate": True}}, indent=2) + "\n"
    )


def make_item_texture():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([3, 3, 12, 12], fill=(70, 34, 120, 255))
    d.ellipse([4, 4, 11, 11], fill=CORE2)
    d.ellipse([5, 5, 10, 10], fill=(200, 160, 255, 255))
    d.ellipse([6, 6, 9, 9], fill=(255, 255, 255, 255))
    for x, y in ((2, 3), (13, 5), (4, 12), (12, 12)):
        d.point((x, y), fill=(180, 240, 255, 255))
    save_texture(os.path.join(TEX, "item", "void_value.png"), img)


def main():
    make_block_texture()
    make_item_texture()
    write_json(os.path.join(BLOCKSTATE, "me_void_supplier.json"), {
        "variants": {"": {"model": "voidgen:block/me_void_supplier"}}
    })
    write_json(os.path.join(MODEL, "me_void_supplier.json"), {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": "voidgen:block/me_void_supplier"},
    })
    write_json(os.path.join(ITEM_MODEL, "me_void_supplier.json"), {
        "parent": "voidgen:block/me_void_supplier"
    })
    write_json(os.path.join(ITEM_MODEL, "void_value.json"), {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": "voidgen:item/void_value"},
    })
    write_json(os.path.join(RES, "data", "voidgen", "recipe", "me_void_supplier.json"), {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "key": {
            "V": {"item": "voidgen:void_ingot"},
            "Q": {"item": "minecraft:quartz"},
            "I": {"item": "voidgen:void_ingot_block"},
            "R": {"item": "minecraft:redstone_block"},
        },
        "pattern": ["VQV", "QIQ", "VRV"],
        "result": {"count": 1, "id": "voidgen:me_void_supplier"},
    })
    write_json(os.path.join(DATA, "loot_table", "blocks", "me_void_supplier.json"), {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0,
            "conditions": [{"condition": "minecraft:survives_explosion"}],
            "entries": [{"type": "minecraft:item", "name": "voidgen:me_void_supplier"}],
            "rolls": 1.0,
        }],
        "random_sequence": "voidgen:blocks/me_void_supplier",
    })
    tag_path = os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "pickaxe.json")
    tag = json.loads(io.open(tag_path, encoding="utf-8").read())
    if "voidgen:me_void_supplier" not in tag["values"]:
        tag["values"].append("voidgen:me_void_supplier")
    write_json(tag_path, tag)
    print("supplier assets OK")


if __name__ == "__main__":
    main()
