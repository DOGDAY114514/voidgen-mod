"""Assets + recipes for the floating crystal family (v2.5.0)."""
import json
import os

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
MODID = "voidgen"


def write_json(rel, obj):
    path = os.path.join(RES, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def load_json(rel):
    path = os.path.join(RES, rel)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


BUDDING = ["damaged", "chipped", "flawed", "flawless"]

# ---- item models ----
for item in ("floating_crystal", "floating_crystal_dust"):
    write_json(f"assets/{MODID}/models/item/{item}.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MODID}:item/{item}"}})

# ---- budding blocks: blockstate + block model + item model ----
for key in BUDDING:
    block = f"floating_budding_{key}"
    write_json(f"assets/{MODID}/blockstates/{block}.json",
               {"variants": {"": {"model": f"{MODID}:block/{block}"}}})
    write_json(f"assets/{MODID}/models/block/{block}.json",
               {"parent": "minecraft:block/cube_all",
                "textures": {"all": f"{MODID}:block/{block}"}})
    write_json(f"assets/{MODID}/models/item/{block}.json",
               {"parent": f"{MODID}:block/{block}"})

# ---- loot tables: drop self ----
for key in BUDDING:
    block = f"floating_budding_{key}"
    write_json(f"data/{MODID}/loot_table/blocks/{block}.json", {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0,
            "rolls": 1.0,
            "entries": [{"type": "minecraft:item", "name": f"{MODID}:{block}"}],
            "conditions": [{"condition": "minecraft:survives_explosion"}],
        }],
        "random_sequence": f"{MODID}:blocks/{block}",
    })

# ---- pickaxe tag ----
tag_rel = "data/minecraft/tags/block/mineable/pickaxe.json"
tag = load_json(tag_rel)
values = tag.setdefault("values", [])
for key in BUDDING:
    entry = f"{MODID}:floating_budding_{key}"
    if entry not in values:
        values.append(entry)
write_json(tag_rel, tag)

# ---- lang ----
EN = {
    "item.voidgen.floating_crystal": "Floating Crystal",
    "item.voidgen.floating_crystal_dust": "Floating Crystal Dust",
    "block.voidgen.floating_budding_damaged": "Damaged Floating Crystal Budding Rock",
    "block.voidgen.floating_budding_chipped": "Chipped Floating Crystal Budding Rock",
    "block.voidgen.floating_budding_flawed": "Flawed Floating Crystal Budding Rock",
    "block.voidgen.floating_budding_flawless": "Flawless Floating Crystal Budding Rock",
    "tooltip.voidgen.floating_crystal": "Grows in water from certus quartz and floating dust.",
}
ZH = {
    "item.voidgen.floating_crystal": "虚浮水晶",
    "item.voidgen.floating_crystal_dust": "虚浮水晶粉",
    "block.voidgen.floating_budding_damaged": "损坏的虚浮水晶石英母岩",
    "block.voidgen.floating_budding_chipped": "开裂的虚浮水晶石英母岩",
    "block.voidgen.floating_budding_flawed": "有瑕的虚浮水晶石英母岩",
    "block.voidgen.floating_budding_flawless": "无瑕的虚浮水晶石英母岩",
    "tooltip.voidgen.floating_crystal": "将赛特斯石英与虚浮水晶粉投入水中，一段时间后生成。",
}
for lang, extra in (("en_us", EN), ("zh_cn", ZH)):
    rel = f"assets/{MODID}/lang/{lang}.json"
    data = load_json(rel)
    data.update(extra)
    write_json(rel, data)

# ---- recipes ----
COND = [{"type": "neoforge:mod_loaded", "modid": "advanced_ae"}]

void_ingot = {
    "neoforge:conditions": COND,
    "type": "advanced_ae:reaction",
    "input_energy": 400000,
    "input_fluid": {"amount": 500, "ingredient": {"fluid": "minecraft:water"}},
    "input_items": [
        {"amount": 32, "ingredient": {"item": f"{MODID}:floating_crystal_dust"}},
        {"amount": 32, "ingredient": {"tag": "c:ingots/copper"}},
        {"amount": 32, "ingredient": {"tag": "c:ingots/osmium"}},
    ],
    "output": {"#": 64, "#t": "ae2:i", "id": f"{MODID}:void_ingot"},
}
write_json(f"data/{MODID}/recipe/void_ingot.json", void_ingot)

floating_from_certus = {
    "neoforge:conditions": COND,
    "type": "advanced_ae:reaction",
    "input_energy": 200000,
    "input_fluid": {"amount": 1000, "ingredient": {"fluid": "minecraft:water"}},
    "input_items": [
        {"amount": 32, "ingredient": {"item": "ae2:certus_quartz_crystal"}},
        {"amount": 32, "ingredient": {"item": f"{MODID}:floating_crystal_dust"}},
    ],
    "output": {"#": 64, "#t": "ae2:i", "id": f"{MODID}:floating_crystal"},
}
write_json(f"data/{MODID}/recipe/floating_crystal_from_certus.json", floating_from_certus)

floating_from_charged = {
    "neoforge:conditions": COND,
    "type": "advanced_ae:reaction",
    "input_energy": 150000,
    "input_fluid": {"amount": 500, "ingredient": {"fluid": "minecraft:water"}},
    "input_items": [
        {"amount": 16, "ingredient": {"item": "ae2:charged_certus_quartz_crystal"}},
        {"amount": 16, "ingredient": {"item": "minecraft:redstone"}},
        {"amount": 16, "ingredient": {"item": "minecraft:coal"}},
    ],
    "output": {"#": 64, "#t": "ae2:i", "id": f"{MODID}:floating_crystal"},
}
write_json(f"data/{MODID}/recipe/floating_crystal_from_charged.json", floating_from_charged)

print("floating assets written")
