import io, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.0.jar"
size = os.path.getsize(jar)
print("jar bytes", size, "KB", round(size/1024, 1))
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("v2.2.3 · 单文件 mod jar", "v2.3.0 · 单文件 mod jar")
s = s.replace("（231.9 KB）", "（232.5 KB）")
highlight = """> **v2.3.0 虚空合成器**：新增 AE2 联动方块「虚空合成器」——外观/交互仿 AE2 样板供应器，接入 ME 网络后把 AE2 处理器（逻辑/运算/工程）样板直接「虚空合成」：不消耗材料、不需要机器、瞬间把产物塞进 ME 存储。只接受产物为 AE2 处理器的样板。方块贴图是从 AE2 原版样板供应器贴图派生的七彩循环动画（8 帧，frametime 3，插值）。
>
"""
marker = "> **v2.2.3 "
if marker in s:
    s = s.replace(marker, highlight + marker, 1)
else:
    # fall back: insert after front matter line
    lines = s.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            lines.insert(i, highlight.rstrip("\n"))
            break
    s = "\n".join(lines)
s = s.replace("dist/voidgen-2.2.3.jar", "dist/voidgen-2.3.0.jar")
s = s.replace("voidgen-2.2.3.jar", "voidgen-2.3.0.jar")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("README updated")