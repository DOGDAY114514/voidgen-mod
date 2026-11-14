import os

root = r"D:\AI\voidgen-mod\src\main\java"
bad = []
for dp, _, fs in os.walk(root):
    for n in fs:
        if not n.endswith(".java"):
            continue
        p = os.path.join(dp, n)
        b = open(p, "rb").read()
        if b[:3] == b"\xef\xbb\xbf":
            bad.append((p, "BOM"))
            b = b[3:]
        try:
            s = b.decode("utf-8")
        except UnicodeDecodeError as e:
            bad.append((p, "NOT-UTF8: %s" % e))
            s = b.decode("utf-8", "replace")
        for marker in ("\ufffd", "鈥", "鈭", "锟", "铏", "鐢"):
            if marker in s:
                idx = s.index(marker)
                bad.append((p, "marker %r: %r" % (marker, s[max(0, idx-25):idx+25])))
                break
for p, why in bad:
    print(os.path.relpath(p, root), "|", why)
print("flagged:", len(bad))