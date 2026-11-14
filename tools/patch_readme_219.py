import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.8 · 单文件 mod jar（211.5 KB）", "v2.1.9 · 单文件 mod jar（211.7 KB）")
s = s.replace("绑定卡（便携 FE 电池）", "绑定卡（精准供电控制）")
old_note = "> **v2.1.8 绑定卡改为便携电池**：手持绑定卡右键**虚无发电机**抽取 FE，再手持右键其他机器把 FE 输进去（单次最多 1 亿 FE，卡上限 10 亿 FE）。空手右键绑定、自动连接、饰品栏绑定"
idx = s.find(old_note)
if idx >= 0:
    end = s.find("\n", s.find("\n", idx) + 1)  # skip two lines? conservative
    # replace whole note block up to next blank line
    block_end = s.find("\n\n", idx)
    if block_end < 0:
        block_end = s.find("\n", idx)
    new_note = "> **v2.1.9 绑定卡改为「精准供电控制」**：先把卡右键绑定到某台虚无发电机，之后手持卡右键其他方块即可**解除**或**强制**该方块的供电；发电机本身的范围供电逻辑不变。\n"
    s = s[:idx] + new_note + s[block_end:]
    print("note replaced")
else:
    print("note not found")
start = s.find("### 绑定卡（精准供电控制）")
end = s.find("### 虚无收集装置")
if start >= 0 and end > start:
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
    s = s[:start] + section + s[end:]
    print("section replaced")
else:
    print("section bounds", start, end)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)