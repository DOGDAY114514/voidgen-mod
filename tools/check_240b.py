import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.4.0.jar"
with zipfile.ZipFile(jar) as z:
    n = z.namelist()
    print("entries:", len(n), "KB:", round(os.path.getsize(jar)/1024,1))
    print("binding leftovers:", [x for x in n if "binding_card" in x or "BindingCard" in x or "VoidAccessory" in x])
    print("lang:", len(json.loads(z.read("assets/voidgen/lang/en_us.json"))), len(json.loads(z.read("assets/voidgen/lang/zh_cn.json"))))
    print("recipes:", len([x for x in n if x.startswith("data/voidgen/recipe/") and x.endswith(".json")]))