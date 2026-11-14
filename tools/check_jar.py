import io, zipfile, hashlib, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.0.3.jar"
print("size", os.path.getsize(jar))
with zipfile.ZipFile(jar) as z:
    print("entries", len(z.namelist()))
    for c in ["assets/voidgen/textures/item/void_storage_iron.png",
              "assets/voidgen/textures/item/filled_void_storage_gold.png",
              "assets/voidgen/textures/item/void_storage_nether.png"]:
        h1 = hashlib.sha256(z.read(c)).hexdigest()[:12]
        h2 = hashlib.sha256(open(os.path.join(r"D:\AI\voidgen-mod\src\main\resources", c), "rb").read()).hexdigest()[:12]
        print("MATCH" if h1 == h2 else "DIFF", c)
    meta = z.read("META-INF/neoforge.mods.toml").decode("utf-8")
    print([l for l in meta.splitlines() if l.startswith("version=")])