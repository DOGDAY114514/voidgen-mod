import io, json, os, zipfile
ROOT = r"D:\AI\voidgen-mod"
toml = os.path.join(ROOT, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.5.1"', 'version="2.5.2"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(ROOT, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.5.1.jar", "voidgen-2.5.2.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
readme = os.path.join(ROOT, "README.md")
s = io.open(readme, encoding="utf-8").read()
s = s.replace("（244.8 KB）", "（244.9 KB）")
s = s.replace("voidgen-2.5.1.jar", "voidgen-2.5.2.jar")
s = s.replace("## 更新日志\n\n",
  "## 更新日志\n\n> **v2.5.2 虚浮水晶/粉特效**：水晶改为斜向晶簇造型，水晶粉改为旋转光点团，两者都加了环绕光点动画（8 帧，frametime 3，插值），与紫水晶粉一眼区分。\n\n", 1)
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.5.2")