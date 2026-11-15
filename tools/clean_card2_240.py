import io, os, json
# remove unused import in generator BE
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\block\VoidGeneratorBlockEntity.java"
s = io.open(p, encoding="utf-8").read().replace("import com.voidgen.VoidAccessory;\n", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
# delete binding card recipe
rp = r"D:\AI\voidgen-mod\src\main\resources\data\voidgen\recipe\binding_card.json"
if os.path.exists(rp):
    os.remove(rp); print("deleted recipe binding_card")
# report lang keys mentioning card/accessory/auto/bound/equip
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang"
for loc in ("en_us", "zh_cn"):
    data = json.loads(io.open(os.path.join(base, loc + ".json"), encoding="utf-8").read())
    hits = [k for k in data if any(w in k for w in ("binding", "accessory", "auto_", "auto", "bound", "equip"))]
    print(loc, len(data), hits)
# guide screen references
gp = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\client\VoidGuideScreen.java"
if os.path.exists(gp):
    g = io.open(gp, encoding="utf-8").read()
    print("guide mentions card:", "binding" in g or "绑定" in g)