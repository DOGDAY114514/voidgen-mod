import io
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read()
old = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_ca10438c8142438b8004b4852cd3f4b53c99c79f_output.jar"
new = r"C:\Users\Administrator\.gradle\caches\neoformruntime\intermediate_results\compiledWithNeoForge_719987e3c5f5d9e2c827822e1813d4a73b19efd6_output.jar"
if old not in s:
    raise SystemExit("old path not found")
s = s.replace(old, new)
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("patched patched-jar path -> 21.1.265")