import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.0 ·", "# Voidgen v2.3.1 ·")
s = s.replace("v2.3.0 · 单文件 mod jar（237.1 KB）", "v2.3.1 · 单文件 mod jar（236.7 KB）")
s = s.replace("voidgen-2.3.0.jar", "voidgen-2.3.1.jar")
note = "> **v2.3.1 贴图重绘**：虚空合成器贴图不再直接照搬 AE2 样板供应器——改为六边形虚空符印 + 上下导管 + 四角符文，保留 AE2 金属边框手感；仍是 8 帧七彩循环动画（frametime 3，插值）。"
if "v2.3.1 贴图重绘" not in s:
    lines = s.splitlines()
    idx = next(i for i, ln in enumerate(lines) if ln.startswith("> **v2.3.0 虚空合成器**"))
    lines.insert(idx + 1, note)
    s = "\n".join(lines) + "\n"
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")