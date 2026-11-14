import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read().replace("v2.1.8 · 单文件 mod jar（213.9 KB）", "v2.1.8 · 单文件 mod jar（214.1 KB）")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("size fixed")