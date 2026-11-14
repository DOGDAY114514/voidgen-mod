"""Generate assets for the AE2 void assembler block (v2.3.0).

Rainbow animated block texture derived from AE2's pattern provider texture,
plus blockstate/model/item model/recipe/loot/tag/lang entries.
"""
import colorsys
import io
import json
import os
import sys

from PIL import Image

ROOT = r"D:\AI\voidgen-mod"
REF = os.path.join(ROOT, "docs", "assembler_ref", "pattern_provider_block.png")
RES = os.path.join(ROOT, "src", "main", "resources")
TEX = os.path.join(RES, "assets", "voidgen", "textures", "block")
MODEL_BLOCK = os.path.join(RES, "assets", "voidgen", "models", "block")
MODEL_ITEM = os.path.join(RES, "assets", "voidgen", "models", "item")
BLOCKSTATES = os.path.join(RES, "assets", "voidgen", "blockstates")
LANG = os.path.join(RES, "assets", "voidgen", "lang")
DATA_RECIPE = os.path.join(RES, "data", "voidgen", "recipe")
DATA_LOOT = os.path.join(RES, "data", "voidgen", "loot_table", "blocks")
TAG = os.path.join(RES, "data", "minecraft", "tags", "block")

FRAMES = 8
FRAME_TIME = 3


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def hue_shift_frame(base, shift):
    img = base.copy()
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            if ss < 0.18:
                continue
            hh = (hh + shift) % 1.0
            ss = min(1.0, ss * 1.05)
            nr, ng, nb = colorsys.hsv_to_rgb(hh, ss, vv)
            px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), a)
    return img


def main():
    if not os.path.exists(REF):
        sys.exit("missing reference " + REF)
    base = Image.open(REF).convert("RGBA")
    if base.size != (16, 16):
        base = base.resize((16, 16), Image.NEAREST)

    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for i in range(FRAMES):
        strip.alpha_composite(hue_shift_frame(base, i / float(FRAMES)), (0, i * 16))
    os.makedirs(TEX, exist_ok=True)
    out_png = os.path.join(TEX, "void_assembler.png")
    strip.save(out_png)
    write_json(out_png + ".mcmeta", {"animation": {"frametime": FRAME_TIME, "interpolate": True}})

    write_json(os.path.join(BLOCKSTATES, "void_assembler.json"),
               {"variants": {"": {"model": "voidgen:block/void_assembler"}}})
    write_json(os.path.join(MODEL_BLOCK, "void_assembler.json"),
               {"parent": "minecraft:block/cube_all",
                "textures": {"all": "voidgen:block/void_assembler"}})
    write_json(os.path.join(MODEL_ITEM, "void_assembler.json"),
               {"parent": "voidgen:block/void_assembler"})

    write_json(os.path.join(DATA_RECIPE, "void_assembler.json"), {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [
            {"item": "ae2:pattern_provider"},
            {"item": "voidgen:void_ingot"},
            {"item": "voidgen:void_component_1k"},
        ],
        "result": {"count": 1, "id": "voidgen:void_assembler"},
        "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "ae2"}],
    })

    write_json(os.path.join(DATA_LOOT, "void_assembler.json"), {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0,
            "rolls": 1.0,
            "entries": [{
                "type": "minecraft:item",
                "name": "voidgen:void_assembler",
                "conditions": [{"condition": "minecraft:survives_explosion"}],
            }],
        }],
        "random_sequence": "voidgen:blocks/void_assembler",
    })

    tag_path = os.path.join(TAG, "mineable", "pickaxe.json")
    tag = json.load(io.open(tag_path, encoding="utf-8")) if os.path.exists(tag_path) else {"replace": False, "values": []}
    if "voidgen:void_assembler" not in tag["values"]:
        tag["values"].append("voidgen:void_assembler")
    write_json(tag_path, tag)

    for locale, entries in {
        "en_us": {
            "block.voidgen.void_assembler": "Void Assembler",
            "tooltip.voidgen.void_assembler": "Instantly crafts AE2 processors inside the ME network (no inputs, no machine).",
        },
        "zh_cn": {
            "block.voidgen.void_assembler": "虚空合成器",
            "tooltip.voidgen.void_assembler": "在 ME 网络中瞬间合成 AE2 处理器（不消耗材料、不需要机器）。",
        },
    }.items():
        path = os.path.join(LANG, locale + ".json")
        lang = json.load(io.open(path, encoding="utf-8"))
        lang.update(entries)
        write_json(path, lang)

    print("void assembler assets written")


if __name__ == "__main__":
    main()
