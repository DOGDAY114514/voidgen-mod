import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.6"', 'version="2.1.7"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.6.jar", "voidgen-2.1.7.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("v2.1.6 · 单文件 mod jar（177.4 KB）", "v2.1.7 · 单文件 mod jar（178.4 KB）")
s = s.replace("> **v2.1.6 元件按原版形状重绘**", "> **v2.1.7 元件/磁盘动态粒子**：虚无元件与虚无磁盘改为 8 帧动画贴图（.png.mcmeta，2 tick/帧），在背包/手中/地上都会看到环绕粒子在动，光点也会轻微呼吸。\n>\n> **v2.1.6 元件按原版形状重绘**")
s = s.replace("dist/voidgen-2.1.6.jar", "dist/voidgen-2.1.7.jar")
s = s.replace("voidgen-2.1.6.jar", "voidgen-2.1.7.jar")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.1.7")