import io
toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.3"', 'version="2.3.4"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.3.jar", "voidgen-2.3.4.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("# Voidgen v2.3.3 ·", "# Voidgen v2.3.4 ·")
s = s.replace("v2.3.3 · 单文件 mod jar（241.9 KB）", "v2.3.4 · 单文件 mod jar（242.1 KB）")
s = s.replace("voidgen-2.3.3.jar", "voidgen-2.3.4.jar")
s = s.replace(
    "接入 ME 网络后把 AE2 处理器（逻辑/运算/工程）样板直接「虚空合成」：不消耗材料、不需要机器、瞬间把产物塞进 ME 存储。",
    "接入 ME 网络后把 AE2 处理器（逻辑/运算/工程）样板直接「虚空合成」：不需要机器、瞬间把产物塞进 ME 存储；样板输入材料照常从 ME 网络扣除（会消耗材料），产物放不下时整批失败并退回材料。")
old = "> **v2.3.3 贴图渐变**"
new = "> **v2.3.4 修正消耗材料说明**：虚空合成器不是凭空产出——CPU 推送样板前已从 ME 网络抽取该样板所需的输入材料，返回成功即消耗；产物放不下时先模拟再决定，不会出现「材料退回但产物已进存储」的复制 bug。\n>\n" + old
s = s.replace(old, new, 1)
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.3.4 + readme")