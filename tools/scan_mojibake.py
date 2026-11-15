import io
p = r"D:\AI\voidgen-mod\README.md"
lines = io.open(p, encoding="utf-8").read().split("\n")
bad = []
for i, line in enumerate(lines, 1):
    if any(ch in line for ch in "锛鍙铏鐨鐢鐜鐣缂缁纾纭缁涓鏄鏃璇閫鑳鑺閿闂鍏寮瀹涓"):
        bad.append((i, line[:80]))
print("suspicious lines:", len(bad))
for i, t in bad[:20]:
    print(i, t)