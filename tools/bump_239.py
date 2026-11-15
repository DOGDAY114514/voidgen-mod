import io
# bump version
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.8"', 'version="2.3.9"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.8.jar", "voidgen-2.3.9.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
# README changelog
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "> **v2.3.8 游戏内说明**"
new = ("> **v2.3.9 合成配方修正**：移除 v2.3.6 添加的 3 个方块级合成配方（它们会出现在合成台和 JEI 合成页）。"
       "虚空合成器放宽产物过滤——接受所有含 `processor` 的处理器物品与刻印器 `printed_*` 中间物，"
       "所以刻印器 / 水晶装配器 / 电路切片器的 JEI 配方可以直接按 + 编码成处理样板，放进虚空合成器秒合成；"
       "材料仍从 ME 网络扣除。\n\n")
s = s.replace(anchor, new + anchor)
s = s.replace("> **v2.3.6 JEI 合成配方**", "> **v2.3.6 JEI 合成配方（v2.3.9 已移除）**")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme/toml/build bumped to 2.3.9")