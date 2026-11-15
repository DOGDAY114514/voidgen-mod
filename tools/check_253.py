import json, os, zipfile
from PIL import Image
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.5.3.jar"
with zipfile.ZipFile(jar) as z:
    print("entries:", len(z.namelist()), "KB:", round(os.path.getsize(jar)/1024, 1))
    print("version 2.5.3:", b'version="2.5.3"' in z.read("META-INF/neoforge.mods.toml"))
    for name in ("floating_crystal", "floating_crystal_dust"):
        p = f"assets/voidgen/textures/item/{name}.png"
        img = Image.open(__import__("io").BytesIO(z.read(p)))
        meta = json.loads(z.read(p + ".mcmeta"))
        print(name, img.size, meta)