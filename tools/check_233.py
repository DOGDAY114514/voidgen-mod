import io, json, os, zipfile
from PIL import Image
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.3.jar"
with zipfile.ZipFile(jar) as z:
    print("entries:", len(z.namelist()), "KB:", round(os.path.getsize(jar)/1024,1))
    print("version:", b'version="2.3.3"' in z.read("META-INF/neoforge.mods.toml"))
    print("mcmeta:", json.loads(z.read("assets/voidgen/textures/block/void_assembler.png.mcmeta")))
    img = Image.open(io.BytesIO(z.read("assets/voidgen/textures/block/void_assembler.png")))
    print("texture:", img.size, "frames:", img.size[1]//16)