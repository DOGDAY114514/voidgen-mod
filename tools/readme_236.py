import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.5 ·", "# Voidgen v2.3.6 ·")
s = s.replace("v2.3.5 · 单文件 mod jar（242.2 KB）", "v2.3.6 · 单文件 mod jar（243.8 KB）")
s = s.replace("voidgen-2.3.5.jar", "voidgen-2.3.6.jar")
note = "> **v2.3.6 JEI 方块配方**：补充 3 个方块级合成配方（金块/钻石块/石英块 + 硅块 + 红石块 → 9 个 AE2 处理器），JEI 里可直接看到，在 AE2 样板终端（合成模式）点「+」即可一键编码成样板，塞进虚空合成器后仍是秒合成、照常扣材料。计算处理器用 3 个石英块（12 晶）换 9 个，会浪费 3 个晶。\n>\n> "
s = s.replace("> **v2.3.5 绑定卡右键修复**", note + "> **v2.3.5 绑定卡右键修复**")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")