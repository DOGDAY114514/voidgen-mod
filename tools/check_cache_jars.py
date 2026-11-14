import zipfile, glob, os
files = glob.glob(r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_*_output.jar")
for f in files:
    try:
        with zipfile.ZipFile(f) as z:
            m = z.read("META-INF/MANIFEST.MF").decode("utf-8", "replace")
        print("==", os.path.basename(f))
        for line in m.splitlines():
            if any(k in line for k in ("Implementation-Version", "Specification-Version", "FML-System-Mods", "Implementation-Title")):
                print("   ", line.strip())
    except Exception as e:
        print("ERR", f, e)