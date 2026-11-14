import io, json, os, re, zipfile
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.2.2.jar"
z = zipfile.ZipFile(jar)
n = z.namelist()
print("entries", len(n), "version 2.2.2:", b'version="2.2.2"' in z.read("META-INF/neoforge.mods.toml"))
en = json.loads(z.read("assets/voidgen/lang/en_us.json")); zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
print("lang", len(en), len(zh), "void line", "status.voidgen.void_value_line" in en and "status.voidgen.void_value_line" in zh)
kb = os.path.getsize(jar)/1024.0
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = re.sub(r"v2\.2\.1 · 单文件 mod jar（[0-9.]+ KB）", "v2.2.2 · 单文件 mod jar（%.1f KB）" % kb, s)
note = "> - **v2.2.2**：发电机跨维度无线供电（同坐标范围外、所有已加载维度内玩家放置的接收机器都能收到）；空手右击发电机新增「虚无值」显示。\n"
s = s.replace("> - **v2.2.1**：", note + "> - **v2.2.1**：")
s = s.replace("voidgen-2.2.1.jar", "voidgen-2.2.2.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README 2.2.2, %.1f KB" % kb)