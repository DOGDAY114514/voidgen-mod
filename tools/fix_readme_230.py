import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.2.3", "# Voidgen v2.3.0")
s = s.replace("（226.5 KB）", "（237.1 KB）")
if "v2.3.0 虚空合成器" not in s:
    highlight = "\n> **v2.3.0 虚空合成器**：新增 AE2 联动方块「虚空合成器」——外观/交互仿 AE2 样板供应器，接入 ME 网络后把 AE2 处理器（逻辑/运算/工程）样板直接「虚空合成」：不消耗材料、不需要机器、瞬间把产物塞进 ME 存储。只接受产物为 AE2 处理器的样板；方块贴图是从 AE2 原版样板供应器贴图派生的七彩循环动画（8 帧，frametime 3，插值）。\n"
    idx = s.find("\n\n")
    s = s[:idx] + highlight + s[idx:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok", "v2.3.0" in s)