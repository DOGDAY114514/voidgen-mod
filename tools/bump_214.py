import io, os
from PIL import Image

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.3"', 'version="2.1.4"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)

bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.3.jar", "voidgen-2.1.4.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.3 · 单文件 mod jar（176.3 KB）", "v2.1.4 · 单文件 mod jar（176.6 KB）")
s = s.replace("dist/voidgen-2.1.3.jar", "dist/voidgen-2.1.4.jar")
s = s.replace("voidgen-2.1.3.jar", "voidgen-2.1.4.jar")
s = s.replace("**虚无元件**（虚无锭 + 红石块 + 末影珍珠）",
              "**虚无元件 1K~256M**（10 个等级；1K = 虚无锭 + 红石块 + 末影珍珠，之后用上一级元件 + 虚无锭 + 材料逐级升）")
s = s.replace(" 10 个磁盘", " 10 个磁盘（每个磁盘吃同等级的虚无元件）")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)

# combined sheet: disks row + components row
cells = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
order = ["1k","4k","16k","64k","256k","1m","4m","16m","64m","256m"]
scale = 12
px = 16*scale
pad = 12
w = pad + len(order)*(px+pad)
img = Image.new("RGBA", (w, 2*(px+pad)+2*pad), (26,28,34,255))
for i,t in enumerate(order):
    img.alpha_composite(Image.open(os.path.join(cells, f"void_cell_{t}.png")).convert("RGBA").resize((px,px), Image.NEAREST), (pad+i*(px+pad), pad))
    img.alpha_composite(Image.open(os.path.join(cells, f"void_component_{t}.png")).convert("RGBA").resize((px,px), Image.NEAREST), (pad+i*(px+pad), pad+px+pad))
img.save(r"D:\AI\voidgen-mod\docs\void_disks_components.png")
print("sheet saved")