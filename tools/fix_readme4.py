import io

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.0.3 · 单文件 mod jar（154.6 KB）", "v2.0.4 · 单文件 mod jar（154.6 KB）")
s = s.replace("> **v2.0.3 虚无存储器贴图重做**", """> **v2.0.4 乱码修复**
> - 之前的编码事故把 mods.toml 的 `displayName` 里那个「—」写坏了（显示成 `Voidgen 鈥?Nothingness`）。现在整份 toml 用纯 UTF-8 重写，显示名改为 ASCII 安全的 `Voidgen - Nothingness`，不再有乱码。
> - 顺手扫描了 `src/main/resources` 下所有 json/toml：只有 mods.toml 一处损坏，已修复；中英文 lang 文件均正常。

> **v2.0.3 虚无存储器贴图重做**""")
s = s.replace("dist/voidgen-2.0.3.jar", "dist/voidgen-2.0.4.jar")
s = s.replace("voidgen-2.0.3.jar", "voidgen-2.0.4.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done; 2.0.3 refs left:", s.count("2.0.3"))