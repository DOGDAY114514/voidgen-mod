import io, os, re
ROOT = r"D:\AI\voidgen-mod"
jar = os.path.join(ROOT, "dist", "voidgen-2.2.1.jar")
kb = os.path.getsize(jar) / 1024.0
p = os.path.join(ROOT, "README.md")
s = io.open(p, encoding="utf-8").read()
s = re.sub(r"v2\.2\.0 · 单文件 mod jar（[0-9.]+ KB）", "v2.2.1 · 单文件 mod jar（%.1f KB）" % kb, s)
s = s.replace("> - 贴图为 8 帧动画：三色端口 + 移动光条 + 变色核心。",
              "> - 贴图为 8 帧动画：三色端口 + 移动光条 + 变色核心。\n> - **v2.2.1**：供应器贴图改为从 AE2 原版 ME 接口贴图重绘（同心方框 + 紫/青脉冲 + 游走光点），虚无值改为晶体图标。")
s = s.replace("voidgen-2.2.0.jar", "voidgen-2.2.1.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README 2.2.1 OK, %.1f KB" % kb)