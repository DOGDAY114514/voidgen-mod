import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx_around.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace('    base = Image.open(os.path.join(TEX, kind + ".png")).convert("RGBA")',
              '    base = Image.open(os.path.join(ROOT, "docs", "item_base", kind + ".png")).convert("RGBA")')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("reads pristine base")