import json, zipfile, io, os
from PIL import Image
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.7.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    print("version", b'version="2.1.7"' in z.read("META-INF/neoforge.mods.toml"))
    mcs = [n for n in names if n.endswith(".png.mcmeta") and "void_" in n]
    print("mcmeta files", len(mcs))
    for t in ["void_cell_1k", "void_component_16k"]:
        n = "assets/voidgen/textures/item/%s.png" % t
        im = Image.open(io.BytesIO(z.read(n)))
        print(t, im.size)
        meta = json.loads(z.read(n + ".mcmeta"))
        print("  ", meta)