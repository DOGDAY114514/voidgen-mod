import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("单文件 mod jar（230.6 KB）", "单文件 mod jar（230.9 KB）")
entry = "> **v2.4.1 虚无锭块改成真正的方块**：不再是平面物品图标——注册为可放置方块（紫罗兰金属 + 青色菱形镶嵌面），背包里按方块渲染（和钻石块/铁块同款 3D 图标），带上 blockstate/模型/掉落表/镐挖掘标签；合成仍是 9 虚无锭 ↔ 1 虚无锭块。\n\n"
marker = "## 更新日志\n\n"
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme 2.4.1")