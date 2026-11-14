import io, json, zipfile, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.0.jar"
with zipfile.ZipFile(jar) as z:
    names = set(z.namelist())
    print("entries:", len(names))
    print("version 2.3.0:", b'version="2.3.0"' in z.read("META-INF/neoforge.mods.toml"))
    need = [
        "assets/voidgen/blockstates/void_assembler.json",
        "assets/voidgen/models/block/void_assembler.json",
        "assets/voidgen/models/item/void_assembler.json",
        "assets/voidgen/textures/block/void_assembler.png",
        "assets/voidgen/textures/block/void_assembler.png.mcmeta",
        "data/voidgen/recipe/void_assembler.json",
        "data/voidgen/loot_table/blocks/void_assembler.json",
    ]
    for n in need:
        print(("OK  " if n in names else "MISS"), n)
    tag = json.loads(z.read("data/minecraft/tags/block/mineable/pickaxe.json"))
    print("tag has assembler:", "voidgen:void_assembler" in tag["values"])
    print("classes void_assembler:", [n for n in names if n.startswith("com/voidgen/ae/VoidAssembler")])
    leaks = [n for n in names if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))]
    print("leaks:", leaks[:5], "count", len(leaks))
    lang = zipfile.ZipFile(jar).read("assets/voidgen/lang/en_us.json")
    zh = zipfile.ZipFile(jar).read("assets/voidgen/lang/zh_cn.json")
    en = json.loads(lang); zn = json.loads(zh)
    print("lang keys en/zh:", len(en), len(zn))
    print("assembler keys:", en.get("block.voidgen.void_assembler"), "/", zn.get("block.voidgen.void_assembler"))
    meta = json.loads(z.read("assets/voidgen/textures/block/void_assembler.png.mcmeta"))
    print("mcmeta:", meta)