import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.4.0.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries:", len(names), "KB:", round(os.path.getsize(jar)/1024,1))
    print("version 2.4.0:", b'version="2.4.0"' in z.read("META-INF/neoforge.mods.toml"))
    print("binding card class:", [n for n in names if "BindingCard" in n or "VoidAccessory" in n])
    print("binding card item model/recipe:", [n for n in names if "binding_card" in n])
    for loc in ("en_us","zh_cn"):
        data = json.loads(z.read(f"assets/voidgen/lang/{loc}.json"))
        print(loc, "keys:", len(data), "card keys:", [k for k in data if "card" in k and "binding" in k])
    print("recipes:", len([n for n in names if n.startswith("data/voidgen/recipe/") and n.endswith(".json")]))
    print("ingot textures:", [n for n in names if "void_ingot" in n])
    print("chunkload in VoidPowerNetwork:", b"onChunkLoad" in z.read("com/voidgen/VoidPowerNetwork.class"))
    print("ChunkEvent referenced in VoidGen:", b"ChunkEvent" in z.read("com/voidgen/VoidGen.class"))