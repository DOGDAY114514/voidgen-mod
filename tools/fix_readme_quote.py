import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace('"> **v2.1.0', '> **v2.1.0')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed:", '"> **v2.1.0' not in s, "| has v2.1.0:", "> **v2.1.0" in s)