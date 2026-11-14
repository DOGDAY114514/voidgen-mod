import json, zipfile, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.5.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang", len(en), len(zh), "parity", set(en) == set(zh))
    worst = 0
    for n in names:
        if n.startswith("data/voidgen/recipe/") and n.endswith(".json"):
            d = json.loads(z.read(n))
            ings = d.get("ingredients") or []
            if "key" in d:
                ings = [n2 for n2 in d.get("pattern", []) if n2.strip() != ""]
                ings = [k for row in d.get("pattern", []) for k in row if k != " "]
            worst = max(worst, len(ings))
    print("max ingredients in a recipe:", worst)
    items = set()
    for n in names:
        if n.startswith("assets/voidgen/models/item/"):
            items.add(os.path.basename(n)[:-5])
    comps = sorted(i for i in items if i.startswith("void_component_"))
    print("component models", len(comps))
    print("has void_ingot_block model", "void_ingot_block" in items)
    print("tex ingot block", "assets/voidgen/textures/item/void_ingot_block.png" in names)
    print("old void_component model", "assets/voidgen/models/item/void_component.json" in names)