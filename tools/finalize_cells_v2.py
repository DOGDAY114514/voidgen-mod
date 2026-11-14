import io, os
from PIL import Image

cells = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
order = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
scale = 10
px = 16 * scale
pad = 12
w = pad + 10 * (px + pad)
h = pad * 3 + 2 * (px + pad)
img = Image.new("RGBA", (w, h), (26, 28, 34, 255))
for i, t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad))
extras = ["void_ingot.png", "void_component.png", "void_cell_housing.png"]
for i, f in enumerate(extras):
    img.alpha_composite(Image.open(os.path.join(cells, f)).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad + px + pad))
for i, f in enumerate(["item_storage_cell_1k.png", "item_cell_housing.png", "item_storage_cell_256k.png"]):
    img.alpha_composite(Image.open(os.path.join(ref, f)).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + (i + 4) * (px + pad), pad + px + pad))
out = r"D:\AI\voidgen-mod\docs\ae_cells_v2.png"
img.save(out)
print("saved", out, img.size)

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.0 · 单文件 mod jar（173.0 KB）", "v2.1.1 · 单文件 mod jar（172.8 KB）")
s = s.replace("dist/voidgen-2.1.0.jar", "dist/voidgen-2.1.1.jar")
s = s.replace("voidgen-2.1.0.jar", "voidgen-2.1.1.jar")
note = ("> **v2.1.1 贴图重绘**：虚无磁盘/元件/外壳/虚无锭 按 AE2 存储元件的构图重画——"
        "白色斜面外壳、斜向等级色带、右下角绿色指示灯，周围加虚空星点特效；对应 AE2 参考图 docs/ae2_ref/ae2_zoom.png。\n\n")
s = s.replace("> **v2.1.0 新增 · AE2 虚无磁盘", note + "> **v2.1.0 新增 · AE2 虚无磁盘", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
s2 = io.open(p, encoding="utf-8").read()
print("readme v2.1.1:", "v2.1.1" in s2, "| note:", "贴图重绘" in s2)