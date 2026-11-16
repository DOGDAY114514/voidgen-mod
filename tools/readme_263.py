import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.6.2 · 单文件 mod jar（250.7 KB）", "v2.6.3 · 单文件 mod jar（250.7 KB）")
s = s.replace("voidgen-2.6.2.jar", "voidgen-2.6.3.jar")
entry = (
    "### v2.6.3 无线供电重连修复\n"
    "> 区块从磁盘加载时，方块实体在 `ChunkEvent.Load` 阶段仍是「待实例化 NBT」，`getBlockEntities()` 为空，导致重启后接收机列表丢失、发电机无线不供电。现在改为遍历 `getBlockEntitiesPos()`（包含待实例化位置），用能���查询把它们实例化后注册；跨维度推送同步受益。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")