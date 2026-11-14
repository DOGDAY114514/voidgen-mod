import io
p = r"D:\AI\voidgen-mod\README.md"
lines = io.open(p, encoding="utf-8").read().splitlines()
for i, ln in enumerate(lines):
    if "虚空合成器" in ln or "v2.3.0" in ln:
        print(i + 1, ln[:110])