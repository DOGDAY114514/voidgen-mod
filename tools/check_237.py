import os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.7.jar"
with zipfile.ZipFile(jar) as z:
    print("entries:", len(z.namelist()), "KB:", round(os.path.getsize(jar)/1024, 1))
    print("version 2.3.7:", b'version="2.3.7"' in z.read("META-INF/neoforge.mods.toml"))
    cls = z.read("com/voidgen/ae/VoidAssemblerLogic.class")
    print("scanProcessors present:", b"scanProcessors" in cls)