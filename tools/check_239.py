import io, os, zipfile, json
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.3.9.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("entries:", len(names), "KB:", round(os.path.getsize(jar)/1024,1))
    print("version 2.3.9:", b'version="2.3.9"' in z.read("META-INF/neoforge.mods.toml"))
    recipes = [n for n in names if n.startswith("data/voidgen/recipe/") and n.endswith(".json")]
    print("recipes:", len(recipes))
    print("block recipes present:", [n for n in recipes if "processor_" in n and "from_blocks" in n])
    from PIL import Image
    # lang parity
    langs = {}
    for loc in ("en_us", "zh_cn"):
        data = json.loads(z.read(f"assets/voidgen/lang/{loc}.json").decode("utf-8"))
        langs[loc] = data
    print("lang en/zh:", len(langs["en_us"]), len(langs["zh_cn"]), "parity:", set(langs["en_us"]) == set(langs["zh_cn"]))