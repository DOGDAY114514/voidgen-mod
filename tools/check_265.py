import io, json, os, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.6.5.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries", len(names))
    print("gen state:", json.loads(z.read("assets/voidgen/blockstates/void_generator.json"))["variants"].keys())
    print("furnace state:", json.loads(z.read("assets/voidgen/blockstates/void_furnace.json"))["variants"].keys())
    print("gen recipe:", json.loads(z.read("data/voidgen/recipe/void_generator_max.json"))["result"])