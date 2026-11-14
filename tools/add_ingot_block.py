import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidGen.java"
s = io.open(p, encoding="utf-8").read()
old = '''    public static final DeferredHolder<Item, Item> VOID_INGOT = ITEMS.register("void_ingot",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));'''
new = '''    public static final DeferredHolder<Item, Item> VOID_INGOT = ITEMS.register("void_ingot",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    public static final DeferredHolder<Item, Item> VOID_INGOT_BLOCK = ITEMS.register("void_ingot_block",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));'''
if old not in s:
    raise SystemExit("ingot pattern missing")
s = s.replace(old, new)
s = s.replace("                        output.accept(VOID_INGOT.get());",
              "                        output.accept(VOID_INGOT.get());\n                        output.accept(VOID_INGOT_BLOCK.get());")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("VoidGen updated")