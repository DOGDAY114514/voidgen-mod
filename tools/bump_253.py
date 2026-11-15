import io, json, os, zipfile
ROOT = r"D:\AI\voidgen-mod"
toml = os.path.join(ROOT, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.5.2"', 'version="2.5.3"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(ROOT, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.5.2.jar", "voidgen-2.5.3.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
readme = os.path.join(ROOT, "README.md")
s = io.open(readme, encoding="utf-8").read()
s = s.replace("（245.9 KB）", "（246.0 KB）")
s = s.replace("voidgen-2.5.2.jar", "voidgen-2.5.3.jar")
s = s.replace("## 更新日志\n\n",
  "## 更新日志\n\n> **v2.5.3 特效位置修正**：保留原来的虚浮水晶 / 水晶粉贴图本体不动，只在外围加环绕光点与闪烁粒子（8 帧，frametime 3，插值）。\n\n", 1)
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.5.3")