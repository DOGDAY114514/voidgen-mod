import zipfile
jar = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_ca10438c8142438b8004b4852cd3f4b53c99c79f_output.jar"
targets = [b"neoforge:conditions", b"neoforge:mod_loaded"]
with zipfile.ZipFile(jar) as z:
    hits = {t: [] for t in targets}
    for name in z.namelist():
        if not name.endswith(".class"):
            continue
        data = z.read(name)
        for t in targets:
            if t in data:
                hits[t].append(name)
    for t, names in hits.items():
        print(t.decode(), "->", len(names), "classes")
        for n in names[:8]:
            print("   ", n)