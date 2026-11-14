import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\block\MeVoidSupplierBlock.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace("import com.voidgen.VoidGen;\n", "import com.voidgen.VoidStats;\n")
s = s.replace("VoidGen.fmtCompact(", "VoidStats.fmtCompact(")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.11"', 'version="2.2.0"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.11.jar", "voidgen-2.2.0.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("patched block + versions")