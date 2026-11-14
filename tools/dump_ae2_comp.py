from PIL import Image

ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
for f in ["cell_component_1k.png", "cell_component_256k.png"]:
    img = Image.open(rf"{ref}\{f}").convert("RGBA")
    px = img.load()
    print("==", f)
    for y in range(16):
        row = []
        for x in range(16):
            r,g,b,a = px[x,y]
            row.append("%02x%02x%02x" % (r,g,b) if a else "......")
        print(" ".join(row))