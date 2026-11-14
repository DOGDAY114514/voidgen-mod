import io
p = r"D:\AI\voidgen-mod\tools\gen_cell_assets.py"
s = io.open(p, encoding="utf-8").read()

old = '''DISK_EXTRA = {
    "1k": [],
    "4k": [{"item": "voidgen:void_ingot"}],
    "16k": [{"item": "voidgen:void_ingot"}] * 2,
    "64k": [{"item": "voidgen:void_ingot"}] * 4,
    "256k": [{"item": "voidgen:void_ingot"}] * 8,
    "1m": [{"item": "voidgen:void_ingot"}] * 8 + [{"item": "minecraft:diamond_block"}],
    "4m": [{"item": "voidgen:void_ingot"}] * 8 + [{"item": "minecraft:emerald_block"}],
    "16m": [{"item": "voidgen:void_ingot"}] * 16 + [{"item": "minecraft:netherite_ingot"}],
    "64m": [{"item": "voidgen:void_ingot"}] * 24 + [{"item": "minecraft:nether_star"}],
    "256m": [{"item": "voidgen:void_ingot"}] * 32 + [{"item": "minecraft:nether_star"}, {"item": "minecraft:nether_star"}],
}'''
new = '''INGOT = {"item": "voidgen:void_ingot"}
INGOT_BLOCK = {"item": "voidgen:void_ingot_block"}

# keep every shapeless recipe <= 9 ingredients (vanilla crafts on a 3x3 grid)
DISK_EXTRA = {
    "1k": [],
    "4k": [INGOT],
    "16k": [INGOT] * 2,
    "64k": [INGOT_BLOCK],
    "256k": [INGOT_BLOCK, INGOT, INGOT],
    "1m": [INGOT_BLOCK, {"item": "minecraft:diamond_block"}],
    "4m": [INGOT_BLOCK, {"item": "minecraft:emerald_block"}],
    "16m": [INGOT_BLOCK] * 2 + [{"item": "minecraft:netherite_ingot"}],
    "64m": [INGOT_BLOCK] * 3 + [{"item": "minecraft:nether_star"}],
    "256m": [INGOT_BLOCK] * 4 + [{"item": "minecraft:nether_star"}] * 2,
}'''
if old not in s:
    raise SystemExit("disk extra block missing")
s = s.replace(old, new)

old2 = '''COMP_UPGRADE = {
    "4k": [{"item": "voidgen:void_ingot"}],
    "16k": [{"item": "voidgen:void_ingot"}] * 2,
    "64k": [{"item": "voidgen:void_ingot"}] * 2,
    "256k": [{"item": "voidgen:void_ingot"}] * 4,
    "1m": [{"item": "voidgen:void_ingot"}] * 4 + [{"item": "minecraft:diamond_block"}],
    "4m": [{"item": "voidgen:void_ingot"}] * 4 + [{"item": "minecraft:emerald_block"}],
    "16m": [{"item": "voidgen:void_ingot"}] * 8 + [{"item": "minecraft:netherite_ingot"}],
    "64m": [{"item": "voidgen:void_ingot"}] * 8 + [{"item": "minecraft:nether_star"}],
    "256m": [{"item": "voidgen:void_ingot"}] * 16 + [{"item": "minecraft:nether_star"}, {"item": "minecraft:nether_star"}],
}'''
new2 = '''COMP_UPGRADE = {
    "4k": [INGOT],
    "16k": [INGOT] * 2,
    "64k": [INGOT_BLOCK],
    "256k": [INGOT_BLOCK, INGOT, INGOT],
    "1m": [INGOT_BLOCK, {"item": "minecraft:diamond_block"}],
    "4m": [INGOT_BLOCK, {"item": "minecraft:emerald_block"}],
    "16m": [INGOT_BLOCK] * 2 + [{"item": "minecraft:netherite_ingot"}],
    "64m": [INGOT_BLOCK] * 2 + [{"item": "minecraft:nether_star"}],
    "256m": [INGOT_BLOCK] * 3 + [{"item": "minecraft:nether_star"}] * 2,
}'''
if old2 not in s:
    raise SystemExit("comp upgrade block missing")
s = s.replace(old2, new2)

s = s.replace('    item_model("void_ingot")\n', '    item_model("void_ingot")\n    item_model("void_ingot_block")\n')

# add block recipes right after the ingot recipe
anchor = '''    shapeless("void_ingot", [
        {"item": "voidgen:filled_void_storage_emerald"},
        {"item": "minecraft:nether_star"},
        {"item": "minecraft:diamond_block"},
    ], 8, condition=False)'''
add = anchor + '''

    shaped("void_ingot_block", ["iii", "iii", "iii"], {
        "i": {"item": "voidgen:void_ingot"},
    }, 1, condition=False)
    shapeless("void_ingot_from_block", [{"item": "voidgen:void_ingot_block"}], 9, condition=False)'''
s = s.replace(anchor, add)

# lang entries
s = s.replace('en["item.voidgen.void_cell_housing"] = "Void Cell Housing"',
              'en["item.voidgen.void_cell_housing"] = "Void Cell Housing"\n    en["item.voidgen.void_ingot_block"] = "Void Ingot Block"\n    en["tooltip.voidgen.void_ingot_block"] = "Nine void ingots compressed into one block."')
s = s.replace('zh["item.voidgen.void_cell_housing"] = "虚无磁盘外壳"',
              'zh["item.voidgen.void_cell_housing"] = "虚无磁盘外壳"\n    zh["item.voidgen.void_ingot_block"] = "虚无锭块"\n    zh["tooltip.voidgen.void_ingot_block"] = "9 个虚无锭压成的方块，方便合成高级磁盘。"')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("gen_cell_assets updated")