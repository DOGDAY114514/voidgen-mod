import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx_around.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("    mask = halo_mask(base)", "    mask = []  # keep the original sprite pristine; FX are the orbiting sparkles")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("halo removed")