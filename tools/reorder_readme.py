import io, re

p = r"D:\AI\voidgen-mod\README.md"
text = io.open(p, encoding="utf-8").read()
lines = text.split("\n")

blocks = []
cur = []
for ln in lines:
    if ln.strip() == "":
        if cur:
            blocks.append("\n".join(cur)); cur = []
    else:
        cur.append(ln)
if cur:
    blocks.append("\n".join(cur))

def is_changelog(b):
    first = b.split("\n")[0]
    return bool(re.match(r'^>\s*(?:>\s*)?\*\*v\d', first))

def version_of(b):
    m = re.search(r'\*\*v(\d+)\.(\d+)\.(\d+)', b)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)

body = [b for b in blocks if b.strip() != ">" and not is_changelog(b)]
logs = [b for b in blocks if is_changelog(b)]
logs.sort(key=version_of, reverse=True)

out = "\n\n".join(body).rstrip() + "\n\n## 更新日志\n\n" + "\n\n".join(logs).rstrip() + "\n"
io.open(p, "w", encoding="utf-8", newline="\n").write(out)
print("body blocks:", len(body), "changelog blocks:", len(logs))
print("first line:", out.split("\n")[0])