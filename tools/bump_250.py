import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read()
s = s.replace('version="2.4.1"', 'version="2.5.0"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.4.1.jar", "voidgen-2.5.0.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.5.0")