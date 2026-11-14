import io, json, zipfile
from PIL import Image
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.2.0.jar"
z = zipfile.ZipFile(jar)
names = set(z.namelist())
need = [
 "com/voidgen/block/MeVoidSupplierBlock.class",
 "com/voidgen/block/MeVoidSupplierBlockEntity.class",
 "com/voidgen/item/VoidValueItem.class",
 "assets/voidgen/blockstates/me_void_supplier.json",
 "assets/voidgen/models/block/me_void_supplier.json",
 "assets/voidgen/models/item/me_void_supplier.json",
 "assets/voidgen/models/item/void_value.json",
 "assets/voidgen/textures/block/me_void_supplier.png",
 "assets/voidgen/textures/block/me_void_supplier.png.mcmeta",
 "assets/voidgen/textures/item/void_value.png",
 "data/voidgen/recipe/me_void_supplier.json",
 "data/voidgen/loot_table/blocks/me_void_supplier.json",
]
for n in need:
    print(("OK  " if n in names else "MISS"), n)
img = Image.open(io.BytesIO(z.read("assets/voidgen/textures/block/me_void_supplier.png")))
print("block texture", img.size, img.mode)
iv = Image.open(io.BytesIO(z.read("assets/voidgen/textures/item/void_value.png")))
print("void_value", iv.size, iv.mode)
en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang", len(en), len(zh), "supplier keys", all(k in en and k in zh for k in ["block.voidgen.me_void_supplier","item.voidgen.void_value","status.voidgen.supplier_mode"]))
tag = json.loads(z.read("data/minecraft/tags/block/mineable/pickaxe.json"))
print("tag has supplier:", "voidgen:me_void_supplier" in tag["values"])
toml = z.read("META-INF/neoforge.mods.toml").decode("utf-8")
print("version 2.2.0:", 'version="2.2.0"' in toml)
print("entries", len(names))