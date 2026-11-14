import io
p = r"D:\AI\voidgen-mod\tools\gen_cell_assets.py"
s = io.open(p, encoding="utf-8").read()
anchor = '    zh["tooltip.voidgen.void_ingot"] = "凝聚的虚无，用于合成 AE2 风格的虚无磁盘。"'
if anchor not in s:
    raise SystemExit("zh tooltip anchor missing")
add = anchor + '\n    zh["item.voidgen.void_ingot_block"] = "虚无锭块"\n    zh["tooltip.voidgen.void_ingot_block"] = "9 个虚无锭压成的方块，方便合成高级磁盘。"'
s = s.replace(anchor, add)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("zh anchor patched")