import io
p = r"D:\AI\voidgen-mod\tools\make_cell_textures_v3.py"
s = io.open(p, encoding="utf-8").read()
old = '''    comp = Image.open(os.path.join(REF, "cell_component_256k.png")).convert("RGBA")
    px = comp.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            if mx - mn > 24 and mx > 80:
                px[x, y] = (150, 226, 255, a) if (r + g + b) / 3 > 150 else (70, 150, 200, a)
    for (x, y) in [(1, 1), (14, 14)]:
        if px[x, y][3] == 0:
            px[x, y] = SPARK
    comp.save(os.path.join(OUT, "void_component.png"))'''
new = '''    # component: clean AE2-256k-style grey frame + dark socket + 4 cyan dots
    from PIL import ImageDraw
    comp = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(comp)
    d.rectangle([3, 3, 12, 12], fill=(58, 62, 72, 255))
    d.rectangle([2, 4, 13, 11], fill=(58, 62, 72, 255))
    d.rectangle([4, 2, 11, 13], fill=(58, 62, 72, 255))
    d.rectangle([4, 4, 11, 11], fill=(205, 211, 222, 255))
    d.line([4, 4, 11, 4], fill=(246, 248, 252, 255))
    d.line([4, 4, 4, 11], fill=(246, 248, 252, 255))
    d.line([4, 11, 11, 11], fill=(158, 164, 178, 255))
    d.line([11, 4, 11, 11], fill=(158, 164, 178, 255))
    d.rectangle([5, 5, 10, 10], fill=(40, 52, 68, 255))
    for (x, y) in [(6, 6), (9, 6), (6, 9), (9, 9)]:
        d.point((x, y), fill=(150, 226, 255, 255))
    d.point((7, 8), fill=(220, 250, 255, 255))
    d.point((8, 7), fill=(220, 250, 255, 255))
    for (x, y) in [(1, 1), (14, 14)]:
        d.point((x, y), fill=SPARK)
    comp.save(os.path.join(OUT, "void_component.png"))'''
if old not in s:
    raise SystemExit("pattern not found")
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("component redrawn")