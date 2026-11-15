import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("**Minecraft 1.21.1 · NeoForge 21.1.x · 单文件 mod jar（246.7 KB）**",
              "**Minecraft 1.21.1 · NeoForge 21.1.x · v2.6.0 · 单文件 mod jar（249.9 KB）**")
s = s.replace("voidgen-2.5.3.jar", "voidgen-2.6.0.jar")
entry = (
    "### v2.6.0 虚无存储组件重做 + 虚浮处理器\n"
    "> **改名与配方重排**：1K~256M 改名为「虚无存储组件」，配方照 AE2 原版元件顺序重做——赛特斯石英换成虚浮水晶，荧石粉换成煤粉（16K 起），1M~256M 的两枚处理器换成虚浮处理器。\n"
    "> **新物品**：虚浮处理器（水晶装配器：虚无电路板×4 + 硅板×4 + 煤粉×4 → 4）；虚无电路板（切片器：虚无块 → 4 块电路板）。\n"
    "> **虚无块**：改为 2×2 虚浮水晶合成 1 块（替换旧的 9 锭配方）。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s, "changelog header missing"
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")