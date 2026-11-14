import json, zipfile, tomllib
from collections import Counter
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.0.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    print("version 2.1.0", b'version="2.1.0"' in z.read("META-INF/neoforge.mods.toml"))
    print("AeCellItems", "com/voidgen/ae/AeCellItems.class" in names)
    print("void_cell_items", sum(1 for n in names if n.startswith("assets/voidgen/models/item/void_cell_")))
    print("void_cell_textures", sum(1 for n in names if n.startswith("assets/voidgen/textures/item/void_cell_")))
    print("void_cell_recipes", sum(1 for n in names if n.startswith("data/voidgen/recipe/void_cell_")))
    bad = [n for n in names if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))]
    print("leaks", bad[:5])
    ok = 0; cond = 0
    for n in names:
        if n.endswith(".json") and "/recipe/" in n:
            d = json.loads(z.read(n))
            ok += 1
            if n.startswith("data/voidgen/recipe/void_cell_") and d.get("neoforge:conditions"):
                cond += 1
    print("recipes", ok, "cell recipes with conditions", cond)
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang", len(en), len(zh), "parity", set(en) == set(zh))