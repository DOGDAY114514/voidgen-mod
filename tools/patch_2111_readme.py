import io, zipfile, json, tomllib
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.11.jar"
z = zipfile.ZipFile(jar)
meta = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
print("version", meta["mods"][0]["version"])
print("entries", len(z.namelist()))
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.1.10 · 单文件 mod jar（213.8 KB）", "v2.1.11 · 单文件 mod jar（213.9 KB）")
anchor = "> **v2.1.10 堆叠卡生效**"
note = "> **v2.1.11 储能上限 = long 上限**：虚无发电机内部储能上限改成 `Long.MAX_VALUE`（9,223,372,036,854,775,807 ≈ 9.22E18 FE），容量卡继续 ×2 叠加；GUI/状态栏的大数字改用 K/M/G/T/P/E 简写显示（9.22E18 → `9.22E`）。\n\n"
idx = s.find(anchor)
if idx >= 0:
    s = s[:idx] + note + s[idx:]
    print("note inserted")
s = s.replace("容量卡再 脳2^n（上限 92,000,000,000）", "容量卡再 脳2^n（上限 Long.MAX ≈ 9.22E18）")
s = s.replace("容量卡再 ×2^n（上限 92,000,000,000）", "容量卡再 ×2^n（上限 Long.MAX ≈ 9.22E18）")
s = s.replace("voidgen-2.1.10.jar", "voidgen-2.1.11.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme ok", "v2.1.11" in s, "Long.MAX" in s)