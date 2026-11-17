import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.6.3 · 单文件 mod jar（250.7 KB）", "v2.6.4 · 单文件 mod jar（250.8 KB）")
s = s.replace("voidgen-2.6.3.jar", "voidgen-2.6.4.jar")
entry = (
    "### v2.6.4 放下即连修复\n"
    "> 新放置的机器不再要求「事件触发时方块实体已经存在」：注册改为只记位置，供电时再查询能力；能量查询先试无面上下文，失败再依次试 6 个面（兼容只在特定面暴�� FE 的机器）。刚放下的机器下一 tick 就能被无线供电。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")