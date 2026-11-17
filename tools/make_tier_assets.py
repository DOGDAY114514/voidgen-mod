import io, json, os
from PIL import Image

MOD = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen"
TEX = os.path.join(MOD, "textures", "block")
MODELS = os.path.join(MOD, "models", "block")
STATES = os.path.join(MOD, "blockstates")
ITEMS = os.path.join(MOD, "models", "item")
DATA = r"D:\AI\voidgen-mod\src\main\resources\data\voidgen"
RECIPES = os.path.join(DATA, "recipe")

ACCENTS = {
    1: (255, 196, 96),
    2: (110, 232, 150),
    3: (110, 170, 255),
    4: (214, 120, 255),
    5: (255, 242, 200),
}

def recolor(src, dst, accent):
    img = Image.open(src).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            cyan = g > 135 and b > 135 and r < 190 and (g + b - 2 * r) > 90
            if not cyan:
                continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            f = 0.55 + 0.6 * (lum / 255.0)
            px[x, y] = (min(255, int(accent[0] * f)), min(255, int(accent[1] * f)),
                        min(255, int(accent[2] * f)), a)
    img.save(dst)

def write_json(path, obj):
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def model(name, top, side, bottom):
    write_json(os.path.join(MODELS, name + ".json"), {
        "parent": "minecraft:block/cube_bottom_top",
        "textures": {"top": top, "bottom": bottom, "side": side},
    })

machines = {
    "void_generator": ("void_generator_top", "void_generator_side", "void_generator_bottom"),
    "void_furnace": ("void_furnace_top", "void_furnace_side", "void_furnace_bottom"),
}
for base, (top, side, bottom) in machines.items():
    states = {"variants": {"tier=0": {"model": "voidgen:block/" + base}}}
    for tier in range(1, 6):
        for suffix, tex in (("top", top), ("side", side), ("bottom", bottom)):
            src = os.path.join(TEX, "%s_%s.png" % (base, suffix))
            dst = os.path.join(TEX, "%s_%s_t%d.png" % (base, suffix, tier))
            recolor(src, dst, ACCENTS[tier])
        m = base + "_t%d" % tier
        model(m, "voidgen:block/%s_top_t%d" % (base, tier),
              "voidgen:block/%s_side_t%d" % (base, tier),
              "voidgen:block/%s_bottom_t%d" % (base, tier))
        states["variants"]["tier=%d" % tier] = {"model": "voidgen:block/" + m}
    write_json(os.path.join(STATES, base + ".json"), states)
    print("assets for", base)

# max-tier crafting recipes: base machine + all five nest upgrades -> same block with Tier=5
nest = [{"item": "voidgen:nest_upgrade_%d" % i} for i in range(1, 6)]
for base in machines:
    recipe = {
        "type": "minecraft:crafting_shapeless",
        "category": "misc",
        "ingredients": [{"item": "voidgen:" + base}] + nest,
        "result": {
            "id": "voidgen:" + base,
            "count": 1,
            "components": {"minecraft:custom_data": {"Tier": 5}},
        },
    }
    write_json(os.path.join(RECIPES, base + "_max.json"), recipe)
    print("recipe", base + "_max")

# lang keys
for lang, text in (("en_us", "Tier: %s"), ("zh_cn", "等级: %s")):
    p = os.path.join(MOD, "lang", lang + ".json")
    obj = json.load(io.open(p, encoding="utf-8"))
    obj["tooltip.voidgen.tier"] = text
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    print("lang", lang)
print("done")