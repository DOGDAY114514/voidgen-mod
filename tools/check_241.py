import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.4.1.jar"
with zipfile.ZipFile(jar) as z:
    n = z.namelist()
    print("entries:", len(n), "KB:", round(os.path.getsize(jar)/1024,1))
    for key in ("assets/voidgen/blockstates/void_ingot_block.json",
                "assets/voidgen/models/block/void_ingot_block.json",
                "assets/voidgen/models/item/void_ingot_block.json",
                "assets/voidgen/textures/block/void_ingot_block.png",
                "data/voidgen/loot_table/blocks/void_ingot_block.json",
                "data/minecraft/tags/block/mineable/pickaxe.json"):
        print(key, "->", key in n)
    print("model:", z.read("assets/voidgen/models/item/void_ingot_block.json").decode())
    tag = json.loads(z.read("data/minecraft/tags/block/mineable/pickaxe.json"))
    print("tag has ingot block:", "voidgen:void_ingot_block" in tag["values"])
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("zh block key:", zh.get("block.voidgen.void_ingot_block"), "| item key:", zh.get("item.voidgen.void_ingot_block"))
    print("old item texture present:", "assets/voidgen/textures/item/void_ingot_block.png" in n)