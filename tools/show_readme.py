import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
print("\n".join(s.splitlines()[:26]))
print("---- jar refs ----")
for line in s.splitlines():
    if "voidgen-2.0." in line:
        print(line)