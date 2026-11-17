import io, json, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.6.5.jar"
with zipfile.ZipFile(jar) as z:
    n = z.namelist()
    print("entries", len(n))
    for key in ("assets/voidgen/blockstates/void_generator.json",
                "assets/voidgen/models/block/void_generator_t5.json",
                "assets/voidgen/textures/block/void_generator_top_t5.png",
                "data/voidgen/recipe/void_generator_max.json"):
        print(key, key in n)
    m = json.loads(z.read("assets/voidgen/models/block/void_generator_t5.json"))
    print("t5 elements:", len(m.get("elements", [])))