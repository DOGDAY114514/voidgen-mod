import io
p = r"D:\AI\voidgen-mod\tools\gen_cell_assets.py"
s = io.open(p, encoding="utf-8").read()

# zh anchor fix: add block lang keys next to zh housing line
s = s.replace('        zh.pop("item.voidgen.void_component", None)',
              '        zh.pop("item.voidgen.void_component", None)')

old_zh = 'zh["item.voidgen.void_cell_housing"] = "虚无磁盘外壳"'
if old_zh not in s:
    raise SystemExit("zh anchor missing")
s = s.replace(old_zh, old_zh + '\n    zh["item.voidgen.void_ingot_block"] = "虚无锭块"\n    zh["tooltip.voidgen.void_ingot_block"] = "9 个虚无锭压成的方块，方便合成高级磁盘。"')

# replace naive reverse recipe with correct result id
old_call = '''    shapeless("void_ingot_from_block", [{"item": "voidgen:void_ingot_block"}], 9, condition=False)'''
new_call = '''    write_json(os.path.join(RECIPES, "void_ingot_from_block.json"), {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [{"item": "voidgen:void_ingot_block"}],
        "result": {"count": 9, "id": "voidgen:void_ingot"},
    })'''
if old_call not in s:
    raise SystemExit("reverse recipe call missing")
s = s.replace(old_call, new_call)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")