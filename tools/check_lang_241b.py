import io, json
zh = json.load(io.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\zh_cn.json", encoding="utf-8"))
val = zh.get("block.voidgen.void_ingot_block")
print("zh equals expected:", val == "\u865a\u65e0\u952d\u5757")
print("zh codepoints:", [hex(ord(ch)) for ch in (val or "")])
en = json.load(io.open(r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\en_us.json", encoding="utf-8"))
print("en:", en.get("block.voidgen.void_ingot_block") == "Void Ingot Block")