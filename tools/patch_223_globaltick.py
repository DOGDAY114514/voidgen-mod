"""v2.2.3: run generator ticks from the global server tick (independent of chunk entity ticking),
so force-loaded chunks keep generating/pushing even when no player is in the dimension."""
import io
import json
import os

ROOT = r"D:\AI\voidgen-mod"
BE = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "block", "VoidGeneratorBlockEntity.java")
BLOCK = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "block", "VoidGeneratorBlock.java")
GEN = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "VoidGen.java")

s = io.open(BE, encoding="utf-8").read()

# imports
if "import net.minecraft.server.MinecraftServer;" not in s:
    s = s.replace("import net.minecraft.world.level.Level;\n",
                  "import net.minecraft.resources.ResourceKey;\n"
                  "import net.minecraft.server.MinecraftServer;\n"
                  "import net.minecraft.server.level.ServerLevel;\n"
                  "import net.minecraft.world.level.Level;\n", 1)

anchor = "    public VoidGeneratorBlockEntity(BlockPos pos, BlockState state) {\n        super(VoidGen.VOID_GENERATOR_BE.get(), pos, state);\n    }\n"
addition = (
    "\n"
    "    // Global tick registry (v2.2.3): generators tick from ServerTickEvent.Post, so a\n"
    "    // force-loaded chunk keeps running even when its chunk is not entity-ticking.\n"
    "    private static final java.util.Map<ResourceKey<Level>, java.util.Set<BlockPos>> ACTIVE = new java.util.concurrent.ConcurrentHashMap<>();\n"
    "\n"
    "    @Override\n"
    "    public void setLevel(Level level) {\n"
    "        super.setLevel(level);\n"
    "        if (level != null && !level.isClientSide()) {\n"
    "            ACTIVE.computeIfAbsent(level.dimension(), key -> java.util.concurrent.ConcurrentHashMap.newKeySet()).add(worldPosition);\n"
    "        }\n"
    "    }\n"
    "\n"
    "    @Override\n"
    "    public void setRemoved() {\n"
    "        Level level = getLevel();\n"
    "        if (level != null) {\n"
    "            java.util.Set<BlockPos> set = ACTIVE.get(level.dimension());\n"
    "            if (set != null) {\n"
    "                set.remove(worldPosition);\n"
    "            }\n"
    "        }\n"
    "        super.setRemoved();\n"
    "    }\n"
    "\n"
    "    public static void tickAll(MinecraftServer server) {\n"
    "        for (ServerLevel level : server.getAllLevels()) {\n"
    "            java.util.Set<BlockPos> set = ACTIVE.get(level.dimension());\n"
    "            if (set == null || set.isEmpty()) {\n"
    "                continue;\n"
    "            }\n"
    "            for (BlockPos pos : new java.util.ArrayList<>(set)) {\n"
    "                if (!level.isLoaded(pos)) {\n"
    "                    continue;\n"
    "                }\n"
    "                if (level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity generator) {\n"
    "                    generator.tick(level);\n"
    "                }\n"
    "            }\n"
    "        }\n"
    "    }\n"
)
if "public static void tickAll(" not in s:
    s = s.replace(anchor, anchor + addition)
io.open(BE, "w", encoding="utf-8", newline="\n").write(s)

b = io.open(BLOCK, encoding="utf-8").read()
old_ticker = '''    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide) {
            return null;
        }
        return (tickLevel, pos, tickState, blockEntity) -> {
            if (blockEntity instanceof VoidGeneratorBlockEntity generator) {
                generator.tick(tickLevel);
            }
        };
    }
'''
if old_ticker in b:
    b = b.replace(old_ticker, """    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        // v2.2.3: ticking is driven by ServerTickEvent.Post (VoidGeneratorBlockEntity.tickAll),
        // so force-loaded chunks keep working without entity ticks.
        return null;
    }
""")
io.open(BLOCK, "w", encoding="utf-8", newline="\n").write(b)

g = io.open(GEN, encoding="utf-8").read()
if "VoidGeneratorBlockEntity::tickAll" not in g:
    g = g.replace(
        "        modBus.addListener(RegisterPayloadHandlersEvent.class, VoidNet::register);\n",
        "        modBus.addListener(RegisterPayloadHandlersEvent.class, VoidNet::register);\n"
        "        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.addListener(net.neoforged.neoforge.event.tick.ServerTickEvent.Post.class,\n"
        "                event -> VoidGeneratorBlockEntity.tickAll(event.getServer()));\n",
    )
io.open(GEN, "w", encoding="utf-8", newline="\n").write(g)

toml = os.path.join(ROOT, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
t = io.open(toml, encoding="utf-8").read().replace('version="2.2.2"', 'version="2.2.3"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(t)
bp = os.path.join(ROOT, "tools", "build.ps1")
p = io.open(bp, encoding="utf-8").read().replace("voidgen-2.2.2.jar", "voidgen-2.2.3.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(p)
print("patched v2.2.3 global tick")
