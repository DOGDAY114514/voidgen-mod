import json, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.5.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang", len(en), len(zh), "parity", set(en) == set(zh))
    comps = [n for n in names if n.startswith("assets/voidgen/models/item/void_component_") and n.endswith(".json")]
    disks = [n for n in names if n.startswith("assets/voidgen/models/item/void_cell_") and n.endswith(".json")]
    print("component models", len(comps), "disk models", len(disks))
    comps_rx = [n for n in names if n.startswith("data/voidgen/recipe/void_component_") and n.endswith(".json")]
    disks_rx = [n for n in names if n.startswith("data/voidgen/recipe/void_cell_") and n.endswith(".json")]
    print("component recipes", len(comps_rx), "disk recipes", len(disks_rx))
    worst = 0
    for n in names:
        if n.startswith("data/voidgen/recipe/") and n.endswith(".json"):
            d = json.loads(z.read(n))
            ing = d.get("ingredients") or []
            if "pattern" in d:
                ing = [k for row in d["pattern"] for k in row if k != " "]
            worst = max(worst, len(ing))
    print("max ingredients", worst)
    print("old component model", "assets/voidgen/models/item/void_component.json" in names)
    print("ingot block model", "assets/voidgen/models/item/void_ingot_block.json" in names)
    print("ingot block texture", "assets/voidgen/textures/item/void_ingot_block.png" in names)
    print("version toml", b'version="2.1.5"' in z.read("META-INF/neoforge.mods.toml"))