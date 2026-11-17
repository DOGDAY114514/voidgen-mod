import zipfile, json
jars = [r"D:\AI\voidgen-mod\libs\compile-only\appliedenergistics2-19.2.18.jar",
        r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\AdvancedAE-1.6.12-1.21.1.jar"]
for jar in jars:
    try:
        z = zipfile.ZipFile(jar)
    except Exception as e:
        print("skip", jar, e); continue
    hits = []
    for n in z.namelist():
        if "/recipe/" in n and n.endswith(".json"):
            try:
                t = z.read(n).decode("utf-8")
            except Exception:
                continue
            if '"components"' in t:
                hits.append(n)
    print(jar.split("\\")[-1], "recipes with components:", len(hits))
    for h in hits[:5]:
        print(" ", h)
        print(" ", z.read(h).decode("utf-8")[:300].replace("\n"," "))