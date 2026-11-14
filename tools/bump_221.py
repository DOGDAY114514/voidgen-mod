import io, os, re
ROOT = r"D:\AI\voidgen-mod"
toml = os.path.join(ROOT, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.2.0"', 'version="2.2.1"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(ROOT, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.2.0.jar", "voidgen-2.2.1.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.2.1")