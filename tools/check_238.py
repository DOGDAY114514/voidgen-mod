import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.8.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries:", len(names), "sizeKB:", round(os.path.getsize(jar)/1024, 1))
    print("version 2.3.8:", b'version="2.3.8"' in z.read("META-INF/neoforge.mods.toml"))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang:", len(en), len(zh), "parity:", set(en) == set(zh))
    print("guide class:", "com/voidgen/client/VoidGuideScreen.class" in names)
    data = z.read("com/voidgen/client/VoidGenClient.class")
    print("key id in client class:", b"key.voidgen.guide" in data, b"key.categories.voidgen" in data)
    print("guide title key:", "gui.voidgen.guide.title" in en, en["gui.voidgen.guide.title"])