"""Voidgen v2.0 asset pass: nothingness storages, collectors, distributor, mob spawner.

Adds resources on top of the v1.x generator/furnace assets. Run with the bundled Python.
"""
import json
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", "voidgen")
DATA = os.path.join(RES, "data")
MODID = "voidgen"
VERSION = "2.0.0"

# palette (AE-style dark panels)
FRAME = (40, 46, 54, 255)
FRAME_LIGHT = (64, 72, 82, 255)
FRAME_DARK = (24, 28, 33, 255)
PLATE = (28, 32, 38, 255)
PLATE_DARK = (20, 24, 29, 255)
INSET = (14, 16, 20, 255)
SLIT = (10, 12, 15, 255)
CYAN = (52, 211, 207, 255)
CYAN_LIGHT = (172, 252, 247, 255)
PURPLE = (168, 88, 226, 255)
PURPLE_DEEP = (92, 40, 138, 255)

TIERS = {
    1: {"name": "iron", "color": (150, 162, 176), "rate": 20},
    2: {"name": "gold", "color": (238, 198, 84), "rate": 40},
    3: {"name": "diamond", "color": (90, 214, 222), "rate": 80},
    4: {"name": "emerald", "color": (86, 208, 122), "rate": 160},
    5: {"name": "nether", "color": (190, 112, 236), "rate": 320},
}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)


def save_texture(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def new_image():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def bevel(d, color):
    d.rectangle([0, 0, 15, 15], outline=FRAME_DARK, fill=FRAME)
    d.line([1, 1, 14, 1], fill=FRAME_LIGHT)
    d.line([1, 1, 1, 14], fill=FRAME_LIGHT)
    d.line([1, 14, 14, 14], fill=FRAME_DARK)
    d.line([14, 1, 14, 14], fill=FRAME_DARK)
    d.rectangle([2, 2, 13, 13], outline=PLATE_DARK, fill=PLATE)
    d.rectangle([3, 3, 12, 12], fill=INSET)
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)):
        d.point((x, y), fill=color)


def collector_tex(tier):
    img = new_image()
    d = ImageDraw.Draw(img)
    color = TIERS[tier]["color"] + (255,)
    bevel(d, FRAME_LIGHT)
    # core
    d.rectangle([5, 5, 10, 10], outline=color, fill=PLATE_DARK)
    d.rectangle([7, 7, 8, 8], fill=CYAN_LIGHT if tier < 5 else PURPLE)
    # vents
    for y in (4, 11):
        d.line([4, y, 11, y], fill=SLIT)
    for x in (4, 11):
        d.line([x, 4, x, 11], fill=SLIT)
    if tier >= 2:
        d.point((4, 8), fill=color)
        d.point((11, 8), fill=color)
    if tier >= 4:
        d.rectangle([6, 6, 9, 9], outline=color)
    return img


def distributor_tex():
    img = new_image()
    d = ImageDraw.Draw(img)
    bevel(d, PURPLE)
    d.rectangle([5, 5, 10, 10], outline=PURPLE, fill=PLATE_DARK)
    d.rectangle([7, 7, 8, 8], fill=PURPLE_DEEP)
    d.rectangle([4, 4, 11, 11], outline=PURPLE_DEEP)
    # arrows out
    d.line([8, 2, 8, 4], fill=PURPLE)
    d.line([8, 11, 8, 13], fill=PURPLE)
    d.line([2, 8, 4, 8], fill=PURPLE)
    d.line([11, 8, 13, 8], fill=PURPLE)
    return img


