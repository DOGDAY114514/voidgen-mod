import io, json, os, zipfile

mods = r"F:\Release 2.4.4\.minecraft\versions\New Age Tech Sky\mods"
hits = []
for name in sorted(os.listdir(mods)):
    if not name.endswith(".jar"):
        continue
    path = os.path.join(mods, name)
    try:
        with zipfile.ZipFile(path) as z:
            for entry in z.namelist():
                if entry.endswith(("lang/zh_cn.json", "lang/en_us.json")):
                    try:
                        data = json.loads(z.read(entry).decode("utf-8"))
                    except Exception:
                        continue
                    for k, v in data.items():
                        if isinstance(v, str) and ("反应仓" in v or "Reaction Chamber" in v):
                            hits.append((name, entry, k, v))
    except Exception as e:
        pass
for h in hits[:30]:
    print(h)