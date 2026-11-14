"""Validate the packaged Voidgen v1.4 jar (offline, static checks only)."""
import io
import json
import struct
import sys
import tomllib
import zipfile

from PIL import Image

JAR = r"D:\AI\voidgen-mod\dist\voidgen-1.6.0.jar"

CLASSES = [
    "com/voidgen/VoidGen.class",
    "com/voidgen/VoidStats.class",
    "com/voidgen/VoidPowerNetwork.class",
    "com/voidgen/VoidAccessory.class",
    "com/voidgen/VoidNet.class",
    "com/voidgen/AeReturn.class",
    "com/voidgen/AeBridge.class",
    "com/voidgen/GridHost.class",
    "com/voidgen/VoidNet$AccessoryActionPayload.class",
    "com/voidgen/VoidNet$SyncPayload.class",
    "com/voidgen/ae/FurnaceAeSupport.class",
    "com/voidgen/ae/FurnaceGridNode.class",
    "com/voidgen/block/VoidGeneratorBlock.class",
    "com/voidgen/block/VoidGeneratorBlockEntity.class",
    "com/voidgen/block/VoidGeneratorMenu.class",
    "com/voidgen/block/VoidFurnaceBlock.class",
    "com/voidgen/block/VoidFurnaceBlockEntity.class",
    "com/voidgen/block/VoidFurnaceBlockEntity$FaceMode.class",
    "com/voidgen/block/VoidFurnaceBlockEntity$SidedHandler.class",
    "com/voidgen/block/VoidFurnaceMenu.class",
    "com/voidgen/item/VoidGeneratorItem.class",
    "com/voidgen/item/NestUpgradeItem.class",
    "com/voidgen/item/UpgradeCardItem.class",
    "com/voidgen/item/BindingCardItem.class",
    "com/voidgen/item/VoidFurnaceItem.class",
    "com/voidgen/item/VoidConfiguratorItem.class",
    "com/voidgen/client/VoidGenClient.class",
    "com/voidgen/client/VoidGeneratorScreen.class",
    "com/voidgen/client/VoidFurnaceScreen.class",
]

CARDS = ["accel_card", "overclock_card", "capacity_card", "range_card"]

expected = {
    "META-INF/neoforge.mods.toml",
    "pack.mcmeta",
    "assets/voidgen/blockstates/void_generator.json",
    "assets/voidgen/blockstates/void_furnace.json",
    "assets/voidgen/models/block/void_generator.json",
    "assets/voidgen/models/block/void_furnace.json",
    "assets/voidgen/models/item/void_generator.json",
    "assets/voidgen/models/item/void_furnace.json",
    "assets/voidgen/models/item/void_configurator.json",
    "assets/voidgen/lang/en_us.json",
    "assets/voidgen/lang/zh_cn.json",
    "assets/voidgen/textures/block/void_generator_top.png",
    "assets/voidgen/textures/block/void_generator_side.png",
    "assets/voidgen/textures/block/void_generator_bottom.png",
    "assets/voidgen/textures/block/void_furnace_top.png",
    "assets/voidgen/textures/block/void_furnace_side.png",
    "assets/voidgen/textures/block/void_furnace_bottom.png",
    "assets/voidgen/textures/item/void_configurator.png",
    "data/voidgen/loot_table/blocks/void_generator.json",
    "data/voidgen/loot_table/blocks/void_furnace.json",
    "data/minecraft/tags/block/mineable/pickaxe.json",
    "data/voidgen/recipe/void_generator.json",
    "data/voidgen/recipe/void_furnace.json",
    "data/voidgen/recipe/void_configurator.json",
}
expected.update(CLASSES)
for i in range(1, 6):
    expected.add(f"assets/voidgen/models/item/nest_upgrade_{i}.json")
    expected.add(f"assets/voidgen/textures/item/nest_upgrade_{i}.png")
    expected.add(f"data/voidgen/recipe/nest_upgrade_{i}.json")
for card in CARDS:
    expected.add(f"assets/voidgen/models/item/{card}.json")
    expected.add(f"assets/voidgen/textures/item/{card}.png")
    expected.add(f"data/voidgen/recipe/{card}.json")

expected.add("assets/voidgen/models/item/binding_card.json")
expected.add("assets/voidgen/textures/item/binding_card.png")
expected.add("data/voidgen/recipe/binding_card.json")

