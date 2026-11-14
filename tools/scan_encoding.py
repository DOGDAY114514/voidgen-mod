import io, os

root = r"D:\AI\voidgen-mod\src\main\resources"
bad = []
for dirpath, _, files in os.walk(root):
    for n in files:
        if not n.endswith((".json", ".toml", ".mcmeta")):
            continue
        p = os.path.join(dirpath, n)
        b = open(p, "rb").read()
        notes = []
        if b[:3] == b"\xef\xbb\xbf":
            notes.append("BOM")
        try:
            s = b.decode("utf-8")
        except UnicodeDecodeError as e:
            notes.append("NOT-UTF8 %s" % e)
            s = b.decode("utf-8", errors="replace")
        for marker in ("\ufffd", "鉁", "鈥", "锟", "â€"):
            if marker in s:
                notes.append("marker %r" % marker)
                idx = s.index(marker)
                notes.append(repr(s[max(0, idx - 30):idx + 30]))
        if notes:
            bad.append((os.path.relpath(p, root), notes))
for rel, notes in bad:
    print(rel)
    for n in notes:
        print("   ", n)
print("total flagged:", len(bad))