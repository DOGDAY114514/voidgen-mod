import io, os, zipfile
from PIL import Image
jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\appliedenergistics2-19.2.18.jar"
out_dir = r"D:\AI\voidgen-mod\docs\ae2_interface_ref"
os.makedirs(out_dir, exist_ok=True)
with zipfile.ZipFile(jar) as z:
    data = z.read("assets/ae2/textures/block/interface.png")
img = Image.open(io.BytesIO(data)).convert("RGBA")
img.save(os.path.join(out_dir, "interface.png"))
print("saved", img.size)
img.resize((img.width*10, img.height*10), Image.NEAREST).save(os.path.join(out_dir, "interface_10x.png"))