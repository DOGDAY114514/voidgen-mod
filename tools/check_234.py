import io, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.4.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries:", len(names), "KB:", round(os.path.getsize(jar)/1024,1))
    print("version 2.3.4:", b'version="2.3.4"' in z.read("META-INF/neoforge.mods.toml"))
    print("logic present:", "com/voidgen/ae/VoidAssemblerLogic.class" in names)
    print("lang en keys:", len(__import__("json").loads(z.read("assets/voidgen/lang/en_us.json").decode("utf-8"))))
    print("lang zh keys:", len(__import__("json").loads(z.read("assets/voidgen/lang/zh_cn.json").decode("utf-8"))))