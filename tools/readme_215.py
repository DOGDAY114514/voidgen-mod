import io, json, os
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
subs = [
    ("**Minecraft 1.21.1 · NeoForge 21.1.x · v2.1.4 · 单文件 mod jar（176.6 KB）**",
     "**Minecraft 1.21.1 · NeoForge 21.1.x · v2.1.5 · 单文件 mod jar（177.3 KB）**"),
    ("> **v2.1.3 贴图重绘**", "> **v2.1.5 分级虚无元件**：虚无元件补齐 1K~256M 共 10 个等级，元件逐级合成；虚无磁盘改用对应等级的元件合成。新增「虚无锭块」（9 锭 ↔ 1 块），把所有磁盘配方压到 3×3 可放。\n>\n> **v2.1.3 贴图重绘**"),
    ("dist/voidgen-2.1.4.jar", "dist/voidgen-2.1.5.jar"),
    ("voidgen-2.1.4.jar", "voidgen-2.1.5.jar"),
]
for a, b in subs:
    if a in s:
        s = s.replace(a, b)
    else:
        print("miss:", a[:40])
# 更新 2.1.0 小节标题里的元件描述
s = s.replace("**虚无元件 1K~256M**（10 个等级；1K = 虚无锭 + 红石块 + 末影珍珠，之后用上一级元件",
              "**虚无元件 1K~256M**（10 个等级，1K 为圆形、4K~256M 为方形，逐级用上一级元件")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("README updated", len(s))