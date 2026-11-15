import io, json
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang"
add_en = {"key.categories.voidgen": "Voidgen", "key.voidgen.guide": "Voidgen Guide", "gui.voidgen.guide.title": "Voidgen Guide"}
add_zh = {"key.categories.voidgen": "Voidgen", "key.voidgen.guide": "Voidgen 使用说明", "gui.voidgen.guide.title": "Voidgen 使用说明"}
for name, add in (("en_us.json", add_en), ("zh_cn.json", add_zh)):
    p = base + "\\" + name
    data = json.load(io.open(p, encoding="utf-8"))
    data.update(add)
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(name, "keys:", len(data))

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.7"', 'version="2.3.8"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.7.jar", "voidgen-2.3.8.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.3.8")