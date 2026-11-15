import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read().replace("（244.2 KB）", "（244.8 KB）")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed size")