"""Patch VoidGen.java + lang files for the ME void supplier (v2.2.0). UTF-8 safe."""
import io
import json
import os

ROOT = r"D:\AI\voidgen-mod"
GEN = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "VoidGen.java")
LANG_DIR = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "lang")

s = io.open(GEN, encoding="utf-8").read()

# imports
s = s.replace(
    "import com.voidgen.block.VoidGeneratorMenu;\n",
    "import com.voidgen.block.VoidGeneratorMenu;\n"
    "import com.voidgen.block.MeVoidSupplierBlock;\n"
    "import com.voidgen.block.MeVoidSupplierBlockEntity;\n",
)
if "import com.voidgen.item.VoidValueItem;" not in s:
    s = s.replace(
        "import com.voidgen.item.VoidGeneratorItem;\n",
        "import com.voidgen.item.VoidGeneratorItem;\nimport com.voidgen.item.VoidValueItem;\n",
    )

# registrations: insert after the distributor BE registration block
anchor = (
    '    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<NothingnessDistributorBlockEntity>> NOTHING_DISTRIBUTOR_BE =\n'
    '            BLOCK_ENTITIES.register("nothing_distributor", () -> BlockEntityType.Builder.<NothingnessDistributorBlockEntity>of(\n'
    '                    (pos, state) -> new NothingnessDistributorBlockEntity(pos, state), NOTHING_DISTRIBUTOR.get()).build(null));\n'
)
addition = (
    '\n'
    '    // ---- ME 虚无供应器（v2.2） ----\n'
    '\n'
    '    public static final DeferredHolder<Item, VoidValueItem> VOID_VALUE = ITEMS.register("void_value",\n'
    '            () -> new VoidValueItem(new Item.Properties().stacksTo(64)));\n'
    '\n'
    '    public static final DeferredHolder<Block, MeVoidSupplierBlock> ME_VOID_SUPPLIER = BLOCKS.register("me_void_supplier",\n'
    '            () -> new MeVoidSupplierBlock(BlockBehaviour.Properties.of()\n'
    '                    .mapColor(MapColor.COLOR_PURPLE)\n'
    '                    .strength(4.0F, 5.0F)\n'
    '                    .requiresCorrectToolForDrops()\n'
    '                    .sound(SoundType.METAL)));\n'
    '    public static final DeferredHolder<Item, BlockItem> ME_VOID_SUPPLIER_ITEM = ITEMS.register("me_void_supplier",\n'
    '            () -> new BlockItem(ME_VOID_SUPPLIER.get(), new Item.Properties()));\n'
    '    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<MeVoidSupplierBlockEntity>> ME_VOID_SUPPLIER_BE =\n'
    '            BLOCK_ENTITIES.register("me_void_supplier", () -> BlockEntityType.Builder.<MeVoidSupplierBlockEntity>of(\n'
    '                    (pos, state) -> new MeVoidSupplierBlockEntity(pos, state), ME_VOID_SUPPLIER.get()).build(null));\n'
)
if anchor not in s:
    raise SystemExit("distributor BE anchor missing")
s = s.replace(anchor, anchor + addition)

# capability for the supplier's item handler (ME import/export bus access)
cap_anchor = (
    '        modBus.addListener(RegisterCapabilitiesEvent.class, event -> event.registerBlockEntity(\n'
    '                Capabilities.ItemHandler.BLOCK, VOID_FURNACE_BE.get(), (blockEntity, side) -> blockEntity.getItemHandler(side)));\n'
)
cap_addition = (
    '\n'
    '        modBus.addListener(RegisterCapabilitiesEvent.class, event -> event.registerBlockEntity(\n'
    '                Capabilities.ItemHandler.BLOCK, ME_VOID_SUPPLIER_BE.get(), (blockEntity, side) -> blockEntity.getItemHandler()));\n'
)
if cap_anchor not in s:
    raise SystemExit("capability anchor missing")
s = s.replace(cap_anchor, cap_anchor + cap_addition)

# creative tab entries
tab_anchor = '                        output.accept(NOTHING_DISTRIBUTOR_ITEM.get());\n'
tab_addition = (
    '                        output.accept(ME_VOID_SUPPLIER_ITEM.get());\n'
    '                        output.accept(VOID_VALUE.get());\n'
)
if tab_anchor not in s:
    raise SystemExit("tab anchor missing")
s = s.replace(tab_anchor, tab_anchor + tab_addition)

io.open(GEN, "w", encoding="utf-8", newline="\n").write(s)

# lang additions
en_add = {
    "item.voidgen.void_value": "Void Value",
    "tooltip.voidgen.void_value": "1 item = 1,000 void value",
    "tooltip.voidgen.void_value.hint": "ME Import Bus can pull it into AE (void disks required)",
    "block.voidgen.me_void_supplier": "ME Void Supplier",
    "item.voidgen.me_void_supplier": "ME Void Supplier",
    "tooltip.voidgen.me_void_supplier": "SUPPLY: void value items -> nearby machines . IMPORT: collector void -> void value items",
    "status.voidgen.supplier_mode": "Mode: %s",
    "status.voidgen.supplier_supply": "SUPPLY",
    "status.voidgen.supplier_import": "IMPORT",
    "status.voidgen.supplier_status": "Void: %s . Slot items: %s",
}
zh_add = {
    "item.voidgen.void_value": "虚无值",
    "tooltip.voidgen.void_value": "1 个 = 1,000 虚无值",
    "tooltip.voidgen.void_value.hint": "ME 输入总线可把它吸进 AE（需要虚无磁盘存储）",
    "block.voidgen.me_void_supplier": "ME 虚无供应器",
    "item.voidgen.me_void_supplier": "ME 虚无供应器",
    "tooltip.voidgen.me_void_supplier": "SUPPLY：虚无值物品 → 供给附近机器；IMPORT：从收集装置抽虚无值 → 生成虚无值物品",
    "status.voidgen.supplier_mode": "模式：%s",
    "status.voidgen.supplier_supply": "供给（SUPPLY）",
    "status.voidgen.supplier_import": "导入（IMPORT）",
    "status.voidgen.supplier_status": "虚无值：%s · 槽内物品：%s",
}
for name, add in (("en_us.json", en_add), ("zh_cn.json", zh_add)):
    path = os.path.join(LANG_DIR, name)
    data = json.loads(io.open(path, encoding="utf-8").read())
    data.update(add)
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

print("patched VoidGen + lang")
