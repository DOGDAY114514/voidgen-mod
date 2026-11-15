import os, zipfile
jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\appliedenergistics2-19.2.18.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    for n in names:
        if n.startswith("assets/ae2/textures/") and ("certus" in n or "budding" in n or "quartz" in n):
            print(n)