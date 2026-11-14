import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("deep = tuple(int(c * 0.45) for c in tier_rgb)", "deep = tuple(int(c * 0.55) for c in tier_rgb)")
s = s.replace("light = mix(tier_rgb, (255, 255, 255), 0.72)", "light = mix(tier_rgb, (255, 255, 255), 0.45)")
s = s.replace("f = min(1.0, max(0.0, (lum - 30) / 200.0))", "f = min(1.0, max(0.0, (lum - 60) / 160.0))")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")