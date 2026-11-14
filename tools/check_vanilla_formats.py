import json
import zipfile

JAR = r"C:\Users\Administrator\.gradle\caches\neoformruntime\artifacts\minecraft_1.21.1_client.jar"
wanted = [
    "data/minecraft/recipe/stone.json",
    "data/minecraft/recipe/furnace.json",
    "data/minecraft/loot_table/blocks/stone.json",
    "data/minecraft/tags/block/mineable/pickaxe.json",
]
with zipfile.ZipFile(JAR) as z:
    names = set(z.namelist())
    for path in wanted:
        print("=====", path, "present:", path in names)
        if path in names:
            print(z.read(path).decode("utf-8"))
