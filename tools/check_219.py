import json, zipfile, tomllib
p = r"D:\AI\voidgen-mod\dist\voidgen-2.1.9.jar"
z = zipfile.ZipFile(p)
names = z.namelist()
meta = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
mod = meta["mods"][0]
print("version", mod["version"], "deps", {k: v for k, v in (meta.get("dependencies") or {}).get("voidgen", {}).items()} if isinstance((meta.get("dependencies") or {}).get("voidgen"), dict) else "list")
en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang", len(en), len(zh), "parity", set(en) == set(zh))
print("card keys", [k for k in en if "binding_card" in k or "card_" in k][:20])
print("leaks", [n for n in names if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))])