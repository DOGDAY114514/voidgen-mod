import zipfile
jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\appliedenergistics2-19.2.18.jar"
z = zipfile.ZipFile(jar)
hits = [n for n in z.namelist() if "interface" in n.lower() and n.endswith(".png") and "/block/" in n]
for n in hits: print(n)
print("---")
hits2 = [n for n in z.namelist() if n.endswith("me_interface_front.png") or n.endswith("me_interface_side.png") or n.endswith("me_interface_top.png")]
for n in hits2: print(n)