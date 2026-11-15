import io, re
p = r"D:\AI\voidgen-mod\tools\make_floating_fx.py"
s = io.open(p, encoding="utf-8").read()
start = s.index("def draw_crystal()")
end = s.index("def draw_dust(")
new_fn = '''def draw_crystal() -> Image.Image:
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # tilted shard, amethyst-shard style silhouette
    n = 13
    for i in range(n):
        t = i / (n - 1)
        x = int(round(10.5 - 5.5 * t))
        y = int(round(2 + 11 * t))
        d.point((x - 1, y), fill=DEEP)
        d.point((x, y), fill=BODY)
        d.point((x + 1, y), fill=DEEP)
    # facet highlight along the upper edge
    for i in range(2, n - 2):
        t = i / (n - 1)
        x = int(round(10.5 - 5.5 * t))
        y = int(round(2 + 11 * t))
        d.point((x, y - 1), fill=LIGHT)
    d.point((9, 4), fill=WHITE)
    d.point((8, 5), fill=WHITE)
    # glowing cyan core near the middle
    d.point((7, 8), fill=CYAN)
    d.point((6, 9), fill=CYAN)
    d.point((7, 9), fill=WHITE)
    return img


'''
s = s[:start] + new_fn + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("rewrote crystal")