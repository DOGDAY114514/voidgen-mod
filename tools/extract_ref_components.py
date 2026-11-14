import zipfile, os
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
out = r"D:\AI\voidgen-mod\docs\ref_components"
os.makedirs(out, exist_ok=True)
src = [
    ("appliedenergistics2-19.2.18.jar", "assets/ae2/textures/item/cell_component_%s.png", ["1k","4k","16k","64k","256k"]),
    ("megacells-4.11.0.jar", "assets/megacells/textures/item/cell_component_%s.png", ["1m","4m","16m","64m","256m"]),
]
for jar, pat, tiers in src:
    with zipfile.ZipFile(os.path.join(mods, jar)) as z:
        for t in tiers:
            name = pat % t
            data = z.read(name)
            dst = os.path.join(out, "ref_component_%s.png" % t)
            open(dst, "wb").write(data)
            print("extracted", t, len(data))
# also check megacells for item cell sprites
with zipfile.ZipFile(os.path.join(mods, "megacells-4.11.0.jar")) as z:
    hits = [n for n in z.namelist() if "storage_cell" in n.lower() and n.endswith(".png") and "/item/" in n and "portable" not in n]
for h in sorted(hits):
    print("cell:", h)