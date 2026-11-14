import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
print("lines:", s.count("\n"))
print("has merged:", "。> -" in s)
print("first 300:", s[:300].replace("\n", "\\n"))
i = s.find("v2.1.0")
print("---- section ----")
print(s[i-30:i+520].replace("\n", "\\n"))