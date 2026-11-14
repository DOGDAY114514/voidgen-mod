"""v2.2.2: cross-dimension wireless broadcast + void value in the generator status message."""
import io
import json
import os

ROOT = r"D:\AI\voidgen-mod"
GEN = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "block", "VoidGeneratorBlockEntity.java")
NET = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "VoidPowerNetwork.java")
BLOCK = os.path.join(ROOT, "src", "main", "java", "com", "voidgen", "block", "VoidGeneratorBlock.java")
LANG = os.path.join(ROOT, "src", "main", "resources", "assets", "voidgen", "lang")

s = io.open(GEN, encoding="utf-8").read()
start = s.index("        long wirelessBudget = Math.min(energy, rate);")
end = s.index("        if (changed) {", start)
new_segment = '''        long rateLeft = rate;
        long wirelessBudget = Math.min(energy, rateLeft);
        if (wirelessBudget > 0) {
            long forcedMoved = pushForced(level, wirelessBudget);
            if (forcedMoved > 0) {
                energy -= forcedMoved;
                rateLeft -= forcedMoved;
                changed = true;
            }
            long rest = Math.min(energy, rateLeft);
            if (rest > 0) {
                java.util.Set<BlockPos> skip = new java.util.HashSet<>(excluded);
                skip.addAll(forced);
                VoidPowerNetwork.PushResult result = VoidPowerNetwork.push(level, worldPosition, rest, rate, range(), aeOutput, wirelessCursor, skip);
                if (result.moved() > 0) {
                    energy -= result.moved();
                    rateLeft -= result.moved();
                    changed = true;
                }
                if (result.cursor() != wirelessCursor) {
                    wirelessCursor = result.cursor();
                }
            }
        }
        // cross-dimension broadcast (v2.2.2): the same generator feeds player-placed
        // receivers in every loaded dimension, not only its own.
        if (rateLeft > 0 && energy > 0 && level.getServer() != null) {
            for (net.minecraft.server.level.ServerLevel other : level.getServer().getAllLevels()) {
                if (other == level || rateLeft <= 0 || energy <= 0) {
                    continue;
                }
                long want = Math.min(energy, rateLeft);
                VoidPowerNetwork.PushResult cross = VoidPowerNetwork.pushInfinite(other, worldPosition, want, rateLeft, aeOutput, wirelessCursor, java.util.Set.of());
                if (cross.moved() > 0) {
                    energy -= cross.moved();
                    rateLeft -= cross.moved();
                    changed = true;
                }
                wirelessCursor = cross.cursor();
            }
        }
'''
s = s[:start] + new_segment + s[end:]
io.open(GEN, "w", encoding="utf-8", newline="\n").write(s)

n = io.open(NET, encoding="utf-8").read()
anchor = "    public static PushResult push(Level level, BlockPos origin, long available, long ratePerTick, long range, boolean aeOutput, int cursor) {"
addition = '''    /** Cross-dimension push: no distance check, only chunk-loaded receivers in that level. */
    public static PushResult pushInfinite(Level level, BlockPos origin, long available, long ratePerTick, boolean aeOutput, int cursor, java.util.Set<BlockPos> skip) {
        List<BlockPos> list = RECEIVERS.get(level.dimension());
        if (list == null || list.isEmpty() || available <= 0 || ratePerTick <= 0) {
            return new PushResult(0, 0);
        }
        int size = list.size();
        long budget = Math.min(available, ratePerTick);
        long moved = 0;
        int checks = Math.min(MAX_CHECKS_PER_TICK, size);
        int start = Math.floorMod(cursor, size);
        for (int i = 0; i < checks && budget > 0; i++) {
            BlockPos pos = list.get((start + i) % size);
            if (pos.equals(origin) || !level.isLoaded(pos) || skip.contains(pos)) {
                continue;
            }
            BlockState state = level.getBlockState(pos);
            boolean aeAcceptor = VoidStats.isAeAcceptorBlock(state.getBlock());
            if (aeAcceptor && !aeOutput) {
                continue;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
            if (target == null || !target.canReceive()) {
                continue;
            }
            int accepted = target.receiveEnergy((int) Math.min(Integer.MAX_VALUE, budget), false);
            if (accepted > 0) {
                budget -= accepted;
                moved += accepted;
            }
        }
        return new PushResult(moved, (start + checks) % size);
    }

'''
if "pushInfinite" not in n:
    n = n.replace(anchor, addition + anchor)
io.open(NET, "w", encoding="utf-8", newline="\n").write(n)

b = io.open(BLOCK, encoding="utf-8").read()
old = "                    rangeText(generator.range())), true);\n"
new = "                    rangeText(generator.range())), true);\n            player.displayClientMessage(Component.translatable(\"status.voidgen.void_value_line\",\n                    VoidStats.fmtCompact(generator.voidAmount())), true);\n"
if "status.voidgen.void_value_line" not in b:
    b = b.replace(old, new)
io.open(BLOCK, "w", encoding="utf-8", newline="\n").write(b)

for name, line in (("en_us.json", "Void: %s"), ("zh_cn.json", "虚无值：%s")):
    path = os.path.join(LANG, name)
    data = json.loads(io.open(path, encoding="utf-8").read())
    data["status.voidgen.void_value_line"] = line
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

toml = os.path.join(ROOT, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
t = io.open(toml, encoding="utf-8").read().replace('version="2.2.1"', 'version="2.2.2"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(t)
bp = os.path.join(ROOT, "tools", "build.ps1")
p = io.open(bp, encoding="utf-8").read().replace("voidgen-2.2.1.jar", "voidgen-2.2.2.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(p)
print("patched v2.2.2")
