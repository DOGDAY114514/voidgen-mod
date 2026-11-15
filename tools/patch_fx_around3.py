import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx_around.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("        for (hx, hy) in mask:\n            px[hx, hy] = (150, 246, 255, alpha)",
              "        for (hx, hy) in mask:\n            if (hx + hy + f) % 3 != 0:\n                continue\n            px[hx, hy] = (150, 246, 255, alpha)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("sparsified halo")