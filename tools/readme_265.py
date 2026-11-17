import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.6.4 · 单文件 mod jar（250.8 KB）", "v2.6.5 · 单文件 mod jar（276.1 KB）")
s = s.replace("voidgen-2.6.4.jar", "voidgen-2.6.5.jar")
entry = (
    "### v2.6.5 等级保留 + 分级外观 + 满级合成\n"
    "> **升级不再丢等级**：已经用套娃升级过的虚无发电机/虚无熔炉，拆掉时会掉落带等级的方块物品，重新放下仍是原等级；每级方块有独立外观（外壳 + 等级颜色 + 逐级增加的顶盖 / 角柱 / 悬浮环几何），`tier` 同时写进方块状态与方块实体，老存档的机器会按存档等级自动补正外观。\n"
    "> **满级合成**：`虚无发电机 + 套娃 I~V`（无序）直接合成 V 级发电机，`虚无熔炉` 同理；也可以逐级插套娃升级。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")