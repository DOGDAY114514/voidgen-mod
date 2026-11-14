import zipfile, json, io, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.0.5.jar"
print("size", os.path.getsize(jar))
with zipfile.ZipFile(jar) as z:
    print("entries", len(z.namelist()))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json").decode("utf-8"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json").decode("utf-8"))
    print("lang keys:", len(en), len(zh), "parity:", set(en) == set(zh))
    print("hint en:", json.dumps(en.get("gui.voidgen.spawner_hint"), ensure_ascii=True))
    print("hint zh:", json.dumps(zh.get("gui.voidgen.spawner_hint"), ensure_ascii=True))
    meta = z.read("META-INF/neoforge.mods.toml").decode("utf-8")
    print([l for l in meta.splitlines() if l.startswith(("version", "displayName"))])
    bad = [n for n in z.namelist() if n.startswith(("com/mojang/", "net/neoforged/", "io/netty/", "appeng/"))]
    print("leaks:", bad)