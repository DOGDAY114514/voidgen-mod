import json, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.4.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    print("components", sum(1 for n in names if n.startswith("assets/voidgen/models/item/void_component_")),
          sum(1 for n in names if n.startswith("data/voidgen/recipe/void_component_")),
          sum(1 for n in names if n.startswith("assets/voidgen/textures/item/void_component_")))
    print("old void_component model left:", "assets/voidgen/models/item/void_component.json" in names)
    print("void_cell models", sum(1 for n in names if n.startswith("assets/voidgen/models/item/void_cell_") and "housing" not in n))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang", len(en), len(zh), "parity", set(en) == set(zh))
    r = json.loads(z.read("data/voidgen/recipe/void_cell_256m.json"))
    print("256m disk ingredients:", [i["item"] for i in r["ingredients"]])
    c = json.loads(z.read("data/voidgen/recipe/void_component_256m.json"))
    print("256m component ingredients:", [i["item"] for i in c["ingredients"]])