import io
p = r"D:\AI\voidgen-mod\tools\make_floating_fx_around.py"
s = io.open(p, encoding="utf-8").read()

old_halo = '''def halo(base: Image.Image) -> Image.Image:
    """Soft 1px glow around the opaque silhouette."""
    img = base.copy()
    px = img.load()
    dark = base.load()
    w, h = base.size
    for y in range(h):
        for x in range(w):
            if dark[x, y][3] > 0:
                continue
            near = False
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and dark[nx, ny][3] > 0:
                        near = True
                        break
                if near:
                    break
            if near:
                px[x, y] = (100, 220, 255, 70)
    return img'''
new_halo = '''def halo_mask(base: Image.Image):
    """Positions of transparent pixels touching the opaque silhouette."""
    dark = base.load()
    w, h = base.size
    out = []
    for y in range(h):
        for x in range(w):
            if dark[x, y][3] > 0:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and dark[nx, ny][3] > 0:
                        out.append((x, y))
                        break
                else:
                    continue
                break
    return out'''
s = s.replace(old_halo, new_halo)

old_build = '''    glow = halo(base)
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        frame = glow.copy()
        d = ImageDraw.Draw(frame)'''
new_build = '''    mask = halo_mask(base)
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    for f in range(FRAMES):
        frame = base.copy()
        px = frame.load()
        alpha = int(36 + 34 * abs(math.sin(math.pi * f / FRAMES)))
        for (hx, hy) in mask:
            px[hx, hy] = (100, 220, 255, alpha)
        d = ImageDraw.Draw(frame)'''
s = s.replace(old_build, new_build)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched pulsing halo")