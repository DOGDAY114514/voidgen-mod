import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.6.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries:", len(names), "KB:", round(os.path.getsize(jar)/1024, 1))
    print("version 2.3.6:", b'version="2.3.6"' in z.read("META-INF/neoforge.mods.toml"))
    for n in names:
        if n.startswith("data/voidgen/recipe/processor_") and n.endswith(".json"):
            st = z.read(n)
            json.loads(st)
            print("recipe ok:", n, "ae2 cond:", b"neoforge:mod_loaded" in st)