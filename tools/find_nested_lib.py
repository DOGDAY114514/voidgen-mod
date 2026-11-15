import os, zipfile, io
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
jar = os.path.join(mods, "AdvancedAE-1.6.12-1.21.1.jar")
with zipfile.ZipFile(jar) as z:
    nested = [n for n in z.namelist() if n.lower().endswith(".jar")]
    print("nested jars:", nested)
    for n in nested:
        data = z.read(n)
        with zipfile.ZipFile(io.BytesIO(data)) as nz:
            names = nz.namelist()
            if any("ae2addonlib" in x for x in names):
                print("found lib in nested:", n, "entries:", len(names))
                for x in names:
                    if x.endswith(("IngredientStack$Item.class", "IngredientStack$Fluid.class", "IngredientStack.class")):
                        print("  ", x)
                open(r"D:\AI\voidgen-mod\build\ae2addonlib.jar", "wb").write(data)