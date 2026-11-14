import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.4"', 'version="2.3.5"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.4.jar", "voidgen-2.3.5.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.4 ·", "# Voidgen v2.3.5 ·")
s = s.replace("v2.3.4 · 单文件 mod jar（242.1 KB）", "v2.3.5 · 单文件 mod jar（242.2 KB）")
s = s.replace("voidgen-2.3.4.jar", "voidgen-2.3.5.jar")
old = "> **v2.3.4 修正消耗材料说明**"
new = "> **v2.3.5 绑定卡右键修复**：右键机器时先在 `PlayerInteractEvent.RightClickBlock` 里拦截，绑定卡先执行「解除/强制/恢复」切换，再取消事件——不再被熔炉、收集器、ME 供应器等方块的 GUI 抢走点击。\n>\n" + old
s = s.replace(old, new, 1)
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.3.5")