import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.6 ·", "# Voidgen v2.3.7 ·")
s = s.replace("v2.3.6 · 单文件 mod jar（243.8 KB）", "v2.3.7 · 单文件 mod jar（244.1 KB）")
s = s.replace("voidgen-2.3.6.jar", "voidgen-2.3.7.jar")
note = "> **v2.3.7 自动识别附属处理器**：虚空合成器不再写死 AE2 的三个处理器 id——运行时扫描物品注册表，凡是 id 以 `_processor` 结尾、且不是 press/print 中间产物的物品都算处理器。整合包里实测识别到 20 个（AE2 + AdvancedAE / ExtendedAE / MEGA Cells / AppliedFlux / ae2cs / ae2lt / ae2omnicells / appgen / data_energistics / neoecoae 等）。这些处理器各自的配方仍由附属提供（刻印器 / 晶体装配器 / 晶体聚合器等），在 JEI 里按各自分类显示；编码成样板后塞进虚空合成器即可秒合成、照常扣材料。\n>\n> "
s = s.replace("> **v2.3.6 JEI 方块配方**", note + "> **v2.3.6 JEI 方块配方**")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")