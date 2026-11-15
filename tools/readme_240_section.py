import io
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
start = s.index("### 绑定卡（精准供电控制）")
end = s.index("> 绑定信息存在卡上")
end = s.index("\n", s.index("每台发电机各自独立。", end)) + 1
new = """### 无线供电与自动连接

- 发电机每 tick 自动向**范围内**所有玩家放置的、能接收 FE 的机器供电，不需要线缆或绑定卡。
- 接收器列表会在**区块加载时自动重建**：旧存档里的机器、被强加载的跨维度机器都会被重新发现，不需要玩家重新放置。
- **跨维度**：只要目标区块处于加载状态（例如被 FTB 强加载），主世界/下界/末地的发电机都会自动向其他维度的机器供电。
- 范围由范围卡决定（16 格起，12 张范围卡 = 无限距离）；空手右击发电机可在状态提示里看到当前范围。
"""
s = s[:start] + new + s[end:]
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("section replaced")