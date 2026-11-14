import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()

s = s.replace("**Minecraft 1.21.1 · NeoForge 21.1.x · v2.1.7 · 单文件 mod jar（178.4 KB）**",
              "**Minecraft 1.21.1 · NeoForge 21.1.x · v2.1.8 · 单文件 mod jar（211.5 KB）**")
s = s.replace("+ 绑定卡（人物饰品栏）", "+ 绑定卡（便携 FE 电池）")
s = s.replace("> **v2.1.7 元件/磁盘动态粒子**",
              "> **v2.1.8 绑定卡改为便携电池**：手持绑定卡右键**虚无发电机**抽取 FE，再手持右键其他机器把 FE 输进去（单次最多 1 亿 FE，卡上限 10 亿 FE）。空手右键绑定、自动连接、饰品栏绑定逻辑全部移除。\n>\n> **v2.1.7 元件/磁盘动态粒子**")

old_section = s[s.index("### 绑定卡（人物饰品栏，一拖多）"):s.index("### 升级卡（可叠放）")]
new_section = '''### 绑定卡（便携 FE 电池）

| 项目 | 说明 |
|---|---|
| 合成 | 套娃 II + 末影珍珠 + 金锭 + 红石（无序） |
| 抽电 | 手持绑定卡 **右键虚无发电机**：把发电机里的 FE 抽进卡里（单次最多 100,000,000 FE） |
| 放电 | 手持绑定卡 **右键其他机器**：把卡里的 FE 输进目标（任何带 FE 能力/接口的机器都行） |
| 容量 | 卡内最多存 **1,000,000,000 FE**，动作栏会提示抽取/输出/卡满/没电 |
| 限制 | 不再支持空手右键绑定、饰品栏绑定、自动连接；发电机恢复为范围内全量无线供电 |

> 绑定卡数据存在物品的 CUSTOM_DATA（NBT）里，丢地上/换手/放箱子都不会丢电量。

'''
s = s.replace(old_section, new_section)

s = s.replace("（v2.1.8 起绑定/自动连接已移除，见上）", "")
s = s.replace("- 自动记录**玩家放置的、带方块实体的方块**（机器）；无卡时在范围内全量供电，有绑定卡时只供绑定目标（绑定目标不受范围限制）。",
              "- 自动记录**玩家放置的、带方块实体的方块**（机器），在范围内全量供电。")
s = s.replace("- 每个发电机每 tick 最多检查 32 个接收器（绑定模式为绑定目标），轮询游标保证多台机器/多个目标公平分电。",
              "- 每个发电机每 tick 最多检查 32 个接收器，轮询游标保证多台机器/多个目标公平分电。")
s = s.replace("dist/voidgen-2.1.7.jar", "dist/voidgen-2.1.8.jar")
s = s.replace("voidgen-2.1.7.jar", "voidgen-2.1.8.jar")
s = s.replace("（人物饰品栏）", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README updated")