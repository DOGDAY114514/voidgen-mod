import io, json

# 1) add spawner_hint lang keys
for lang, text in (("en_us", "Scroll or use < > to change page"), ("zh_cn", "\u6eda\u8f6e\u6216\u53f3\u4e0a\u89d2 < > \u7ffb\u9875")):
    p = rf"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang\{lang}.json"
    d = json.load(io.open(p, encoding="utf-8"))
    d["gui.voidgen.spawner_hint"] = text
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(lang, "keys:", len(d))

# 2) clean the replacement char comment in NothingnessCollectorMenu
p2 = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\block\NothingnessCollectorMenu.java"
s = io.open(p2, encoding="utf-8").read()
idx = s.find("\ufffd")
print("menu file replacement at", idx)
print(json.dumps(s[max(0, idx-60):idx+40], ensure_ascii=True))