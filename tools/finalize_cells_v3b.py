import io, os, shutil
from PIL import Image

src = r"D:\AI\voidgen-mod\docs\cells_v3"
dst = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
for f in os.listdir(src):
    if f.endswith(".png"):
        shutil.copyfile(os.path.join(src, f), os.path.join(dst, f))

cells = dst
order = ["1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"]
scale = 12
px = 16 * scale
pad = 12
w = pad + len(order) * (px + pad)
img = Image.new("RGBA", (w, 2 * (px + pad) + 2 * pad), (26, 28, 34, 255))
for i, t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad))
ref = r"D:\AI\voidgen-mod\docs\ae2_ref\assets\ae2\textures\item"
row = [("cells", "void_cell_housing.png"), ("cells", "void_component.png"),
       ("ref", "item_storage_cell_1k.png"), ("ref", "item_cell_housing.png"), ("ref", "item_storage_cell_256k.png")]
for i, (kind, f) in enumerate(row):
    base = cells if kind == "cells" else ref
    img.alpha_composite(Image.open(os.path.join(base, f)).convert("RGBA").resize((px, px), Image.NEAREST),
                        (pad + i * (px + pad), pad + px + pad))
img.save(r"D:\AI\voidgen-mod\docs\ae_cells_v3.png")

# README: bump to 2.1.2 and rewrite the note line
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.1 · 单文件 mod jar（172.8 KB）", "v2.1.2 · 单文件 mod jar（176.3 KB）")
s = s.replace("dist/voidgen-2.1.1.jar", "dist/voidgen-2.1.2.jar")
s = s.replace("voidgen-2.1.1.jar", "voidgen-2.1.2.jar")
s = s.replace(
    "> **v2.1.1 贴图重绘**：虚无磁盘/元件/外壳/虚无锭 按 AE2 存储元件的构图重画——"
    "白色斜面外壳、斜向等级色带、右下角绿色指示灯，周围加虚空星点特效；对应 AE2 参考图 docs/ae2_ref/ae2_zoom.png。",
    "> **v2.1.2 贴图重绘**：虚无磁盘直接以 AE2 原版存储元件的像素轮廓为底稿——"
    "同样的圆角外壳、斜向等级色带、右下角指示灯，换成虚无配色并加星点特效；"
    "对照图见 docs/ae_cells_v3.png 与 docs/cell_1k_vs_ae2.png。")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme 2.1.2:", "v2.1.2" in io.open(p, encoding="utf-8").read())