import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.2.2 · 单文件 mod jar（225.9 KB）", "v2.2.3 · 单文件 mod jar（226.5 KB）")
note = """> **v2.2.3 跨维度/强加载修复**：发电机改为由全局服务器 tick 驱动（不再依赖区块实体 tick）。只要区块被 FTB 强加载、且目标机器所在区块已加载，玩家人在别的维度也会持续发电与传电。
>
"""
if "v2.2.3 跨维度/强加载修复" not in s:
    s = s.replace("> **v2.2.2 跨维度传电**", note + "> **v2.2.2 跨维度传电**", 1)
s = s.replace("dist/voidgen-2.2.2.jar", "dist/voidgen-2.2.3.jar")
s = s.replace("voidgen-2.2.2.jar", "voidgen-2.2.3.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme bumped 2.2.3")