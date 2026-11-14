import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("211.7 KB", "213.7 KB")
s = s.replace("voidgen-2.1.8.jar", "voidgen-2.1.9.jar")
start = s.find("### 绑定卡")
end = s.find("\n### ", start + 1)
if end < 0:
    end = s.find("\n## ", start + 1)
section = """### 绑定卡（精准供电控制）

| 操作 | 效果 |
|---|---|
| 右键 **虚无发电机** | 把卡绑定到这台发电机（再右键一次解除绑定）；绑定坐标显示在物品提示里 |
| 右键 **其他方块** | 切换该方块是否接受这台发电机的无线供电 |
| 发电机本身 | 依旧范围内全量无线供电，绑定卡只做例外控制 |

- 对**范围内正在供电**的方块右键 → 停止给它供电（加入排除表）
- 对**范围外 / 没在供电**的方块右键 → 强制绑定供电（无视范围）
- 再右键一次 → 恢复默认供电

> 绑定信息存在卡上（发电机坐标 + 维度）；发电机被拆掉后卡片会自动清空绑定。方块例外表存在发电机方块实体里，NBT 持久化，每台发电机各自独立。

"""
if start >= 0 and end > start:
    s = s[:start] + section + s[end:]
    print("section ok", start, end)
else:
    print("section fail", start, end)
while "\n\n\n" in s:
    s = s.replace("\n\n\n", "\n\n")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done", "2.1.9" in s, len(s))