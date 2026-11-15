import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidGen.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace('''    public static final DeferredHolder<Item, BindingCardItem> BINDING_CARD = ITEMS.register("binding_card",
            () -> new BindingCardItem(new Item.Properties()));

''', "")
s = s.replace("                        output.accept(BINDING_CARD.get());\n", "")
s = s.replace("        NeoForge.EVENT_BUS.addListener(PlayerInteractEvent.RightClickBlock.class, BindingCardItem::onRightClickBlock);\n", "")
s = s.replace("        NeoForge.EVENT_BUS.addListener(PlayerTickEvent.Post.class, VoidAccessory::onPlayerTick);\n", "")
s = s.replace("        NeoForge.EVENT_BUS.addListener(PlayerEvent.PlayerLoggedInEvent.class, VoidAccessory::onLoggedIn);\n", "")
s = s.replace("        NeoForge.EVENT_BUS.addListener(PlayerEvent.Clone.class, VoidAccessory::onClone);\n", "")
s = s.replace("        NeoForge.EVENT_BUS.addListener(BlockEvent.EntityPlaceEvent.class, VoidPowerNetwork::onPlace);\n",
              "        NeoForge.EVENT_BUS.addListener(BlockEvent.EntityPlaceEvent.class, VoidPowerNetwork::onPlace);\n        NeoForge.EVENT_BUS.addListener(ChunkEvent.Load.class, VoidPowerNetwork::onChunkLoad);\n")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("VoidGen edited")