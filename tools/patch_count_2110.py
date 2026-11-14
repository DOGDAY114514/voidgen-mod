import io
stats = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidStats.java"
s = io.open(stats, encoding="utf-8").read()
old = """        int count = 0;
        for (int slot = 0; slot < handler.getSlots(); slot++) {
            if (typeOf(handler.getStackInSlot(slot)) == type) {
                count++;
            }
        }"""
new = """        int count = 0;
        for (int slot = 0; slot < handler.getSlots(); slot++) {
            ItemStack stack = handler.getStackInSlot(slot);
            if (typeOf(stack) == type) {
                count += stack.getCount();
            }
        }"""
if old not in s:
    raise SystemExit("count pattern missing")
s = s.replace(old, new)
io.open(stats, "w", encoding="utf-8", newline="\n").write(s)
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.9"', 'version="2.1.10"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.9.jar", "voidgen-2.1.10.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("patched count + 2.1.10")