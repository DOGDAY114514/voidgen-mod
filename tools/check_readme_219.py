import json, io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
print("has 2.1.9 title:", "v2.1.9" in s, "| section:", "### 绑定卡（精准供电控制）" in s, "| old text gone:", "便携 FE 电池" not in s)
print("size line ok:", "213.7 KB" in s)