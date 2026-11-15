import io, os, zipfile
from PIL import Image

client = r"C:\Users\Administrator\.gradle\caches\neoformruntime\artifacts\minecraft_1.21.1_client.jar"
outdir = r"D:\AI\voidgen-mod\docs\ingot_ref"
os.makedirs(outdir, exist_ok=True)
want = {
 "assets/minecraft/textures/item/iron_ingot.png": "iron_ingot.png",
 "assets/minecraft/textures/block/iron_block.png": "iron_block.png",
}
with zipfile.ZipFile(client) as z:
    for src, dst in want.items():
        p = os.path.join(outdir, dst)
        open(p, "wb").write(z.read(src))
        img = Image.open(p).convert("RGBA")
        print(dst, img.size)