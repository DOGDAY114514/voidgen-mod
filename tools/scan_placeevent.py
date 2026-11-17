import zipfile
jar = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_719987e3c5f5d9e2c827822e1813d4a73b19efd6_output.jar"
with zipfile.ZipFile(jar) as z:
    for n in z.namelist():
        if not n.endswith(".class"):
            continue
        b = z.read(n)
        if b"EntityPlaceEvent" in b:
            print(n)