import io, os, zipfile
root = r"D:\AI\voidgen-mod"
toml = os.path.join(root, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.6"', 'version="2.3.7"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(root, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.6.jar", "voidgen-2.3.7.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.3.7")