import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v2.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("from PIL import Image\n", "from PIL import Image, ImageDraw\n")
s = s.replace("d = img.load()", "d = ImageDraw.Draw(img)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched", s.count("ImageDraw.Draw(img)"))