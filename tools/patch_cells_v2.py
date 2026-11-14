import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v2.py"
s = io.open(p, encoding="utf-8").read()
s = s.replace("PLATE_LIGHT = (232, 236, 244, 255)", "PLATE_LIGHT = (246, 248, 252, 255)")
s = s.replace("PLATE = (205, 211, 222, 255)", "PLATE = (228, 232, 240, 255)")
s = s.replace("PLATE_MID = (180, 187, 200, 255)", "PLATE_MID = (204, 210, 220, 255)")
s = s.replace("PLATE_DARK = (140, 147, 162, 255)", "PLATE_DARK = (158, 164, 178, 255)")
s = s.replace("        d.point((x, y), fill=color)\n        d.point((x + 1, y), fill=top)\n        d.point((x, y + 1), fill=deep)",
              "        d.point((x, y), fill=color)\n        d.point((x + 1, y), fill=top)\n        d.point((x + 1, y + 1), fill=top)\n        d.point((x, y + 1), fill=deep)")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")