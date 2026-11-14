import zipfile, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.0.4.jar"
print("size", os.path.getsize(jar))
with zipfile.ZipFile(jar) as z:
    b = z.read("META-INF/neoforge.mods.toml")
    print("BOM:", b[:3] == b"\xef\xbb\xbf")
    s = b.decode("utf-8")
    for line in s.splitlines():
        if line.startswith(("displayName", "version", "modId")):
            print(line)
    bad = [n for n in z.namelist() if n.startswith(("com/mojang/", "net/neoforged/", "io/netty/", "appeng/"))]
    print("leaks:", bad)