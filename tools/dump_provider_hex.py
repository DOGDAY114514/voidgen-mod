from PIL import Image
p = r"D:\AI\voidgen-mod\docs\assembler_ref\pattern_provider_block.png"
img = Image.open(p).convert("RGBA")
px = img.load()
for y in range(16):
    row = []
    for x in range(16):
        r,g,b,a = px[x,y]
        row.append("%02x%02x%02x" % (r,g,b))
    print(y, " ".join(row))