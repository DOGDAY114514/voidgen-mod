import io, json, os

MODELS = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\models\block"

def face(tex, uv=None):
    f = {"texture": "#" + tex}
    if uv:
        f["uv"] = uv
    return f

def cube(frm, to, up="#top", down="#bottom", side="#side", uv=None):
    return {
        "from": frm, "to": to,
        "faces": {
            "down": face("bottom" if down == "#bottom" else down, uv),
            "up": face("top" if up == "#top" else up, uv),
            "north": face("side" if side == "#side" else side, uv),
            "south": face("side" if side == "#side" else side, uv),
            "west": face("side" if side == "#side" else side, uv),
            "east": face("side" if side == "#side" else side, uv),
        },
    }

def build(tier):
    els = [cube([0, 0, 0], [16, 16, 16])]
    if tier >= 1:
        els.append(cube([3, 16, 3], [13, 18, 13], up="#top", down="#side", side="#side", uv=[0, 0, 16, 16]))
    if tier >= 2:
        for (x, z) in ((1, 1), (13, 1), (1, 13), (13, 13)):
            els.append(cube([x, 16, z], [x + 2, 19, z + 2], uv=[2, 2, 14, 14]))
    if tier >= 3:
        for (x, z) in ((1, 1), (13, 1), (1, 13), (13, 13)):
            els.append(cube([x, 0, z], [x + 2, 16, z + 2], uv=[4, 4, 12, 12]))
    if tier >= 4:
        for (frm, to) in (([2, 16, 2], [14, 18, 4]), ([2, 16, 12], [14, 18, 14]),
                          ([2, 16, 4], [4, 18, 12]), ([12, 16, 4], [14, 18, 12])):
            els.append(cube(frm, to, uv=[4, 4, 12, 12]))
    if tier >= 5:
        for (x, z) in ((2, 2), (11, 2), (2, 11), (11, 11)):
            els.append(cube([x, 20, z], [x + 3, 22, z + 3], uv=[6, 6, 10, 10]))
    return {
        "textures": {
            "particle": "#side",
            "top": "#top",
            "bottom": "#bottom",
            "side": "#side",
        },
        "elements": els,
    }

def write(path, obj):
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

for base in ("void_generator", "void_furnace"):
    for tier in range(1, 6):
        m = build(tier)
        # resolve texture refs to concrete files
        m["textures"] = {
            "particle": "voidgen:block/%s_side_t%d" % (base, tier),
            "top": "voidgen:block/%s_top_t%d" % (base, tier),
            "bottom": "voidgen:block/%s_bottom_t%d" % (base, tier),
            "side": "voidgen:block/%s_side_t%d" % (base, tier),
        }
        # texture keys must match the #refs used in faces
        m["textures"]["top"] = "voidgen:block/%s_top_t%d" % (base, tier)
        write(os.path.join(MODELS, "%s_t%d.json" % (base, tier)), m)
print("tier models written with geometry")