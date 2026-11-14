import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.1 ·", "# Voidgen v2.3.2 ·")
s = s.replace("v2.3.1 · 单文件 mod jar（236.7 KB）", "v2.3.2 · 单文件 mod jar（236.9 KB）")
s = s.replace("voidgen-2.3.1.jar", "voidgen-2.3.2.jar")
old_note = "> **v2.3.1 贴图重绘**：虚空合成器贴图不再直接照搬 AE2 样板供应器——改为六边形虚空符印 + 上下导管 + 四角符文，保留 AE2 金属边框手感；仍是 8 帧七彩循环动画（frametime 3，插值）。"
new_note = "> **v2.3.1/2.3.2 贴图调整**：保留 AE2 样板供应器的白壳 + 深灰框 + 同心方框构图，纹路做小幅修改（核心四角切角、四角螺丝、中心发光核），并按 8 帧循环做七彩换色（frametime 3，插值）。"
s = s.replace(old_note, new_note)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")