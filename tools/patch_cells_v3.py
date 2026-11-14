import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("if mx - mn >= 16 and b > r + 8 and b >= g - 6:", "if mx - mn >= 45 and b > r and b >= g - 10:")
s = s.replace("if mx - mn <= 34 and mx > 120:", "if mx - mn <= 40 and mx > 150:")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")