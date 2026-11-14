import io, os, shutil

src = r"D:\AI\voidgen-mod\docs\cells_v2"
dst = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
for f in os.listdir(src):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))
print("copied", len([f for f in os.listdir(src) if f.endswith('.png')]), "textures")

# bump version in mods.toml
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read()
s = s.replace('version="2.1.0"', 'version="2.1.1"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
print("toml version 2.1.1:", 'version="2.1.1"' in io.open(toml, encoding="utf-8").read())

# bump jar name in build.ps1
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read()
s = s.replace("voidgen-2.1.0.jar", "voidgen-2.1.1.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("build.ps1 2.1.1:", "voidgen-2.1.1.jar" in io.open(bp, encoding="utf-8").read())