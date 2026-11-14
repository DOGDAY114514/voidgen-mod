import io, os
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.2"', 'version="2.1.3"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)

bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.2.jar", "voidgen-2.1.3.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.2 · 单文件 mod jar（176.3 KB）", "v2.1.3 · 单文件 mod jar（176.3 KB）")
s = s.replace("dist/voidgen-2.1.2.jar", "dist/voidgen-2.1.3.jar")
s = s.replace("voidgen-2.1.2.jar", "voidgen-2.1.3.jar")
s = s.replace(
    "> **v2.1.2 贴图重绘**：虚无磁盘直接以 AE2 原版存储元件的像素轮廓为底稿——"
    "同样的圆角外壳、斜向等级色带、右下角指示灯，换成虚无配色并加星点特效；"
    "对照图见 docs/ae_cells_v3.png 与 docs/cell_1k_vs_ae2.png。",
    "> **v2.1.3 贴图重绘**：虚无磁盘/虚无元件/磁盘外壳直接以 AE2 原版像素为底稿——"
    "磁盘复用 AE2 存储元件的圆角外壳+斜向色带+指示灯骨架，虚无元件复用 AE2 256K 组件的方形 PCB+点阵，"
    "统一换虚无配色并加星点特效；对照图见 docs/ae_cells_v3.png、docs/cell_1k_vs_ae2.png、docs/component_vs_ae2.png。")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.1.3")