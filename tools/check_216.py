import json, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.6.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    print("version 2.1.6", b'version="2.1.6"' in z.read("META-INF/neoforge.mods.toml"))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang", len(en), len(zh), set(en) == set(zh))
    comps = [n for n in names if n.startswith("assets/voidgen/textures/item/void_component_") and n.endswith(".png")]
    print("component textures", len(comps))
    print("sparkle check 4k", "assets/voidgen/textures/item/void_component_4k.png" in names)