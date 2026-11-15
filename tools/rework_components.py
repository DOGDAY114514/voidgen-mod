"""Rework void components (names + AE2-order recipes), add void processor / circuit board."""
import json
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
MODID = "voidgen"
TIERS = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
PREV = {t: TIERS[i - 1] for i, t in enumerate(TIERS) if i > 0}


def wj(rel, obj):
    p = os.path.join(RES, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def lj(rel):
    with open(os.path.join(RES, rel), encoding="utf-8") as fh:
        return json.load(fh)


def tex(name, draw):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw(ImageDraw.Draw(img), img.load())
    p = os.path.join(RES, "assets", MODID, "textures", "item", name + ".png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)


def board_tex(d, px):
    d.rectangle([2, 2, 13, 13], fill=(20, 46, 34, 255))
    d.rectangle([2, 2, 13, 13], outline=(12, 28, 20, 255))
    for y in (5, 8, 11):
        d.line([(4, y), (11, y)], fill=(190, 158, 82, 255))
    for x in (4, 7, 10):
        d.rectangle([x, 4, x + 1, 11], fill=(24, 60, 40, 255))
    d.rectangle([7, 7, 8, 8], fill=(130, 246, 255, 255))
    d.point((4, 8), fill=(196, 164, 84, 255))
    d.point((11, 8), fill=(196, 164, 84, 255))
    d.point((3, 3), fill=(196, 164, 84, 255))
    d.point((12, 12), fill=(196, 164, 84, 255))


def processor_tex(d, px):
    d.rectangle([3, 3, 12, 12], fill=(52, 30, 92, 255))
    d.rectangle([3, 3, 12, 12], outline=(30, 16, 56, 255))
    d.rectangle([5, 5, 10, 10], fill=(96, 64, 168, 255))
    d.rectangle([6, 6, 9, 9], fill=(24, 12, 44, 255))
    d.rectangle([7, 7, 8, 8], fill=(130, 246, 255, 255))
    for x in (4, 6, 8, 10, 12):
        d.point((x, 1), fill=(210, 176, 90, 255))
        d.point((x, 14), fill=(210, 176, 90, 255))
    d.point((2, 5), fill=(210, 176, 90, 255))
    d.point((2, 9), fill=(210, 176, 90, 255))
    d.point((13, 5), fill=(210, 176, 90, 255))
    d.point((13, 9), fill=(210, 176, 90, 255))
    d.point((5, 4), fill=(150, 120, 210, 255))


tex("void_circuit_board", board_tex)
tex("void_processor", processor_tex)

for item in ("void_circuit_board", "void_processor"):
    wj(f"assets/{MODID}/models/item/{item}.json",
       {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{item}"}})

# ---- delete old component recipes ----
recipe_dir = os.path.join(RES, "data", MODID, "recipe")
for t in TIERS:
    p = os.path.join(recipe_dir, f"void_component_{t}.json")
    if os.path.exists(p):
        os.remove(p)

# ---- new component recipes, mirrored on AE2's progression ----
COND_AE2 = [{"type": "neoforge:mod_loaded", "modid": "ae2"}]
for t in TIERS:
    if t == "1k":
        key = {
            "a": {"tag": "c:dusts/redstone"},
            "b": {"item": f"{MODID}:floating_crystal"},
            "c": {"item": "ae2:logic_processor"},
        }
        pattern = ["aba", "bcb", "aba"]
    else:
        dust = {"tag": "c:dusts/redstone"} if t == "4k" else {"tag": "c:dusts/coal"}
        processor = {"item": f"{MODID}:void_processor"} if t in ("1m", "4m", "16m", "64m", "256m") \
            else {"item": "ae2:calculation_processor"}
        key = {
            "a": dust,
            "b": processor,
            "c": {"item": f"{MODID}:void_component_{PREV[t]}"},
            "d": {"item": "ae2:quartz_glass"},
        }
        pattern = ["aba", "cdc", "aca"]
    wj(f"data/{MODID}/recipe/void_component_{t}.json", {
        "neoforge:conditions": COND_AE2,
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "key": key,
        "pattern": pattern,
        "result": {"count": 1, "id": f"{MODID}:void_component_{t}"},
    })

# ---- void block: 4 floating crystals ----
wj(f"data/{MODID}/recipe/void_ingot_block.json", {
    "type": "minecraft:crafting_shaped",
    "category": "misc",
    "key": {"f": {"item": f"{MODID}:floating_crystal"}},
    "pattern": ["ff", "ff"],
    "result": {"count": 1, "id": f"{MODID}:void_ingot_block"},
})

# ---- circuit cutter: void block -> 4 circuit boards ----
wj(f"data/{MODID}/recipe/void_circuit_board.json", {
    "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "extendedae"}],
    "type": "extendedae:circuit_cutter",
    "input": {"ingredient": {"item": f"{MODID}:void_ingot_block"}},
    "output": {"count": 4, "id": f"{MODID}:void_circuit_board"},
})

# ---- crystal assembler: board + silicon plate + coal dust -> floating processor ----
wj(f"data/{MODID}/recipe/void_processor.json", {
    "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "extendedae"}],
    "type": "extendedae:crystal_assembler",
    "input_items": [
        {"amount": 4, "ingredient": {"item": f"{MODID}:void_circuit_board"}},
        {"amount": 4, "ingredient": {"item": "ae2:printed_silicon"}},
        {"amount": 4, "ingredient": {"tag": "c:dusts/coal"}},
    ],
    "output": {"count": 4, "id": f"{MODID}:void_processor"},
})

# ---- lang ----
TIER_LABEL = {t: t.upper() for t in TIERS}
EN = {}
ZH = {}
for t in TIERS:
    EN[f"item.voidgen.void_component_{t}"] = f"Void Storage Component {TIER_LABEL[t]}"
    ZH[f"item.voidgen.void_component_{t}"] = f"虚无存储组件 {TIER_LABEL[t]}"
EN.update({
    "item.voidgen.void_processor": "Floating Processor",
    "item.voidgen.void_circuit_board": "Void Circuit Board",
    "tooltip.voidgen.void_processor": "Pressed in the crystal assembler from a void circuit board, printed silicon and coal dust.",
    "tooltip.voidgen.void_circuit_board": "Sliced from a void block in the circuit cutter.",
    "tooltip.voidgen.void_ingot_block": "Four floating crystals compressed into one block; slices into circuit boards.",
})
ZH.update({
    "item.voidgen.void_processor": "虚浮处理器",
    "item.voidgen.void_circuit_board": "虚无电路板",
    "tooltip.voidgen.void_processor": "在水晶装配器中由虚无电路板、硅板、煤粉压制成型。",
    "tooltip.voidgen.void_circuit_board": "用切片器切割虚无块获得。",
    "tooltip.voidgen.void_ingot_block": "四个虚浮水晶压成的方块，可切割成虚无电路板。",
})
for lang, extra in (("en_us", EN), ("zh_cn", ZH)):
    rel = f"assets/{MODID}/lang/{lang}.json"
    data = lj(rel)
    data.update(extra)
    wj(rel, data)

print("components/recipes/lang done")
