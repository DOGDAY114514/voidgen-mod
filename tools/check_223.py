import json, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.2.3.jar"
z = zipfile.ZipFile(jar)
toml = z.read("META-INF/neoforge.mods.toml").decode("utf-8")
print("mods.toml version line:", [l for l in toml.splitlines() if l.startswith("version=")][:1])
en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang en/zh:", len(en), len(zh), "parity:", set(en)==set(zh))
print("entries:", len(z.namelist()))
print("has tickAll class:", any(n.endswith("VoidGeneratorBlockEntity.class") for n in z.namelist()))