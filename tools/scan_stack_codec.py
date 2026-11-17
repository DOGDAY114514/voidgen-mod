import zipfile
jar = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_719987e3c5f5d9e2c827822e1813d4a73b19efd6_output.jar"
with zipfile.ZipFile(jar) as z:
    b = z.read("net/minecraft/world/item/ItemStack.class")
    for probe in (b"components", b"custom_data", b"count", b"id"):
        print(probe, probe in b)