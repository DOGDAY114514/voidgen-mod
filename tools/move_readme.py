import io
p = r"D:\AI\voidgen-mod\README.md"
lines = io.open(p, encoding="utf-8").read().splitlines()
idx = next(i for i, ln in enumerate(lines) if "v2.3.0 虚空合成器" in ln)
hl = lines.pop(idx)
# find subtitle
si = next(i for i, ln in enumerate(lines) if ln.startswith("**Minecraft 1.21.1"))
lines.insert(si + 1, "")
lines.insert(si + 2, hl)
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("moved; lines now", len(lines))