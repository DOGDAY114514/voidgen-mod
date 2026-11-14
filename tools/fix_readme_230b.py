import io, re
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
lines = s.splitlines()
# normalize title
lines[0] = "# Voidgen v2.3.0 · 虚无发电机 + 虚无熔炉 + 虚无值系统 + AE2 虚无磁盘 / 虚空合成器"
# insert highlight right after the subtitle line (line starting with **Minecraft)
highlight = "> **v2.3.0 虚空合成器**：新增 AE2 联动方块「虚空合成器」——外观/交互仿 AE2 样板供应器，接入 ME 网络后把 AE2 处理器（逻辑/运算/工程）样板直接「虚空合成」：不消耗材料、不需要机器、瞬间把产物塞进 ME 存储。只接受产物为 AE2 处理器的样板；方块贴图是从 AE2 原版样板供应器贴图派生的七彩循环动画（8 帧，frametime 3，插值）。"
if not any("v2.3.0 虚空合成器" in ln for ln in lines):
    for i, ln in enumerate(lines):
        if ln.startswith("**Minecraft 1.21.1"):
            lines.insert(i + 1, "")
            lines.insert(i + 2, highlight)
            break
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("done")