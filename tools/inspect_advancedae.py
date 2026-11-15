import os, zipfile
jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\AdvancedAE-1.6.12-1.21.1.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    print("== data recipes ==")
    for n in names:
        if "/recipe/" in n and n.endswith(".json"):
            print(n)
    print("== reaction classes ==")
    for n in names:
        if "reaction" in n.lower() and n.endswith(".class"):
            print(n)