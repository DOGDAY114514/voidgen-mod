import zipfile, os
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
jars = ["appliedenergistics2-19.2.18.jar", "megacells-4.11.0.jar", "ExtendedAE-1.21-2.2.42-neoforge.jar", "ae2omnicells-1.21.1-neoforge-1.1.6.jar", "bigger_ae2-1.21.1-21.2.3.jar"]
for j in jars:
    p = os.path.join(mods, j)
    if not os.path.exists(p):
        print("MISSING", j)
        continue
    with zipfile.ZipFile(p) as z:
        hits = [n for n in z.namelist() if ("component" in n.lower() or "cell" in n.lower()) and n.endswith(".png") and "/item/" in n]
    print("=====", j)
    for h in sorted(hits)[:40]:
        print("  ", h)