errors = []
with zipfile.ZipFile(JAR) as z:
    names = set(z.namelist())
    missing = expected - names
    if missing:
        errors.append(f"missing entries: {sorted(missing)}")
    bad = [n for n in names if n.startswith(("com/mojang/", "net/neoforged/", "io/netty/"))]
    if bad:
        errors.append(f"stub classes leaked into jar: {bad}")

    meta = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
    mod = (meta.get("mods") or [{}])[0]
    print(f"mods.toml: modLoader={meta.get('modLoader')} loaderVersion={meta.get('loaderVersion')} modId={mod.get('modId')} version={mod.get('version')}")
    if meta.get("modLoader") != "javafml" or mod.get("modId") != "voidgen" or mod.get("version") != "1.6.0":
        errors.append("mods.toml basic fields wrong")
    deps = (meta.get("dependencies") or {}).get(mod.get("modId"), [])
    dep_ids = {d.get("modId"): d.get("type") for d in deps}
    print("dependencies:", dep_ids)
    if dep_ids.get("neoforge") != "required" or dep_ids.get("minecraft") != "required":
        errors.append("required dependencies missing")
    if dep_ids.get("ae2") not in (None, "optional"):
        errors.append("ae2 dependency should be optional if present")

    pack = json.loads(z.read("pack.mcmeta").decode("utf-8"))
    print("pack.mcmeta:", pack["pack"])

    json_count = 0
    for n in sorted(names):
        if n.endswith(".json"):
            try:
                json.loads(z.read(n).decode("utf-8"))
                json_count += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid JSON {n}: {exc}")
    print("JSON files parsed:", json_count)

    for n in names:
        if n.endswith(".png"):
            img = Image.open(io.BytesIO(z.read(n)))
            if img.size != (16, 16) or img.mode != "RGBA":
                errors.append(f"bad texture {n}: {img.size} {img.mode}")
    print("textures: 16x16 RGBA ok")

    recipes = [n for n in names if n.startswith("data/voidgen/recipe/") and n.endswith(".json")]
    print("recipes:", len(sorted(recipes)))
    if len(recipes) != 13:
        errors.append(f"expected 13 recipes, got {len(recipes)}")
    for n in recipes:
        r = json.loads(z.read(n).decode("utf-8"))
        if not r["result"]["id"].startswith("voidgen:"):
            errors.append(f"recipe {n} result not in mod namespace")

    tag = json.loads(z.read("data/minecraft/tags/block/mineable/pickaxe.json").decode("utf-8"))
    if tag["values"] != ["voidgen:void_generator", "voidgen:void_furnace"]:
        errors.append("pickaxe tag values wrong")

    en = json.loads(z.read("assets/voidgen/lang/en_us.json").decode("utf-8"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json").decode("utf-8"))
    if set(en) != set(zh):
        errors.append(f"lang key mismatch: {sorted(set(en) ^ set(zh))}")
    required = ["item.voidgen.accel_card", "item.voidgen.overclock_card", "item.voidgen.capacity_card", "item.voidgen.range_card",
                "item.voidgen.binding_card", "tooltip.voidgen.binding_card", "tooltip.voidgen.binding_card.bind",
                "tooltip.voidgen.binding_card.auto", "gui.voidgen.accessory", "gui.voidgen.auto_on", "gui.voidgen.auto_off",
                "gui.voidgen.bound",
                "gui.voidgen.rate", "gui.voidgen.energy", "gui.voidgen.range", "gui.voidgen.tier", "gui.voidgen.cards",
                "gui.voidgen.ae",
                "status.voidgen.void_generator", "status.voidgen.upgraded", "status.voidgen.equipped",
                "status.voidgen.unequipped", "status.voidgen.no_card", "status.voidgen.bound",
                "tooltip.voidgen.void_generator",
                "block.voidgen.void_furnace", "item.voidgen.void_configurator",
                "tooltip.voidgen.void_furnace", "tooltip.voidgen.void_configurator",
                "gui.voidgen.furnace_rate", "gui.voidgen.furnace_slot", "gui.voidgen.furnace_wireless",
                "gui.voidgen.furnace_ae", "status.voidgen.furnace_ae_on", "status.voidgen.furnace_ae_off",
                "gui.voidgen.face_mode.input", "gui.voidgen.face_mode.output", "gui.voidgen.face_mode.disabled",
                "status.voidgen.furnace_upgraded", "status.voidgen.furnace_upgrade_required",
                "status.voidgen.furnace_status", "status.voidgen.furnace_face"]
    for key in required:
        if key not in en:
            errors.append(f"en_us missing {key}")
    print("lang keys:", len(en), "parity ok")

    # annotation/method presence via constant pool search
    def class_bytes(name):
        return z.read(name)

    def major_version(data):
        return struct.unpack(">H", data[6:8])[0]

    main = class_bytes("com/voidgen/VoidGen.class")
    if major_version(main) != 65:
        errors.append(f"VoidGen major version {major_version(main)}")
    if b"Lnet/neoforged/fml/common/Mod;" not in main:
        errors.append("@Mod annotation missing in VoidGen")
    client = class_bytes("com/voidgen/client/VoidGenClient.class")
    if b"Lnet/neoforged/fml/common/EventBusSubscriber;" not in client:
        errors.append("@EventBusSubscriber missing in VoidGenClient")
    if b"AccessoryActionPayload" not in client or b"PacketDistributor" not in client:
        errors.append("client accessory networking missing")
    action = class_bytes("com/voidgen/VoidNet$AccessoryActionPayload.class")
    sync = class_bytes("com/voidgen/VoidNet$SyncPayload.class")
    if b"accessory_action" not in action or b"accessory_sync" not in sync:
        errors.append("payload ids missing in record classes")
    screen = class_bytes("com/voidgen/client/VoidGeneratorScreen.class")
    if b"handleInventoryButtonClick" not in screen:
        errors.append("screen does not call handleInventoryButtonClick")
    furnace_screen = class_bytes("com/voidgen/client/VoidFurnaceScreen.class")
    if b"handleInventoryButtonClick" not in furnace_screen:
        errors.append("furnace screen does not call handleInventoryButtonClick")
    if b"getItemHandler" not in main:
        errors.append("ItemHandler capability registration missing in VoidGen")
    menu = class_bytes("com/voidgen/block/VoidGeneratorMenu.class")
    if b"<init>" not in menu:
        errors.append("menu init missing")

if errors:
    print("FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("ALL CHECKS PASSED")
