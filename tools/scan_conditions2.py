import zipfile
jar = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_ca10438c8142438b8004b4852cd3f4b53c99c79f_output.jar"
with zipfile.ZipFile(jar) as z:
    for t in [b"mod_loaded", b"tag_empty", b"item_exists"]:
        names = [n for n in z.namelist() if n.endswith(".class") and t in z.read(n)]
        print(t.decode(), "->", names[:6])