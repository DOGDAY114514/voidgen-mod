import json, zipfile

jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.0.jar"
z = zipfile.ZipFile(jar)
names = z.namelist()
print("entries", len(names), "bytes", sum(i.file_size for i in z.infolist()))
bad = [n for n in names if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))]
print("leaks", bad[:5], "count", len(bad))
toml = z.read("META-INF/neoforge.mods.toml").decode("utf-8")
print("version 2.1.0:", 'version="2.1.0"' in toml)
classes = [n for n in names if n.startswith("com/voidgen/") and n.endswith(".class")]
print("classes", len(classes))
print("has AeCellItems:", "com/voidgen/ae/AeCellItems.class" in names)
models = [n for n in names if n.startswith("assets/voidgen/models/item/void_cell_")]
recipes = [n for n in names if n.startswith("data/voidgen/recipe/void_cell_")]
print("cell models", len(models), "cell recipes", len(recipes))
en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang", len(en), len(zh), "parity", set(en) == set(zh))
missing = [k for k in en if k.startswith(("item.voidgen.void_", "tooltip.voidgen.void")) and k not in zh]
print("missing zh:", missing)
tex = [n for n in names if n.startswith("assets/voidgen/textures/item/void_cell_")]
print("cell textures", len(tex))
r = json.loads(z.read("data/voidgen/recipe/void_cell_1k.json"))
print("1k recipe:", r.get("neoforge:conditions"), r["result"])