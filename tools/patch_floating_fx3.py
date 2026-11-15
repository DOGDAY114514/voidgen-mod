import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace('out = os.path.join(TEX, f"floating_{kind}.png")',
              'names = {"crystal": "floating_crystal", "dust": "floating_crystal_dust"}\n    base = names[kind]\n    out = os.path.join(TEX, base + ".png")')
s = s.replace('meta = os.path.join(TEX, f"floating_{kind}.png.mcmeta")',
              'meta = os.path.join(TEX, base + ".png.mcmeta")')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched names")