import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.1.jar"
with zipfile.ZipFile(jar) as z:
    names = set(z.namelist())
    print("entries:", len(names), "size KB:", round(os.path.getsize(jar)/1024, 1))
    print("version 2.3.1:", b'version="2.3.1"' in z.read("META-INF/neoforge.mods.toml"))
    tex = z.read("assets/voidgen/textures/block/void_assembler.png")
    from PIL import Image
    img = Image.open(io.BytesIO(tex))
    print("texture size:", img.size)
    print("mcmeta:", json.loads(z.read("assets/voidgen/textures/block/void_assembler.png.mcmeta")))
    print("assembler classes:", sorted(n for n in names if "VoidAssembler" in n))
    leaks = [n for n in names if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))]
    print("leaks:", len(leaks))
    en = json.loads(z.read("assets/voidgen/lang/en_us.json")); zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("lang:", len(en), len(zh), "assembler:", en.get("block.voidgen.void_assembler"), zh.get("block.voidgen.void_assembler"))