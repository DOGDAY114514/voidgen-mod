import io, zipfile, json, tomllib
p = r"D:\AI\voidgen-mod\dist\voidgen-2.1.10.jar"
z = zipfile.ZipFile(p)
meta = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
print("version", meta["mods"][0]["version"])
en = json.loads(z.read("assets/voidgen/lang/en_us.json")); zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang", len(en), len(zh), set(en) == set(zh))
print("leaks", [n for n in z.namelist() if n.startswith(("appeng/", "net/neoforged/", "com/mojang/", "io/netty/"))])
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
s = s.replace("v2.1.9 · 单文件 mod jar（213.7 KB）", "v2.1.10 · 单文件 mod jar（213.8 KB）")
anchor = "> **v2.1.9 绑定卡改为"
note = "> **v2.1.10 堆叠卡生效**：卡片槽里同一格的堆叠数量现在全额计入 —— 同格 5 张加速卡 = 5 张的效果，发电机/熔炉的所有卡片（加速/超频/容量/范围）都按**卡的总张数**计算。\n\n"
idx = s.find(anchor)
if idx >= 0:
    s = s[:idx] + note + s[idx:]
    print("note inserted")
else:
    print("anchor missing")
s = s.replace("voidgen-2.1.9.jar", "voidgen-2.1.10.jar")
io.open(readme, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")