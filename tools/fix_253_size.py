import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read().replace("（246.0 KB）", "（246.7 KB）")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("size fixed")