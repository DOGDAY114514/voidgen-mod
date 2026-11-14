import io
readme = r"D:\AI\voidgen-mod\README.md"
s = io.open(readme, encoding="utf-8").read()
print("\n".join(s.splitlines()[:18]))