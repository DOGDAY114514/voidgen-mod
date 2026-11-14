import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
old = "                factor = 0.55 + 0.55 * (lum / 255.0)\n                col = tuple(min(255, int(c * factor)) for c in tier_rgb)\n                px[x, y] = (col[0], col[1], col[2], a)"
new = "                factor = 0.55 + 0.55 * (lum / 255.0)\n                col = tuple(min(255, int(c * factor)) for c in tier_rgb)\n                if lum > 150:\n                    col = mix(col, (255, 255, 255), 0.38)\n                px[x, y] = (col[0], col[1], col[2], a)"
if old not in s:
    raise SystemExit("pattern missing")
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched highlight")