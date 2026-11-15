import zipfile, re
jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\appliedenergistics2-19.2.18.jar"
with zipfile.ZipFile(jar) as z:
    hits = []
    for n in z.namelist():
        if "/recipe/" in n and n.endswith(".json"):
            s = z.read(n).decode("utf-8", "ignore")
            if '"amount"' in s and '"id"' in s:
                hits.append(n)
    print("recipes with id+amount:", hits[:10])