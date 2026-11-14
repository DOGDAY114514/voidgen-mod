"""Generate all Voidgen v2 mod resources (JSON + 16x16 pixel textures).

Run with the DSH bundled Python (has Pillow):
  C:\\Users\\Administrator\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe gen_assets.py
"""
import json
import os

from PIL import Image, ImageDraw

ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")

MODID = "voidgen"
VERSION = "1.6.0"
LOADER_VERSION = "[4,)"  # FML loader major for NeoForge 21.1.x

CARD_IDS = ["accel_card", "overclock_card", "capacity_card", "range_card"]


def write_json(rel_path, data):
    path = os.path.join(RES, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("json ", rel_path)


def write_text(rel_path, text):
    path = os.path.join(RES, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("text ", rel_path)


def save_texture(rel_path, img):
    path = os.path.join(RES, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print("png  ", rel_path)


# ---------------------------------------------------------------- mods.toml
MODS_TOML = f'''modLoader="javafml"
loaderVersion="{LOADER_VERSION}"
license="MIT"

[[mods]]
modId="{MODID}"
version="{VERSION}"
displayName="Voidgen — Void Generator & Furnace"
authors="Voidgen"
description="A free-FE generator and a free-smelting Void Furnace built for AE2 bases. Generator: shift-right-click an AE2-style panel with 12 upgrade-card slots, cards accelerate generation, multiply the buffer, extend wireless range to infinite, or overclock; the Binding Card is a player accessory that scopes wireless power to right-clicked machines. Furnace: 9 input + 9 output slots, 8192 items per slot, no fuel or FE, 64 items/tick base and up to 8192 with speed cards, spread evenly over all 9 slots; the Void Configurator cycles each face between input, output and disabled, and shift-right-click toggles wireless auto-output. The furnace also has an AE return toggle that feeds its output into nearby AE2 ME Interfaces (optional reflective AE2 19.x integration). Works standalone, and feeds AE2 energy acceptors directly."

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
write_text("META-INF/neoforge.mods.toml", MODS_TOML)

# ---------------------------------------------------------------- pack.mcmeta
write_json(
    "pack.mcmeta",
    {
        "pack": {
            "pack_format": 34,
            "supported_formats": {"min_inclusive": 34, "max_inclusive": 48},
            "description": "Voidgen v1.6 resources (MC 1.21.1 / NeoForge 21.1)",
        }
    },
)

# ---------------------------------------------------------------- blockstates / models
write_json("assets/voidgen/blockstates/void_generator.json", {"variants": {"": {"model": "voidgen:block/void_generator"}}})
write_json(
    "assets/voidgen/models/block/void_generator.json",
    {
        "parent": "minecraft:block/cube_bottom_top",
        "textures": {
            "top": "voidgen:block/void_generator_top",
            "bottom": "voidgen:block/void_generator_bottom",
            "side": "voidgen:block/void_generator_side",
        },
    },
)
write_json("assets/voidgen/models/item/void_generator.json", {"parent": "voidgen:block/void_generator"})
write_json("assets/voidgen/blockstates/void_furnace.json", {"variants": {"": {"model": "voidgen:block/void_furnace"}}})
write_json(
    "assets/voidgen/models/block/void_furnace.json",
    {
        "parent": "minecraft:block/cube_bottom_top",
        "textures": {
            "top": "voidgen:block/void_furnace_top",
            "bottom": "voidgen:block/void_furnace_bottom",
            "side": "voidgen:block/void_furnace_side",
        },
    },
)
write_json("assets/voidgen/models/item/void_furnace.json", {"parent": "voidgen:block/void_furnace"})
write_json(
    "assets/voidgen/models/item/void_configurator.json",
    {"parent": "minecraft:item/generated", "textures": {"layer0": "voidgen:item/void_configurator"}},
)
for tier in range(1, 6):
    write_json(
        f"assets/voidgen/models/item/nest_upgrade_{tier}.json",
        {"parent": "minecraft:item/generated", "textures": {"layer0": f"voidgen:item/nest_upgrade_{tier}"}},
    )
for card in CARD_IDS:
    write_json(
        f"assets/voidgen/models/item/{card}.json",
        {"parent": "minecraft:item/generated", "textures": {"layer0": f"voidgen:item/{card}"}},
    )
write_json(
    "assets/voidgen/models/item/binding_card.json",
    {"parent": "minecraft:item/generated", "textures": {"layer0": "voidgen:item/binding_card"}},
)

# ---------------------------------------------------------------- lang
EN = {
    "block.voidgen.void_generator": "Void Generator",
    "itemGroup.voidgen": "Voidgen",
    "item.voidgen.accel_card": "Acceleration Card",
    "item.voidgen.overclock_card": "Overclock Card",
    "item.voidgen.capacity_card": "Capacity Card",
    "item.voidgen.range_card": "Range Card",
    "item.voidgen.binding_card": "Binding Card",
    "tooltip.voidgen.void_generator": "Generates FE out of the void. Right-click with an upgrade card to socket it.",
    "tooltip.voidgen.void_generator.shift": "Shift + right-click to open the internal AE-style panel.",
    "tooltip.voidgen.nest_upgrade": "Nest Upgrade %s: install on the generator in order I-V.",
    "tooltip.voidgen.card.acceleration": "x2 generation and transfer per card (stacks to 12).",
    "tooltip.voidgen.card.overclock": "Doubles the per-tick generation/transfer actions (stacks).",
    "tooltip.voidgen.card.capacity": "x2 energy buffer per card (stacks).",
    "tooltip.voidgen.card.range": "x4 wireless range per card; 12 cards = infinite reach.",
    "tooltip.voidgen.binding_card": "Equip in the player accessory slot. With it equipped, empty-hand right-click machines to bind them for wireless power.",
    "tooltip.voidgen.binding_card.bind": "Empty-hand right-click machines to bind/unbind them.",
    "tooltip.voidgen.binding_card.auto": "Shift + scroll in the world toggles auto-connect.",
    "gui.voidgen.accessory": "Accessory: Binding Card",
    "gui.voidgen.rate": "Generation: %s FE/t",
    "gui.voidgen.energy": "Buffer: %s / %s FE",
    "gui.voidgen.range": "Wireless: %s",
    "gui.voidgen.tier": "Tier: %s / %s",
    "gui.voidgen.cards": "Upgrade cards (%s)",
    "gui.voidgen.ae": "AE output: %s",
    "gui.voidgen.ae_on": "ON",
    "gui.voidgen.ae_off": "OFF",
    "gui.voidgen.auto_on": "ON",
    "gui.voidgen.auto_off": "OFF",
    "gui.voidgen.bound": "Linked: %s",
    "gui.voidgen.finite": "%s blocks",
    "gui.voidgen.infinite": "infinite",
    "status.voidgen.void_generator": "Tier %s - %s FE/t - %s / %s FE - range %s",
    "status.voidgen.upgraded": "Upgraded to tier %s",
    "status.voidgen.upgrade_required": "Install nest upgrade tier %s first",
    "status.voidgen.card_inserted": "Card installed",
    "status.voidgen.slots_full": "No free card slot",
    "status.voidgen.equipped": "Binding card equipped",
    "status.voidgen.unequipped": "Binding card returned to your inventory",
    "status.voidgen.already_equipped": "A binding card is already equipped",
    "status.voidgen.no_card": "No binding card equipped",
    "status.voidgen.bound": "Machine bound for wireless power",
    "status.voidgen.unbound": "Binding removed",
    "status.voidgen.bound_full": "Binding list is full (512)",
    "status.voidgen.auto_enabled": "Auto-connect: ON",
    "status.voidgen.auto_disabled": "Auto-connect: OFF",
    "block.voidgen.void_furnace": "Void Furnace",
    "item.voidgen.void_furnace": "Void Furnace",
    "item.voidgen.void_configurator": "Void Configurator",
    "tooltip.voidgen.void_furnace": "Smelts out of the void: no fuel, no FE. 9 input + 9 output slots, 8192 items per slot.",
    "tooltip.voidgen.void_furnace.controls": "Right-click: internal panel. Shift + right-click with cards / nest upgrades to install them. AE return feeds only ME Interfaces attached to the furnace.",
    "tooltip.voidgen.void_configurator": "Configure furnace faces: right-click a face to cycle Input / Output / Disabled.",
    "tooltip.voidgen.void_configurator.shift": "Shift + right-click: toggle wireless auto-output.",
    "gui.voidgen.furnace_rate": "Rate: %s items/tick",
    "gui.voidgen.furnace_slot": "Per slot: %s · Speed cards: %s",
    "gui.voidgen.furnace_wireless": "Wireless output: %s",
    "gui.voidgen.furnace_wireless_on": "ON",
    "gui.voidgen.furnace_wireless_off": "OFF",
    "gui.voidgen.furnace_ae": "AE return: %s",
    "gui.voidgen.furnace_ae_on": "ON",
    "gui.voidgen.furnace_ae_off": "OFF",    "gui.voidgen.face.down": "Down",
    "gui.voidgen.face.up": "Up",
    "gui.voidgen.face.north": "North",
    "gui.voidgen.face.south": "South",
    "gui.voidgen.face.west": "West",
    "gui.voidgen.face.east": "East",
    "gui.voidgen.face_mode.input": "Input",
    "gui.voidgen.face_mode.output": "Output",
    "gui.voidgen.face_mode.disabled": "Disabled",
    "status.voidgen.furnace_upgraded": "Void Furnace upgraded to tier %s",
    "status.voidgen.furnace_upgrade_required": "Install nest upgrade tier %s first",
    "status.voidgen.furnace_cards_full": "No free card slot",
    "status.voidgen.furnace_status": "Tier %s · %s items/tick · %s per slot · wireless %s",
    "status.voidgen.furnace_face": "Face %s -> %s",
    "status.voidgen.furnace_wireless_on": "Wireless output: ON",
    "status.voidgen.furnace_wireless_off": "Wireless output: OFF",
    "status.voidgen.furnace_ae_on": "AE return: ON (attach an ME Interface to the furnace)",
    "status.voidgen.furnace_ae_off": "AE return: OFF",
}
ZH = {
    "block.voidgen.void_generator": "虚空发电机",
    "itemGroup.voidgen": "虚空工坊",
    "item.voidgen.accel_card": "加速卡",
    "item.voidgen.overclock_card": "超频卡",
    "item.voidgen.capacity_card": "容量卡",
    "item.voidgen.range_card": "范围卡",
    "item.voidgen.binding_card": "绑定卡",
    "tooltip.voidgen.void_generator": "凭空产生 FE。手持升级卡右击可插入卡槽。",
    "tooltip.voidgen.void_generator.shift": "Shift + 右击打开内部 AE 风格面板。",
    "tooltip.voidgen.nest_upgrade": "套娃升级 %s 阶：对发电机按 I→V 顺序安装。",
    "tooltip.voidgen.card.acceleration": "加速卡：每张使发电与传电 ×2（可叠放 12 张）。",
    "tooltip.voidgen.card.overclock": "超频卡：每张使每 tick 的发电/传电次数翻倍（可叠放）。",
    "tooltip.voidgen.card.capacity": "容量卡：每张使储能 ×2（可叠放）。",
    "tooltip.voidgen.card.range": "范围卡：每张使无线范围 ×4；插满 12 张后无限距离。",
    "tooltip.voidgen.binding_card": "饰品栏装备后，空手右击机器即可绑定/解绑无线传电。",
    "tooltip.voidgen.binding_card.bind": "空手右击机器：绑定/解绑该机器的无线供电。",
    "tooltip.voidgen.binding_card.auto": "世界中 Shift+滚轮：开关自动连接。",
    "gui.voidgen.accessory": "饰品栏：绑定卡",
    "gui.voidgen.rate": "发电: %s FE/t",
    "gui.voidgen.energy": "储能: %s / %s FE",
    "gui.voidgen.range": "无线范围: %s",
    "gui.voidgen.tier": "阶数: %s / %s",
    "gui.voidgen.cards": "升级卡槽 (%s)",
    "gui.voidgen.ae": "AE 输出: %s",
    "gui.voidgen.ae_on": "开",
    "gui.voidgen.ae_off": "关",
    "gui.voidgen.auto_on": "开",
    "gui.voidgen.auto_off": "关",
    "gui.voidgen.bound": "已绑定: %s",
    "gui.voidgen.finite": "%s 格",
    "gui.voidgen.infinite": "无限",
    "status.voidgen.void_generator": "阶数 %s · %s FE/t · %s / %s FE · 范围 %s",
    "status.voidgen.upgraded": "已升级到 %s 阶",
    "status.voidgen.upgrade_required": "请先安装套娃 %s 阶",
    "status.voidgen.card_inserted": "升级卡已安装",
    "status.voidgen.slots_full": "升级卡槽已满",
    "status.voidgen.equipped": "绑定卡已装备到饰品栏",
    "status.voidgen.unequipped": "绑定卡已放回背包",
    "status.voidgen.already_equipped": "饰品栏已经装备了绑定卡",
    "status.voidgen.no_card": "尚未装备绑定卡",
    "status.voidgen.bound": "机器已绑定无线供电",
    "status.voidgen.unbound": "已解除绑定",
    "status.voidgen.bound_full": "绑定列表已满（512）",
    "status.voidgen.auto_enabled": "自动连接：开",
    "status.voidgen.auto_disabled": "自动连接：关",
    "block.voidgen.void_furnace": "虚空熔炉",
    "item.voidgen.void_furnace": "虚空熔炉",
    "item.voidgen.void_configurator": "虚空配置器",
    "tooltip.voidgen.void_furnace": "凭空熔炼：不需要燃料、不需要 FE。9 输入槽 + 9 输出槽，每槽 8192 个。",
    "tooltip.voidgen.void_furnace.controls": "右击：打开内部面板。手持升级卡/套娃 Shift+右击可直接安装。AE 回传只喂贴着熔炉的 ME 接口。",
    "tooltip.voidgen.void_configurator": "调整熔炉各面：右击某一面切换 输入 / 输出 / 禁用。",
    "tooltip.voidgen.void_configurator.shift": "Shift + 右击：开关无线自动输出。",
    "gui.voidgen.furnace_rate": "速率: %s 件/刻",
    "gui.voidgen.furnace_slot": "单槽: %s · 加速卡: %s",
    "gui.voidgen.furnace_wireless": "无线输出: %s",
    "gui.voidgen.furnace_wireless_on": "开",
    "gui.voidgen.furnace_wireless_off": "关",
    "gui.voidgen.furnace_ae": "AE 回传: %s",
    "gui.voidgen.furnace_ae_on": "开",
    "gui.voidgen.furnace_ae_off": "关",
    "gui.voidgen.face.down": "下",
    "gui.voidgen.face.up": "上",
    "gui.voidgen.face.north": "北",
    "gui.voidgen.face.south": "南",
    "gui.voidgen.face.west": "西",
    "gui.voidgen.face.east": "东",
    "gui.voidgen.face_mode.input": "输入",
    "gui.voidgen.face_mode.output": "输出",
    "gui.voidgen.face_mode.disabled": "禁用",
    "status.voidgen.furnace_upgraded": "虚空熔炉已升级到 %s 阶",
    "status.voidgen.furnace_upgrade_required": "请先安装套娃 %s 阶",
    "status.voidgen.furnace_cards_full": "升级卡槽已满",
    "status.voidgen.furnace_status": "阶数 %s · %s 件/刻 · 单槽 %s · 无线 %s",
    "status.voidgen.furnace_face": "面 %s → %s",
    "status.voidgen.furnace_wireless_on": "无线输出：开",
    "status.voidgen.furnace_wireless_off": "无线输出：关",
    "status.voidgen.furnace_ae_on": "AE 回传：开（需把 ME 接口贴在熔炉上）",
    "status.voidgen.furnace_ae_off": "AE 回传：关",
}
for tier, roman in enumerate(["I", "II", "III", "IV", "V"], start=1):
    EN[f"item.voidgen.nest_upgrade_{tier}"] = f"Nest Upgrade {roman}"
    ZH[f"item.voidgen.nest_upgrade_{tier}"] = f"套娃升级 {roman}"
write_json("assets/voidgen/lang/en_us.json", EN)
write_json("assets/voidgen/lang/zh_cn.json", ZH)

# ---------------------------------------------------------------- recipes
write_json(
    "data/voidgen/recipe/void_generator.json",
    {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [
            {"item": "minecraft:iron_block"},
            {"item": "minecraft:furnace"},
            {"item": "minecraft:redstone_block"},
            {"item": "minecraft:redstone_block"},
        ],
        "result": {"count": 1, "id": "voidgen:void_generator"},
    },
)

# Each nest upgrade = the previous tier, doubled, plus one catalyst: proper matryoshka nesting.
NEST_CATALYSTS = {
    1: [{"item": "minecraft:redstone_block"}, {"item": "minecraft:redstone_block"}, {"item": "minecraft:gold_ingot"}],
    2: [{"item": "voidgen:nest_upgrade_1"}, {"item": "voidgen:nest_upgrade_1"}, {"item": "minecraft:gold_block"}],
    3: [{"item": "voidgen:nest_upgrade_2"}, {"item": "voidgen:nest_upgrade_2"}, {"item": "minecraft:diamond"}],
    4: [{"item": "voidgen:nest_upgrade_3"}, {"item": "voidgen:nest_upgrade_3"}, {"item": "minecraft:emerald_block"}],
    5: [{"item": "voidgen:nest_upgrade_4"}, {"item": "voidgen:nest_upgrade_4"}, {"item": "minecraft:nether_star"}],
}
for tier, ingredients in NEST_CATALYSTS.items():
    write_json(
        f"data/voidgen/recipe/nest_upgrade_{tier}.json",
        {
            "type": "minecraft:crafting_shapeless",
            "category": "misc",
            "ingredients": ingredients,
            "result": {"count": 1, "id": f"voidgen:nest_upgrade_{tier}"},
        },
    )

CARD_RECIPES = {
    "accel_card": ["voidgen:nest_upgrade_2", "minecraft:sugar", "minecraft:redstone_block"],
    "overclock_card": ["voidgen:nest_upgrade_2", "minecraft:clock", "minecraft:glowstone_dust"],
    "capacity_card": ["voidgen:nest_upgrade_2", "minecraft:chest", "minecraft:redstone_block"],
    "range_card": ["voidgen:nest_upgrade_3", "minecraft:ender_pearl", "minecraft:amethyst_shard"],
    "binding_card": ["voidgen:nest_upgrade_2", "minecraft:ender_pearl", "minecraft:gold_ingot", "minecraft:redstone"],
}
for card, ingredients in CARD_RECIPES.items():
    write_json(
        f"data/voidgen/recipe/{card}.json",
        {
            "type": "minecraft:crafting_shapeless",
            "category": "misc",
            "ingredients": [{"item": item} for item in ingredients],
            "result": {"count": 1, "id": f"voidgen:{card}"},
        },
    )

# ---------------------------------------------------------------- furnace recipes
write_json(
    "data/voidgen/recipe/void_furnace.json",
    {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "key": {
            "I": {"item": "minecraft:iron_block"},
            "F": {"item": "minecraft:furnace"},
            "R": {"item": "minecraft:redstone_block"},
        },
        "pattern": [
            "III",
            "IFI",
            "RRR",
        ],
        "result": {"count": 1, "id": "voidgen:void_furnace"},
    },
)
write_json(
    "data/voidgen/recipe/void_configurator.json",
    {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [
            {"item": "minecraft:gold_ingot"},
            {"item": "minecraft:ender_pearl"},
            {"item": "minecraft:redstone"},
            {"item": "minecraft:stick"},
        ],
        "result": {"count": 1, "id": "voidgen:void_configurator"},
    },
)

# ---------------------------------------------------------------- loot + tags
write_json(
    "data/voidgen/loot_table/blocks/void_generator.json",
    {
        "type": "minecraft:block",
        "pools": [
            {
                "bonus_rolls": 0.0,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": f"{MODID}:void_generator",
                        "conditions": [{"condition": "minecraft:survives_explosion"}],
                    }
                ],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{MODID}:blocks/void_generator",
    },
)
write_json(
    "data/voidgen/loot_table/blocks/void_furnace.json",
    {
        "type": "minecraft:block",
        "pools": [
            {
                "bonus_rolls": 0.0,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": f"{MODID}:void_furnace",
                        "conditions": [{"condition": "minecraft:survives_explosion"}],
                    }
                ],
                "rolls": 1.0,
            }
        ],
        "random_sequence": f"{MODID}:blocks/void_furnace",
    },
)
write_json("data/minecraft/tags/block/mineable/pickaxe.json",
           {"replace": False, "values": [f"{MODID}:void_generator", f"{MODID}:void_furnace"]})


# ---------------------------------------------------------------- textures
def new_img():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


# AE2-inspired modern palette: graphite plates, crisp bevels, cyan energy glow.
BG_OUTLINE = (9, 11, 14, 255)
FRAME = (40, 46, 54, 255)
FRAME_LIGHT = (64, 72, 82, 255)
FRAME_DARK = (24, 28, 33, 255)
PLATE = (28, 32, 38, 255)
PLATE_LIGHT = (34, 39, 46, 255)
PLATE_DARK = (20, 24, 29, 255)
INSET = (14, 16, 20, 255)
SLIT = (10, 12, 15, 255)
CYAN = (52, 211, 207, 255)
CYAN_LIGHT = (172, 252, 247, 255)
CYAN_DEEP = (20, 112, 114, 255)
BLUE = (77, 141, 255, 255)
SCREW = (126, 134, 144, 255)


def bevel_frame(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=FRAME)
    d.rectangle([x0, y0, x1, y0], fill=FRAME_LIGHT)
    d.rectangle([x0, y0, x0, y1], fill=FRAME_LIGHT)
    d.rectangle([x0, y1, x1, y1], fill=FRAME_DARK)
    d.rectangle([x1, y0, x1, y1], fill=FRAME_DARK)


def screws(d):
    for x, y in ((2, 2), (13, 2), (2, 13), (13, 13)):
        d.point((x, y), fill=SCREW)


def make_generator_top():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    d.rectangle([3, 3, 12, 3], fill=PLATE_LIGHT)
    screws(d)
    # circuit traces running from the frame into the core
    for x in (5, 10):
        d.point((x, 2), fill=CYAN_DEEP)
        d.point((x, 13), fill=CYAN_DEEP)
    for y in (5, 10):
        d.point((2, y), fill=CYAN_DEEP)
        d.point((13, y), fill=CYAN_DEEP)
    # concentric energy core: glowing ring with a bright center
    d.rectangle([4, 4, 11, 11], fill=INSET)
    d.rectangle([5, 5, 10, 10], outline=CYAN)
    d.rectangle([6, 6, 9, 9], fill=PLATE_DARK)
    d.rectangle([7, 7, 8, 8], fill=CYAN_LIGHT)
    return img


def make_generator_side():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    screws(d)
    # recessed vent panel with vertical fins
    d.rectangle([3, 4, 12, 10], fill=PLATE_DARK)
    for x in (5, 7, 9, 11):
        d.rectangle([x, 5, x, 9], fill=SLIT)
    # recessed power port with a small cyan indicator
    d.rectangle([4, 10, 11, 12], fill=INSET)
    d.rectangle([6, 11, 9, 11], fill=CYAN_DEEP)
    d.point((7, 11), fill=CYAN)
    d.point((8, 11), fill=CYAN)
    return img


def make_generator_bottom():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    d.rectangle([3, 3, 12, 3], fill=PLATE_LIGHT)
    screws(d)
    # central exhaust cross with a faint glow
    d.rectangle([7, 5, 8, 10], fill=INSET)
    d.rectangle([5, 7, 10, 8], fill=INSET)
    d.point((7, 7), fill=CYAN_DEEP)
    d.point((8, 8), fill=CYAN_DEEP)
    for x, y in ((4, 4), (11, 4), (4, 11), (11, 11)):
        d.point((x, y), fill=FRAME_DARK)
    return img


def make_card(base, dark, accent, icon):
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=(12, 12, 16, 255))
    d.rectangle([1, 1, 14, 14], fill=base + (255,))
    d.rectangle([1, 1, 14, 2], fill=accent + (255,))
    d.rectangle([1, 13, 14, 14], fill=dark + (255,))
    d.rectangle([2, 3, 13, 12], fill=dark + (255,))
    icon(d, accent)
    d.point((2, 2), fill=(210, 214, 226, 255))
    d.point((13, 2), fill=(210, 214, 226, 255))
    d.point((2, 13), fill=(210, 214, 226, 255))
    d.point((13, 13), fill=(210, 214, 226, 255))
    return img


def icon_accel(d, accent):
    d.polygon([(8, 4), (11, 8), (9, 8), (9, 11), (7, 11), (7, 8), (5, 8)], fill=accent + (255,))


def icon_overclock(d, accent):
    d.polygon([(9, 4), (6, 9), (8, 9), (7, 12), (11, 7), (9, 7)], fill=accent + (255,))


def icon_capacity(d, accent):
    d.rectangle([5, 5, 10, 11], outline=accent + (255,), width=1)
    d.rectangle([7, 3, 8, 4], fill=accent + (255,))
    d.rectangle([7, 7, 8, 9], fill=accent + (255,))


def icon_range(d, accent):
    d.ellipse([4, 4, 11, 11], outline=accent + (255,))
    d.ellipse([6, 6, 9, 9], outline=accent + (255,))
    d.point((8, 8), fill=accent + (255,))


def icon_bind(d, accent):
    # two interlocked chain links
    d.ellipse([3, 5, 8, 11], outline=accent + (255,))
    d.ellipse([7, 5, 12, 11], outline=accent + (255,))
    d.point((7, 8), fill=accent + (255,))
    d.point((8, 8), fill=accent + (255,))


def make_furnace_top():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    d.rectangle([3, 3, 12, 3], fill=PLATE_LIGHT)
    screws(d)
    # furnace mouth: recessed opening with a cyan heat bed
    d.rectangle([4, 5, 11, 12], fill=INSET)
    d.rectangle([5, 6, 10, 10], fill=SLIT)
    d.rectangle([5, 8, 10, 10], fill=CYAN_DEEP)
    for x in (6, 8, 9):
        d.point((x, 9), fill=CYAN)
    d.point((7, 8), fill=CYAN_LIGHT)
    d.point((10, 8), fill=CYAN)
    return img


def make_furnace_side():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    screws(d)
    # vertical vent fins
    d.rectangle([3, 4, 12, 10], fill=PLATE_DARK)
    for x in (5, 7, 9, 11):
        d.rectangle([x, 5, x, 9], fill=SLIT)
    # power feed rail with a small indicator
    d.rectangle([4, 10, 11, 12], fill=INSET)
    d.rectangle([6, 11, 9, 11], fill=CYAN_DEEP)
    d.point((7, 11), fill=CYAN)
    d.point((8, 11), fill=CYAN)
    return img


def make_furnace_bottom():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 15, 15], fill=BG_OUTLINE)
    bevel_frame(d, 1, 1, 14, 14)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    d.rectangle([3, 3, 12, 3], fill=PLATE_LIGHT)
    screws(d)
    # exhaust cross with a faint glow
    d.rectangle([7, 5, 8, 10], fill=INSET)
    d.rectangle([5, 7, 10, 8], fill=INSET)
    d.point((7, 7), fill=CYAN_DEEP)
    d.point((8, 8), fill=CYAN_DEEP)
    for x, y in ((4, 4), (11, 4), (4, 11), (11, 11)):
        d.point((x, y), fill=FRAME_DARK)
    return img


def make_configurator():
    img = new_img()
    d = ImageDraw.Draw(img)
    d.rectangle([1, 1, 14, 14], fill=(12, 12, 16, 255))
    d.rectangle([2, 2, 13, 13], fill=FRAME)
    d.rectangle([3, 3, 12, 12], fill=PLATE)
    d.rectangle([3, 3, 12, 3], fill=PLATE_LIGHT)
    # selector dial
    d.ellipse([5, 4, 10, 9], outline=CYAN)
    d.point((7, 6), fill=CYAN_LIGHT)
    d.point((8, 6), fill=CYAN_LIGHT)
    # face arrows
    d.point((4, 10), fill=CYAN_DEEP)
    d.point((11, 10), fill=CYAN_DEEP)
    d.rectangle([7, 11, 8, 12], fill=CYAN_DEEP)
    return img


save_texture("assets/voidgen/textures/block/void_generator_top.png", make_generator_top())
save_texture("assets/voidgen/textures/block/void_generator_side.png", make_generator_side())
save_texture("assets/voidgen/textures/block/void_generator_bottom.png", make_generator_bottom())
save_texture("assets/voidgen/textures/block/void_furnace_top.png", make_furnace_top())
save_texture("assets/voidgen/textures/block/void_furnace_side.png", make_furnace_side())
save_texture("assets/voidgen/textures/block/void_furnace_bottom.png", make_furnace_bottom())
save_texture("assets/voidgen/textures/item/void_configurator.png", make_configurator())

CARD_LOOKS = {
    "accel_card": ((16, 44, 46), (10, 28, 30), (63, 224, 208), icon_accel),
    "overclock_card": ((48, 18, 20), (30, 10, 12), (255, 90, 70), icon_overclock),
    "capacity_card": ((16, 42, 26), (9, 26, 16), (87, 227, 139), icon_capacity),
    "range_card": ((18, 30, 48), (10, 18, 30), (90, 168, 255), icon_range),
    "binding_card": ((46, 38, 16), (28, 22, 8), (255, 204, 92), icon_bind),
}
for card, (base, dark, accent, icon) in CARD_LOOKS.items():
    save_texture(f"assets/voidgen/textures/item/{card}.png", make_card(base, dark, accent, icon))

NEST_COLORS = {
    1: ((190, 48, 48), (110, 20, 20)),
    2: ((226, 116, 30), (140, 62, 12)),
    3: ((246, 198, 52), (156, 116, 16)),
    4: ((56, 186, 106), (18, 108, 56)),
    5: ((168, 68, 218), (82, 18, 122)),
}


def make_nest(tier):
    main, dark = NEST_COLORS[tier]
    light = tuple(min(255, c + 48) for c in main)
    face = (250, 226, 190, 255)
    img = new_img()
    d = ImageDraw.Draw(img)
    # head
    d.rectangle([5, 3, 10, 7], fill=main + (255,))
    d.line([5, 3, 10, 3], fill=dark + (255,))
    d.line([5, 3, 5, 7], fill=dark + (255,))
    d.line([10, 3, 10, 7], fill=dark + (255,))
    d.rectangle([6, 4, 9, 6], fill=face)
    d.point((6, 5), fill=(40, 30, 30, 255))
    d.point((9, 5), fill=(40, 30, 30, 255))
    d.point((7, 6), fill=(224, 150, 150, 255))
    d.point((8, 6), fill=(224, 150, 150, 255))
    d.point((6, 4), fill=(255, 240, 220, 255))
    # body
    d.rectangle([4, 8, 11, 14], fill=main + (255,))
    d.line([4, 8, 4, 14], fill=dark + (255,))
    d.line([11, 8, 11, 14], fill=dark + (255,))
    d.line([4, 14, 11, 14], fill=dark + (255,))
    d.rectangle([5, 8, 10, 8], fill=dark + (255,))
    d.line([5, 9, 5, 13], fill=light + (255,))
    d.rectangle([6, 9, 9, 11], fill=face)
    for i in range(tier):
        d.point((6 + i, 13), fill=(255, 244, 190, 255))
    return img


for tier in range(1, 6):
    save_texture(f"assets/voidgen/textures/item/nest_upgrade_{tier}.png", make_nest(tier))

print("DONE")
