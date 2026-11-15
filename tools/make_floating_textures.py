import io, os, zipfile
from PIL import Image

jar = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods\appliedenergistics2-19.2.18.jar"
ref = r"D:\AI\voidgen-mod\docs\ref_floating"
os.makedirs(ref, exist_ok=True)
items = {
    "certus_crystal": "assets/ae2/textures/item/certus_quartz_crystal.png",
    "certus_dust": "assets/ae2/textures/item/certus_quartz_dust.png",
}
blocks = {
    "damaged": "assets/ae2/textures/block/damaged_budding_quartz.png",
    "chipped": "assets/ae2/textures/block/chipped_budding_quartz.png",
    "flawed": "assets/ae2/textures/block/flawed_budding_quartz.png",
    "flawless": "assets/ae2/textures/block/flawless_budding_quartz.png",
}
with zipfile.ZipFile(jar) as z:
    for key, path in items.items():
        open(os.path.join(ref, key + ".png"), "wb").write(z.read(path))
    for key, path in blocks.items():
        open(os.path.join(ref, key + ".png"), "wb").write(z.read(path))
print("extracted", os.listdir(ref))

# ---- recolor ----
def clamp(v): return max(0, min(255, int(v)))

def recolor_item(src, out, ramp):
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            # pick two nearest stops
            t = lum / 255.0
            n = len(ramp) - 1
            pos = t * n
            i = min(n - 1, int(pos))
            f = pos - i
            c0, c1 = ramp[i], ramp[i + 1]
            px[x, y] = (clamp(c0[0] + (c1[0] - c0[0]) * f),
                        clamp(c0[1] + (c1[1] - c0[1]) * f),
                        clamp(c0[2] + (c1[2] - c0[2]) * f), a)
    img.save(out)

CRYSTAL_RAMP = [(30, 16, 60), (80, 46, 150), (150, 110, 230), (210, 190, 255), (240, 255, 255)]
DUST_RAMP = [(28, 18, 48), (70, 44, 110), (120, 88, 170), (170, 150, 210), (220, 215, 240)]
res = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
os.makedirs(os.path.join(res, "item"), exist_ok=True)
os.makedirs(os.path.join(res, "block"), exist_ok=True)
recolor_item(os.path.join(ref, "certus_crystal.png"), os.path.join(res, "item", "floating_crystal.png"), CRYSTAL_RAMP)
recolor_item(os.path.join(ref, "certus_dust.png"), os.path.join(res, "item", "floating_crystal_dust.png"), DUST_RAMP)

def recolor_block(src, out):
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            bluish = b > r + 12 and lum > 110
            if bluish:
                px[x, y] = (110, 240, 255, a)
            else:
                t = lum / 255.0
                base = (58, 44, 82)
                light = (120, 104, 150)
                px[x, y] = (clamp(base[0] + (light[0]-base[0])*t),
                            clamp(base[1] + (light[1]-base[1])*t),
                            clamp(base[2] + (light[2]-base[2])*t), a)
    img.save(out)

for key in ("damaged", "chipped", "flawed", "flawless"):
    recolor_block(os.path.join(ref, key + ".png"), os.path.join(res, "block", "floating_budding_" + key + ".png"))

# preview sheet
sheet = Image.new("RGBA", (6*96 + 7*12, 96 + 2*12), (22, 24, 30, 255))
files = [os.path.join(res, "item", "floating_crystal.png"),
         os.path.join(res, "item", "floating_crystal_dust.png"),
         os.path.join(res, "block", "floating_budding_damaged.png"),
         os.path.join(res, "block", "floating_budding_chipped.png"),
         os.path.join(res, "block", "floating_budding_flawed.png"),
         os.path.join(res, "block", "floating_budding_flawless.png")]
for i, f in enumerate(files):
    tile = Image.open(f).convert("RGBA").resize((96, 96), Image.NEAREST)
    sheet.alpha_composite(tile, (12 + i*(96+12), 12))
sheet.save(r"D:\AI\voidgen-mod\docs\floating_crystals_v1.png")
print("done")