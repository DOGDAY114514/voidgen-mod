import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx.py"
s = io.open(p, encoding="utf-8").read()

old_rows = '''    rows = {
        2: (7, 8), 3: (6, 9), 4: (6, 9), 5: (5, 10), 6: (5, 10),
        7: (5, 10), 8: (5, 10), 9: (5, 10), 10: (6, 9), 11: (6, 9), 12: (7, 8),
    }'''
new_rows = '''    rows = {
        1: (7, 8), 2: (7, 8), 3: (6, 9), 4: (6, 9), 5: (5, 10), 6: (5, 10),
        7: (5, 10), 8: (5, 10), 9: (5, 10), 10: (5, 10), 11: (6, 9), 12: (6, 9),
        13: (7, 8), 14: (7, 8),
    }'''
s = s.replace(old_rows, new_rows)

old_facet = '''    # facet highlight
    d.line([(8, 3), (8, 4), (9, 5), (9, 6)], fill=LIGHT)
    d.point((7, 5), fill=WHITE)
    # glowing core
    d.line([(7, 7), (8, 10)], fill=CYAN)
    d.point((7, 8), fill=WHITE)'''
new_facet = '''    # facet highlight down the left side
    d.line([(7, 3), (6, 5), (6, 8), (7, 10)], fill=LIGHT)
    d.point((7, 6), fill=WHITE)
    d.point((6, 7), fill=WHITE)
    # glowing core
    d.rectangle([7, 7, 8, 8], fill=CYAN)
    d.point((7, 7), fill=WHITE)'''
s = s.replace(old_facet, new_facet)

old_dust = '''        t = i / 10.0
        col = (
            int(BODY[0] + (CYAN[0] - BODY[0]) * t),
            int(BODY[1] + (CYAN[1] - BODY[1]) * t),
            int(BODY[2] + (CYAN[2] - BODY[2]) * t),
            255,
        )'''
new_dust = '''        t = i / 10.0
        if i in (3, 8):
            col = CYAN
        else:
            col = (
                int(BODY[0] + (LIGHT[0] - BODY[0]) * t),
                int(BODY[1] + (LIGHT[1] - BODY[1]) * t),
                int(BODY[2] + (LIGHT[2] - BODY[2]) * t),
                255,
            )'''
s = s.replace(old_dust, new_dust)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")