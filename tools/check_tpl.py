import os, zipfile
p = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item\item_storage_cell_1k.png"
print("exists:", os.path.exists(p))
mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
with zipfile.ZipFile(os.path.join(mods, "appliedenergistics2-19.2.18.jar")) as z:
    for n in ["assets/ae2/textures/item/item_storage_cell_1k.png", "assets/ae2/textures/item/cell_component_1k.png"]:
        print(n, len(z.read(n)))