def storage_tex(tier, filled=False):
    img = new_image()
    d = ImageDraw.Draw(img)
    color = TIERS[tier]["color"] + (255,)
    d.rectangle([2, 4, 13, 13], outline=FRAME_DARK, fill=FRAME)
    d.rectangle([3, 5, 12, 12], outline=PLATE_DARK, fill=PLATE)
    d.rectangle([4, 7, 11, 10], fill=INSET)
    if filled:
        d.rectangle([5, 8, 10, 9], fill=CYAN_LIGHT)
        d.rectangle([6, 6, 9, 11], fill=color)
        d.point((7, 7), fill=(255, 255, 255, 255))
        d.point((8, 8), fill=(255, 255, 255, 255))
    else:
        level = 8 - tier + 2
        d.rectangle([5, 8, 4 + level, 9], fill=color)
    d.line([6, 5, 9, 5], fill=color)
    d.point((3, 5), fill=FRAME_LIGHT)
    d.point((12, 12), fill=FRAME_LIGHT)
    return img


def mob_spawner_tex():
    img = new_image()
    d = ImageDraw.Draw(img)
    d.rectangle([3, 3, 12, 12], outline=FRAME_DARK, fill=FRAME)
    d.ellipse([5, 4, 10, 9], fill=(18, 16, 24, 255))
    d.ellipse([5, 6, 10, 12], fill=(26, 22, 34, 255))
    d.rectangle([7, 7, 8, 8], fill=CYAN_LIGHT)
    d.point((6, 5), fill=PURPLE)
    d.point((9, 5), fill=PURPLE)
    d.line([6, 10, 9, 10], fill=SLIT)
    return img


def cube_json(texture):
    return {"parent": "minecraft:block/cube_all", "textures": {"all": texture}}


