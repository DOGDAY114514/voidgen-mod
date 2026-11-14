import json, io
for lang in ("en_us", "zh_cn"):
    p = rf"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\{lang}.json"
    d = json.load(io.open(p, encoding="utf-8"))
    for k in ("gui.voidgen.spawner_page", "gui.voidgen.spawner_cost", "gui.voidgen.spawner_click", "gui.voidgen.spawner_hint"):
        print(lang, k, "->", repr(d.get(k)))