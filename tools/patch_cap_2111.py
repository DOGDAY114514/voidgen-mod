import io
stats = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidStats.java"
s = io.open(stats, encoding="utf-8").read()
s = s.replace("public static final long MAX_BUFFER = 92_000_000_000L;", "public static final long MAX_BUFFER = Long.MAX_VALUE;")
old = """    public static long capacity(int tier, int capacityCards) {
        long value = BASE_BUFFER;
        for (int i = 0; i < Math.min(tier, 8); i++) {
            value *= 4L;
        }
        value *= 1L << Math.min(capacityCards, 20);
        return Math.min(value, MAX_BUFFER);
    }"""
new = """    public static long capacity(int tier, int capacityCards) {
        long value = BASE_BUFFER;
        for (int i = 0; i < Math.min(tier, 8); i++) {
            value = satMul(value, 4L);
        }
        value = satMul(value, 1L << Math.min(capacityCards, 20));
        return Math.min(value, MAX_BUFFER);
    }

    private static long satMul(long a, long b) {
        if (a <= 0L || b <= 0L) {
            return 0L;
        }
        if (a > Long.MAX_VALUE / b) {
            return Long.MAX_VALUE;
        }
        return a * b;
    }"""
if old not in s:
    raise SystemExit("capacity pattern missing")
s = s.replace(old, new)
oldfmt = """    public static String fmt(long value) {
        return String.format("%,d", value);
    }"""
newfmt = """    public static String fmt(long value) {
        return String.format("%,d", value);
    }

    /** Human-friendly magnitude for the huge generator numbers (K/M/G/T/P/E). */
    public static String fmtCompact(long value) {
        if (value < 1_000_000L) {
            return String.format("%,d", value);
        }
        if (value >= 1_000_000_000_000_000_000L) {
            return String.format("%.2fE", value / 1.0E18);
        }
        if (value >= 1_000_000_000_000_000L) {
            return String.format("%.2fP", value / 1.0E15);
        }
        if (value >= 1_000_000_000_000L) {
            return String.format("%.2fT", value / 1.0E12);
        }
        if (value >= 1_000_000_000L) {
            return String.format("%.2fG", value / 1.0E9);
        }
        return String.format("%.2fM", value / 1.0E6);
    }"""
if oldfmt not in s:
    raise SystemExit("fmt pattern missing")
s = s.replace(oldfmt, newfmt)
io.open(stats, "w", encoding="utf-8", newline="\n").write(s)

scr = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\client\VoidGeneratorScreen.java"
t = io.open(scr, encoding="utf-8").read()
for a, b in [
    ('Component.translatable("gui.voidgen.rate", VoidStats.fmt(this.menu.rate()))', 'Component.translatable("gui.voidgen.rate", VoidStats.fmtCompact(this.menu.rate()))'),
    ('Component.translatable("gui.voidgen.energy", VoidStats.fmt(this.menu.energy()), VoidStats.fmt(this.menu.capacity()))', 'Component.translatable("gui.voidgen.energy", VoidStats.fmtCompact(this.menu.energy()), VoidStats.fmtCompact(this.menu.capacity()))'),
    ('Component.translatable("gui.voidgen.finite", VoidStats.fmt(this.menu.range()))', 'Component.translatable("gui.voidgen.finite", VoidStats.fmtCompact(this.menu.range()))'),
]:
    if a not in t:
        print("screen pattern missing:", a[:60])
    t = t.replace(a, b)
io.open(scr, "w", encoding="utf-8", newline="\n").write(t)

blk = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\block\VoidGeneratorBlock.java"
t = io.open(blk, encoding="utf-8").read()
t = t.replace("VoidStats.fmt(generator.rate()),", "VoidStats.fmtCompact(generator.rate()),")
t = t.replace("VoidStats.fmt(generator.energy()),", "VoidStats.fmtCompact(generator.energy()),")
t = t.replace("VoidStats.fmt(generator.capacity()),", "VoidStats.fmtCompact(generator.capacity()),")
t = t.replace('Component.translatable("gui.voidgen.finite", VoidStats.fmt(range))', 'Component.translatable("gui.voidgen.finite", VoidStats.fmtCompact(range))')
io.open(blk, "w", encoding="utf-8", newline="\n").write(t)

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.10"', 'version="2.1.11"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.10.jar", "voidgen-2.1.11.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("patched to 2.1.11")