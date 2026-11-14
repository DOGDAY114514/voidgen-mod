import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("factor = 0.55 + 0.55 * (lum / 255.0)", "factor = 0.72 + 0.32 * (lum / 255.0)")
s = s.replace("if lum > 150:\n                    col = mix(col, (255, 255, 255), 0.38)", "if lum > 150:\n                    col = mix(col, (255, 255, 255), 0.18)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched sat")