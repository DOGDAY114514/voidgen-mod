import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.6.4"', 'version="2.6.5"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.6.4.jar", "voidgen-2.6.5.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.6.5")