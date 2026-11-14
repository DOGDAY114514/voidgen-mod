import os

root = r"D:\AI\voidgen-mod\src\main\java"
markers = ("锛", "銆", "\ufffd", "鈥", "鈭", "椋", "庢", "牸", "叧", "鍣", "鏃", "櫄", "鍝", "缁", "鐢")
for dp, _, fs in os.walk(root):
    for n in fs:
        if not n.endswith(".java"):
            continue
        p = os.path.join(dp, n)
        s = open(p, encoding="utf-8", errors="replace").read()
        hits = [(m, s.index(m)) for m in markers if m in s]
        if hits:
            print(os.path.relpath(p, root), [m for m, _ in hits])