def main():
    # ---- blocks: collectors + distributor ----
    for tier, info in TIERS.items():
        name = f"nothing_collector_{tier}"
        model = f"{MODID}:block/{name}"
        write_json(os.path.join(ASSETS, "blockstates", name + ".json"),
                   {"variants": {"": {"model": model}}})
        write_json(os.path.join(ASSETS, "models", "block", name + ".json"), cube_json(f"{MODID}:block/{name}"))
        write_json(os.path.join(ASSETS, "models", "item", name + ".json"), {"parent": model})
        save_texture(os.path.join(ASSETS, "textures", "block", name + ".png"), collector_tex(tier))
        write_json(os.path.join(DATA, MODID, "loot_table", "blocks", name + ".json"), {
            "type": "minecraft:block",
            "pools": [{
                "bonus_rolls": 0.0, "rolls": 1.0,
                "entries": [{
                    "type": "minecraft:item", "name": f"{MODID}:{name}",
                    "conditions": [{"condition": "minecraft:survives_explosion"}],
                }],
            }],
            "random_sequence": f"{MODID}:blocks/{name}",
        })

    name = "nothing_distributor"
    write_json(os.path.join(ASSETS, "blockstates", name + ".json"),
               {"variants": {"": {"model": f"{MODID}:block/{name}"}}})
    write_json(os.path.join(ASSETS, "models", "block", name + ".json"), cube_json(f"{MODID}:block/{name}"))
    write_json(os.path.join(ASSETS, "models", "item", name + ".json"), {"parent": f"{MODID}:block/{name}"})
    save_texture(os.path.join(ASSETS, "textures", "block", name + ".png"), distributor_tex())
    write_json(os.path.join(DATA, MODID, "loot_table", "blocks", name + ".json"), {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0, "rolls": 1.0,
            "entries": [{
                "type": "minecraft:item", "name": f"{MODID}:{name}",
                "conditions": [{"condition": "minecraft:survives_explosion"}],
            }],
        }],
        "random_sequence": f"{MODID}:blocks/{name}",
    })

    # ---- items: storages, filled, mob spawner ----
    storage_models = {}
    for tier, info in TIERS.items():
        storage = f"void_storage_{info['name']}"
        write_json(os.path.join(ASSETS, "models", "item", storage + ".json"),
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{storage}"}})
        save_texture(os.path.join(ASSETS, "textures", "item", storage + ".png"), storage_tex(tier))
        storage_models[info["name"]] = storage
        if tier < 5:
            filled = f"filled_void_storage_{info['name']}"
            write_json(os.path.join(ASSETS, "models", "item", filled + ".json"),
                       {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{filled}"}})
            save_texture(os.path.join(ASSETS, "textures", "item", filled + ".png"), storage_tex(tier, filled=True))

    mob = "mob_spawner"
    write_json(os.path.join(ASSETS, "models", "item", mob + ".json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{mob}"}})
    save_texture(os.path.join(ASSETS, "textures", "item", mob + ".png"), mob_spawner_tex())

    # ---- recipes ----
    recipes = {
        "void_storage_iron": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:iron_block"}, {"item": "minecraft:redstone_block"}, {"item": "minecraft:ender_pearl"}],
            "result": {"count": 1, "id": f"{MODID}:void_storage_iron"}},
        "void_storage_gold": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:gold_block"}, {"item": f"{MODID}:void_storage_iron"}, {"item": "minecraft:redstone"}],
            "result": {"count": 1, "id": f"{MODID}:void_storage_gold"}},
        "void_storage_diamond": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:diamond_block"}, {"item": f"{MODID}:void_storage_gold"}, {"item": "minecraft:redstone"}],
            "result": {"count": 1, "id": f"{MODID}:void_storage_diamond"}},
        "void_storage_emerald": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:emerald_block"}, {"item": f"{MODID}:void_storage_diamond"}, {"item": "minecraft:redstone"}],
            "result": {"count": 1, "id": f"{MODID}:void_storage_emerald"}},
        "void_storage_nether": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:nether_star"}, {"item": f"{MODID}:void_storage_emerald"}, {"item": "minecraft:obsidian"}],
            "result": {"count": 1, "id": f"{MODID}:void_storage_nether"}},
        "nothing_collector_1": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": f"{MODID}:filled_void_storage_iron"}, {"item": "minecraft:iron_block"}, {"item": "minecraft:redstone_block"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_collector_1"}},
        "nothing_collector_2": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": f"{MODID}:filled_void_storage_gold"}, {"item": f"{MODID}:nothing_collector_1"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_collector_2"}},
        "nothing_collector_3": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": f"{MODID}:filled_void_storage_diamond"}, {"item": f"{MODID}:nothing_collector_2"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_collector_3"}},
        "nothing_collector_4": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": f"{MODID}:filled_void_storage_emerald"}, {"item": f"{MODID}:nothing_collector_3"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_collector_4"}},
        "nothing_collector_5": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": f"{MODID}:void_storage_nether"}, {"item": f"{MODID}:nothing_collector_4"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_collector_5"}},
        "nothing_distributor": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:iron_block"}, {"item": "minecraft:ender_pearl"}, {"item": "minecraft:redstone_block"}, {"item": "minecraft:amethyst_shard"}],
            "result": {"count": 1, "id": f"{MODID}:nothing_distributor"}},
        "mob_spawner": {"type": "minecraft:crafting_shapeless", "category": "misc", "ingredients": [
            {"item": "minecraft:ender_pearl"}, {"item": "minecraft:diamond"}, {"item": "minecraft:gold_ingot"}, {"item": "minecraft:redstone_block"}],
            "result": {"count": 1, "id": f"{MODID}:mob_spawner"}},
    }
    for name, recipe in recipes.items():
        write_json(os.path.join(DATA, MODID, "recipe", name + ".json"), recipe)

    # ---- pickaxe tag: add the new blocks ----
    tag_path = os.path.join(DATA, "minecraft", "tags", "block", "mineable", "pickaxe.json")
    tag = {"replace": False, "values": []}
    if os.path.exists(tag_path):
        with open(tag_path, encoding="utf-8") as fh:
            tag = json.load(fh)
    for name in ["nothing_collector_1", "nothing_collector_2", "nothing_collector_3",
                 "nothing_collector_4", "nothing_collector_5", "nothing_distributor"]:
        entry = f"{MODID}:{name}"
        if entry not in tag["values"]:
            tag["values"].append(entry)
    write_json(tag_path, tag)

    # ---- language files ----
    en_path = os.path.join(ASSETS, "lang", "en_us.json")
    zh_path = os.path.join(ASSETS, "lang", "zh_cn.json")
    en = {}
    zh = {}
    if os.path.exists(en_path):
        with open(en_path, encoding="utf-8") as fh:
            en = json.load(fh)
    if os.path.exists(zh_path):
        with open(zh_path, encoding="utf-8") as fh:
            zh = json.load(fh)

    en.update({
        "itemGroup.voidgen": "Voidgen �?Nothingness",
        "block.voidgen.void_generator": "Nothingness Generator",
        "block.voidgen.void_furnace": "Nothingness Furnace",
        "block.voidgen.nothing_distributor": "Nothingness Distributor",
        "item.voidgen.void_storage_iron": "Void Storage (Iron)",
        "item.voidgen.void_storage_gold": "Void Storage (Gold)",
        "item.voidgen.void_storage_diamond": "Void Storage (Diamond)",
        "item.voidgen.void_storage_emerald": "Void Storage (Emerald)",
        "item.voidgen.void_storage_nether": "Void Storage (Nether Star)",
        "item.voidgen.filled_void_storage_iron": "Filled Void Storage (Iron)",
        "item.voidgen.filled_void_storage_gold": "Filled Void Storage (Gold)",
        "item.voidgen.filled_void_storage_diamond": "Filled Void Storage (Diamond)",
        "item.voidgen.filled_void_storage_emerald": "Filled Void Storage (Emerald)",
        "item.voidgen.mob_spawner": "Void Mob Spawner",
        "tooltip.voidgen.store": "Stored: %s / %s",
        "tooltip.voidgen.store.infinite": "Unlimited capacity",
        "tooltip.voidgen.store.full": "Full �?right-click the collector to fill it",
        "tooltip.voidgen.collector": "Collects %s void/tick, 16 storage slots",
        "tooltip.voidgen.distributor": "Pulls from an adjacent collector and feeds nearby machines",
        "tooltip.voidgen.mob_spawner.controls": "Shift+right-click: pick a mob\nShift+right-click distributor: bind\nRight-click: spawn",
        "gui.voidgen.collector_rate": "Collection: %s void/tick",
        "gui.voidgen.collector_buffer": "Buffer: %s / %s",
        "gui.voidgen.collector_bypass": "Overflow absorbed by storages",
        "gui.voidgen.collector_tier": "Tier: %s",
        "gui.voidgen.spawner_page": "Page %s/%s",
        "gui.voidgen.spawner_cost": "Cost: %s void",
        "gui.voidgen.spawner_click": "Click to select",
        "status.voidgen.void_drop": "+%s void",
        "status.voidgen.void_drop_full": "No void storage in your inventory",
        "status.voidgen.spawner_bound": "Bound distributor: %s",
        "status.voidgen.spawner_no_mob": "Pick a mob first (Shift+right-click)",
        "status.voidgen.spawner_blocked": "No room to spawn there",
        "status.voidgen.spawner_no_value": "Not enough void (%s)",
        "status.voidgen.spawner_failed": "This mob cannot be spawned",
        "status.voidgen.spawner_spawned": "Spawned %s (-%s void)",
        "status.voidgen.spawner_selected": "Selected %s",
    })
    for tier, info in TIERS.items():
        en[f"block.voidgen.nothing_collector_{tier}"] = f"Nothingness Collector {['I', 'II', 'III', 'IV', 'V'][tier - 1]}"

    zh.update({
        "itemGroup.voidgen": "虚无 · Voidgen",
        "block.voidgen.void_generator": "虚无发电�?,
        "block.voidgen.void_furnace": "虚无熔炉",
        "block.voidgen.nothing_distributor": "虚无发散�?,
        "item.voidgen.void_storage_iron": "虚无存储器（铁）",
        "item.voidgen.void_storage_gold": "虚无存储器（金）",
        "item.voidgen.void_storage_diamond": "虚无存储器（钻石�?,
        "item.voidgen.void_storage_emerald": "虚无存储器（绿宝石）",
        "item.voidgen.void_storage_nether": "虚无存储器（下界之星�?,
        "item.voidgen.filled_void_storage_iron": "充盈的虚无存储器（铁�?,
        "item.voidgen.filled_void_storage_gold": "充盈的虚无存储器（金�?,
        "item.voidgen.filled_void_storage_diamond": "充盈的虚无存储器（钻石）",
        "item.voidgen.filled_void_storage_emerald": "充盈的虚无存储器（绿宝石�?,
        "item.voidgen.mob_spawner": "虚无生物生成�?,
        "tooltip.voidgen.store": "存储�?s / %s",
        "tooltip.voidgen.store.infinite": "无限容量",
        "tooltip.voidgen.store.full": "已满——放进收集装置即可转成充盈形�?,
        "tooltip.voidgen.collector": "�?tick 收集 %s 虚无值，16 个存储器槽位",
        "tooltip.voidgen.distributor": "从相邻收集装置抽取虚无值，供给附近的机�?,
        "tooltip.voidgen.mob_spawner.controls": "Shift+右键：选择生物\nShift+右键发散器：绑定\n右键：生�?,
        "gui.voidgen.collector_rate": "收集速度�?s 虚无�?tick",
        "gui.voidgen.collector_buffer": "缓存�?s / %s",
        "gui.voidgen.collector_bypass": "溢出的虚无值由存储器吸�?,
        "gui.voidgen.collector_tier": "等级�?s",
        "gui.voidgen.spawner_page": "�?%s/%s �?,
        "gui.voidgen.spawner_cost": "消耗：%s 虚无�?,
        "gui.voidgen.spawner_click": "点击选择",
        "status.voidgen.void_drop": "+%s 虚无�?,
        "status.voidgen.void_drop_full": "背包里没有虚无存储器",
        "status.voidgen.spawner_bound": "已绑定发散器�?s",
        "status.voidgen.spawner_no_mob": "先选择一个生物（Shift+右键�?,
        "status.voidgen.spawner_blocked": "生成位置没有空间",
        "status.voidgen.spawner_no_value": "虚无值不足（需�?%s�?,
        "status.voidgen.spawner_failed": "该生物无法生�?,
        "status.voidgen.spawner_spawned": "已生�?%s�?%s 虚无值）",
        "status.voidgen.spawner_selected": "已选择 %s",
    })
    for tier, info in TIERS.items():
        zh[f"block.voidgen.nothing_collector_{tier}"] = f"虚无收集装置 {['I', 'II', 'III', 'IV', 'V'][tier - 1]}"

    write_json(en_path, en)
    write_json(zh_path, zh)

    # ---- mods.toml / pack.mcmeta ----
    toml = f'''modLoader="javafml"
loaderVersion="[4,)"
license="MIT"
[[mods]]
modId="{MODID}"
version="{VERSION}"
displayName="Voidgen �?Nothingness"
description=\'\'\'Nothingness generator, furnace, storages, collectors and a mob spawner. Optionally integrates with AE2 (ME Interface return + in-world grid).\'\'\'
authors="Voidgen"
[[dependencies.{MODID}]]
modId="neoforge"
type="required"
versionRange="[21.1.0,)"
ordering="NONE"
side="BOTH"
[[dependencies.{MODID}]]
modId="minecraft"
type="required"
versionRange="[1.21.1]"
ordering="NONE"
side="BOTH"
[[dependencies.{MODID}]]
modId="ae2"
type="optional"
versionRange="[19.0.0,)"
ordering="NONE"
side="BOTH"
'''
    with open(os.path.join(RES, "META-INF", "neoforge.mods.toml"), "w", encoding="utf-8") as fh:
        fh.write(toml)
    write_json(os.path.join(RES, "pack.mcmeta"), {"pack": {
        "pack_format": 34,
        "supported_formats": {"min_inclusive": 34, "max_inclusive": 48},
        "description": "Voidgen v2.0 resources (MC 1.21.1 / NeoForge 21.1)",
    }})

    print("DONE v2 assets: collectors/distributor/storages/spawner")


if __name__ == "__main__":
    main()
