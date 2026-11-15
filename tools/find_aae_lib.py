import os, zipfile
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
# find jar containing ae2addonlib classes
for name in os.listdir(mods):
    if not name.endswith(".jar"): continue
    try:
        with zipfile.ZipFile(os.path.join(mods, name)) as z:
            if any(n.startswith("net/pedroksl/ae2addonlib/recipes/IngredientStack") for n in z.namelist()):
                print("lib in:", name)
    except Exception: pass
# advancedae reaction chamber type id
jar = os.path.join(mods, "AdvancedAE-1.6.12-1.21.1.jar")
with zipfile.ZipFile(jar) as z:
    names = [n for n in z.namelist() if "ReactionChamberRecipe" in n]
    print(names)