import io
p = r"D:\AI\voidgen-mod\README.md"
lines = io.open(p, encoding="utf-8").read().split("\n")
print("total lines:", len(lines))
for i, ln in enumerate(lines, 1):
    if ln.startswith("## "):
        print(i, ln)
print("changelog headings:", sum(1 for ln in lines if ln.startswith("> **v")))