import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.5"', 'version="2.1.6"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.5.jar", "voidgen-2.1.6.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("v2.1.5 · 单文件 mod jar（177.3 KB）", "v2.1.6 · 单文件 mod jar（177.4 KB）")
s = s.replace("> **v2.1.5 分级虚无元件**", "> **v2.1.6 元件按原版形状重绘**：1K~256K 分别套用 AE2 的圆形/椭圆/三角/方形元件轮廓，1M~256M 套用 MEGA Cells 的暗色虚空元件轮廓，再按等级换色并加虚无粒子。\n>\n> **v2.1.5 分级虚无元件**")
s = s.replace("dist/voidgen-2.1.5.jar", "dist/voidgen-2.1.6.jar")
s = s.replace("voidgen-2.1.5.jar", "voidgen-2.1.6.jar")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.1.6")