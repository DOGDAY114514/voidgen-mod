import io, json
for loc in ("zh_cn", "en_us"):
    d = json.load(io.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\%s.json" % loc, encoding="utf-8"))
    print(loc, repr(d.get("block.voidgen.void_ingot_block")), "item key:", "item.voidgen.void_ingot_block" in d)