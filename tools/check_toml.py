import io, os
p = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
b = open(p, "rb").read()
print("BOM:", b[:3] == b"\xef\xbb\xbf", "size", len(b))
s = b.decode("utf-8", errors="replace")
for line in s.splitlines():
    if any(ch in line for ch in ("displayName", "description", "Voidgen", "Nothingness", "虚无")):
        print(repr(line))