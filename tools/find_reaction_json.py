import os, zipfile
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
found = []
for name in sorted(os.listdir(mods)):
    if not name.endswith(".jar"): continue
    try:
        with zipfile.ZipFile(os.path.join(mods, name)) as z:
            for n in z.namelist():
                if "/recipe/" in n and n.endswith(".json"):
                    txt = z.read(n).decode("utf-8", "ignore")
                    if "input_items" in txt or '"what"' in txt:
                        found.append((name, n, txt[:400]))
    except Exception: pass
print("hits:", len(found))
for f in found[:6]:
    print("==", f[0], f[1])
    print(f[2][:400])