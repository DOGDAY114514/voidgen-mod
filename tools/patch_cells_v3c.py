import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("                f = min(1.0, max(0.0, (lum - 60) / 160.0))\n                col = mix(deep, light, f)\n                px[x, y] = (col[0], col[1], col[2], a)",
              "                factor = 0.55 + 0.55 * (lum / 255.0)\n                col = tuple(min(255, int(c * factor)) for c in tier_rgb)\n                px[x, y] = (col[0], col[1], col[2], a)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched vivid")