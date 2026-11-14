import io, json, os

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
size_kb = os.path.getsize(r"D:\AI\voidgen-mod\dist\voidgen-2.1.0.jar") / 1024.0

s = s.replace("# Voidgen v2.0 · 虚无发电机 + 虚无熔炉 + 虚无值系统",
              "# Voidgen v2.1 · 虚无发电机 + 虚无熔炉 + 虚无值系统 + AE2 虚无磁盘")
s = s.replace("**Minecraft 1.21.1 · NeoForge 21.1.x · v2.0.5 · 单文件 mod jar（155.5 KB）**",
              "**Minecraft 1.21.1 · NeoForge 21.1.x · v2.1.0 · 单文件 mod jar（%.1f KB）**" % size_kb)

anchor = "> **v2.0.5 GUI 调整**"
block = """"> **v2.1.0 新增 · AE2 虚无磁盘（1K~256M）**\n> \n> - 新增材料：**虚无锭**（充盈的虚无存储器·绿宝石 + 下界之星 + 钻石块 → 8 锭）、**虚无元件**（虚无锭 + 红石块 + 末影珍珠）、**虚无磁盘外壳**（玻璃 + 虚无锭 + 铁锭/铜锭）。\n> - **虚无磁盘 1K / 4K / 16K / 64K / 256K / 1M / 4M / 16M / 64M / 256M**：按 AE2 存储元件的方式实现（`BasicStorageCell`），放进 ME 驱动器/ME 箱子就能当 AE2 存储元件用。磁盘越大，合成时需要的虚无锭越多（1M 以上还要钻石块 / 绿宝石块 / 下界合金锭 / 下界之星）。\n> - 需要 AE2 19.x：没装 AE2 时磁盘退化为无功能占位物品，磁盘配方也不会加载（`neoforge:mod_loaded` 条件）。\n> - 贴图参考 AE2 存储元件：深灰外壳 + 斜向等级色色带 + 容量点阵 + 周围星点特效；10 个等级颜色递进。预览：[docs/ae_cells_v1.png](docs/ae_cells_v1.png)\n\n"""
s = s.replace(anchor, block + anchor, 1)

s = s.replace("dist/voidgen-2.0.5.jar", "dist/voidgen-2.1.0.jar")
s = s.replace("voidgen-2.0.5.jar", "voidgen-2.1.0.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated, size %.1f KB" % size_kb)