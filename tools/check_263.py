import io, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.6.3.jar"
with zipfile.ZipFile(jar) as z:
    print("version 2.6.3:", b'version="2.6.3"' in z.read("META-INF/neoforge.mods.toml"))
    print("has getBlockEntitiesPos ref:", b"getBlockEntitiesPos" in z.read("com/voidgen/VoidPowerNetwork.class"))
print("entries:", len(zipfile.ZipFile(jar).namelist()))

readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
for line in s.splitlines():
    if "2.6.2" in line or "250.7 KB" in line or "249.9 KB" in line:
        print("README:", line[:120])