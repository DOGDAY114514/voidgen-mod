import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.2 ·", "# Voidgen v2.3.3 ·")
s = s.replace("v2.3.2 · 单文件 mod jar（236.9 KB）", "v2.3.3 · 单文件 mod jar（241.9 KB）")
s = s.replace("voidgen-2.3.2.jar", "voidgen-2.3.3.jar")
old = "> **v2.3.1/2.3.2 贴图调整**：保留 AE2 样板供应器的白壳 + 深灰框 + 同心方框构图，纹路做小幅修改（核心四角切角、四角螺丝、中心发光核），并按 8 帧循环做七彩换色（frametime 3，插值）。"
new = "> **v2.3.3 贴图渐变**：保留 AE2 样板供应器的白壳 + 深灰框 + 同心方框构图，核心颜色改为**对角渐变幻彩**（同一帧内从左上到右下色相平移），动画扩到 32 帧（frametime 2，插值），游戏里是连续渐变而不是跳色。"
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")