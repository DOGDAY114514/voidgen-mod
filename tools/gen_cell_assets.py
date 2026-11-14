"""Generate models, recipes and lang for the AE2-style void disks (clean, idempotent)."""
import json
import os

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
MODELS_ITEM = os.path.join(RES, "assets", "voidgen", "models", "item")
RECIPES = os.path.join(RES, "data", "voidgen", "recipe")
LANG = os.path.join(RES, "assets", "voidgen", "lang")

MODID = "voidgen"

# (id suffix, display label, bytes, recipe material, material count)
TIERS = [
    ("1k", "1K", 1_024, "minecraft:redstone_block", 0),
    ("4k", "4K", 4_096, "minecraft:gold_block", 1),
    ("16k", "16K", 16_384, "minecraft:diamond_block", 1),
    ("64k", "64K", 65_536, "minecraft:emerald_block", 2),
    ("256k", "256K", 262_144, "minecraft:netherite_ingot", 2),
    ("1m", "1M", 1_048_576, "minecraft:diamond_block", 3),
    ("4m", "4M", 4_194_304, "minecraft:emerald_block", 3),
    ("16m", "16M", 16_777_216, "minecraft:amethyst_block", 4),
    ("64m", "64M", 67_108_864, "minecraft:nether_star", 4),
    ("256m", "256M", 268_435_456, "minecraft:nether_star", 5),
]

INGOT = {"item": "voidgen:void_ingot"}
INGOT_BLOCK = {"item": "voidgen:void_ingot_block"}


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def item_model(name):
    write_json(os.path.join(MODELS_ITEM, name + ".json"), {
        "parent": "minecraft:item/generated",
        "textures": {"layer0": "voidgen:item/" + name},
    })


def shaped(name, pattern, key, count, condition=True):
    data = {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "key": {k: v for k, v in key.items()},
        "pattern": pattern,
        "result": {"count": count, "id": MODID + ":" + name},
    }
    if condition:
        data = {"neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "ae2"}], **data}
    write_json(os.path.join(RECIPES, name + ".json"), data)


def shapeless(name, ingredients, count, condition=True, result_id=None):
    assert len(ingredients) <= 9, (name, len(ingredients))
    data = {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": ingredients,
        "result": {"count": count, "id": MODID + ":" + (result_id or name)},
    }
    if condition:
        data = {"neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "ae2"}], **data}
    write_json(os.path.join(RECIPES, name + ".json"), data)


def disk_extras(key):
    tier = dict(zip([t[0] for t in TIERS], TIERS))[key]
    amount = tier[4]
    if amount == 0:
        return []
    if amount == 1:
        return [INGOT]
    return [INGOT_BLOCK] * (amount - 1) + [INGOT]


def main():
    item_model("void_ingot")
    item_model("void_ingot_block")
    item_model("void_cell_housing")
    for key, *_ in TIERS:
        item_model("void_component_" + key)
        item_model("void_cell_" + key)

    # base materials
    shapeless("void_ingot", [
        {"item": "voidgen:filled_void_storage_emerald"},
        {"item": "minecraft:nether_star"},
        {"item": "minecraft:diamond_block"},
    ], 8, condition=False)
    shaped("void_ingot_block", ["iii", "iii", "iii"], {"i": INGOT}, 1, condition=False)
    shapeless("void_ingot_from_block", [INGOT_BLOCK], 9, condition=False, result_id="void_ingot")

    # components: chain, keep <= 9 ingredients
    shapeless("void_component_1k", [
        INGOT, INGOT, INGOT,
        {"item": "minecraft:redstone_block"},
        {"item": "minecraft:ender_pearl"},
        INGOT, INGOT, INGOT,
    ], 1, condition=False)
    for i, (key, *_rest) in enumerate(TIERS):
        if i == 0:
            continue
        prev = {"item": "voidgen:void_component_" + TIERS[i - 1][0]}
        extra = TIERS[i][4]
        ingredients = [prev, {"item": "minecraft:redstone_block"}]
        ingredients.extend([INGOT_BLOCK] * max(0, extra - 1))
        ingredients.extend([INGOT] * 1)
        shapeless("void_component_" + key, ingredients, 1, condition=False)

    # housings + disks
    shaped("void_cell_housing", ["aba", "b b", "cdc"], {
        "a": {"item": "minecraft:glass"},
        "b": INGOT,
        "c": {"item": "minecraft:iron_ingot"},
        "d": {"item": "minecraft:copper_ingot"},
    }, 1, condition=False)
    for key, *_ in TIERS:
        shapeless("void_cell_" + key, [
            {"item": "voidgen:void_cell_housing"},
            {"item": "voidgen:void_component_" + key},
        ] + disk_extras(key), 1)

    # lang
    en, zh = {}, {}
    en["item.voidgen.void_ingot"] = "Void Ingot"
    en["item.voidgen.void_ingot_block"] = "Void Ingot Block"
    en["item.voidgen.void_cell_housing"] = "Void Cell Housing"
    en["tooltip.voidgen.void_ingot"] = "Condensed nothingness; used for AE2-style void disks."
    en["tooltip.voidgen.void_ingot_block"] = "Nine void ingots compressed into one block."
    en["tooltip.voidgen.void_cell_housing"] = "Shell for a void disk; combine with a component and ingots."
    zh["item.voidgen.void_ingot"] = "虚无锭"
    zh["item.voidgen.void_ingot_block"] = "虚无锭块"
    zh["item.voidgen.void_cell_housing"] = "虚无磁盘外壳"
    zh["tooltip.voidgen.void_ingot"] = "凝聚的虚无，用于合成 AE2 风格的虚无磁盘。"
    zh["tooltip.voidgen.void_ingot_block"] = "9 个虚无锭压成的方块，方便合成高级磁盘。"
    zh["tooltip.voidgen.void_cell_housing"] = "虚无磁盘的外壳，和元件、锭一起合成磁盘。"
    for key, label, *_ in TIERS:
        en["item.voidgen.void_component_" + key] = "Void Component " + label
        zh["item.voidgen.void_component_" + key] = "虚无元件 " + label
        en["item.voidgen.void_cell_" + key] = "Void Disk " + label
        zh["item.voidgen.void_cell_" + key] = "虚无磁盘 " + label
    en.pop("item.voidgen.void_component", None)
    en.pop("tooltip.voidgen.void_component", None)
    zh.pop("item.voidgen.void_component", None)
    zh.pop("tooltip.voidgen.void_component", None)

    existing_en = {}
    existing_zh = {}
    en_path = os.path.join(LANG, "en_us.json")
    zh_path = os.path.join(LANG, "zh_cn.json")
    if os.path.exists(en_path):
        with open(en_path, encoding="utf-8") as fh:
            existing_en = json.load(fh)
    if os.path.exists(zh_path):
        with open(zh_path, encoding="utf-8") as fh:
            existing_zh = json.load(fh)
    existing_en.update(en)
    existing_zh.update(zh)
    write_json(en_path, existing_en)
    write_json(zh_path, existing_zh)

    print("models 23, recipes 23, lang", len(existing_en), "/", len(existing_zh))


if __name__ == "__main__":
    main()
