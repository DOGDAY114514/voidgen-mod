import io, json, os
ROOT = r"D:\AI\voidgen-mod"
RES = os.path.join(ROOT, "src", "main", "resources")
def wj(rel, obj):
    p = os.path.join(RES, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2); fh.write("\n")

wj("data/voidgen/recipe/floating_crystal_dust_from_certus.json", {
    "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": "ae2"}],
    "type": "minecraft:crafting_shapeless",
    "category": "misc",
    "ingredients": [{"item": "ae2:certus_quartz_crystal"}],
    "result": {"count": 2, "id": "voidgen:floating_crystal_dust"},
})
wj("data/voidgen/recipe/floating_crystal_dust_from_crystal.json", {
    "type": "minecraft:crafting_shapeless",
    "category": "misc",
    "ingredients": [{"item": "voidgen:floating_crystal"}],
    "result": {"count": 4, "id": "voidgen:floating_crystal_dust"},
})

toml = os.path.join(RES, "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.5.0"', 'version="2.5.1"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(ROOT, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.5.0.jar", "voidgen-2.5.1.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

readme = os.path.join(ROOT, "README.md")
s = io.open(readme, encoding="utf-8").read()
s = s.replace("（244.1 KB）", "（244.2 KB）")
s = s.replace("voidgen-2.5.0.jar", "voidgen-2.5.1.jar")
s = s.replace("## 更新日志\n\n",
  "## 更新日志\n\n> **v2.5.1 虚浮水晶粉获取**：1 赛特斯石英 → 2 虚浮水晶粉（无序，需 AE2）；1 虚浮水晶 → 4 虚浮水晶粉（无序）。\n\n", 1)
s = s.replace("- **虚浮水晶** / **虚浮水晶粉**：由 AE2 赛特斯系列重绘（紫罗兰 + 青色）。",
  "- **虚浮水晶** / **虚浮水晶粉**：由 AE2 赛特斯系列重绘（紫罗兰 + 青色）。粉的获取：1 赛特斯石英 → 2 粉（无序），1 虚浮水晶 → 4 粉（无序）。")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("2.5.1 prepared")