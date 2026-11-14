import json, io
p = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\zh_cn.json"
raw = open(p, "rb").read()
print("BOM:", raw[:3] == b"\xef\xbb\xbf", "size", len(raw))
try:
    s = raw.decode("utf-8")
    print("utf8 ok")
except UnicodeDecodeError as e:
    print("NOT UTF8:", e)
    s = raw.decode("utf-8", "replace")
d = json.loads(s)
for k in ("item.voidgen.mob_spawner", "gui.voidgen.spawner_page", "gui.voidgen.spawner_cost", "gui.voidgen.spawner_click", "block.voidgen.nothing_collector_1"):
    print(json.dumps(k, ensure_ascii=True), "->", json.dumps(d.get(k), ensure_ascii=True)[:120])
print("replacement chars in file:", s.count("\ufffd"))