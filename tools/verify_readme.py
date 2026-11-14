import io, json
p = r"D:\AI\voidgen-mod\README.md"
b = open(p, "rb").read()
print("BOM:", b[:3] == b"\xef\xbb\xbf")
s = b.decode("utf-8")
print("first line:", json.dumps(s.splitlines()[0], ensure_ascii=True))
print("has v2.0.5 note:", "v2.0.5" in s, "| has spawner fix:", "\u7ffb\u9875" in s)
print("2.0.4 refs:", s.count("2.0.4"), "| 2.0.5 refs:", s.count("2.0.5"))