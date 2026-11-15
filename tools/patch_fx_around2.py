import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx_around.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("alpha = int(36 + 34 * abs(math.sin(math.pi * f / FRAMES)))",
              "alpha = int(90 + 60 * abs(math.sin(math.pi * f / FRAMES)))")
s = s.replace("px[hx, hy] = (100, 220, 255, alpha)",
              "px[hx, hy] = (150, 246, 255, alpha)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("brightened halo")