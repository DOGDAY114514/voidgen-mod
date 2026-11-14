import io, json, os, zipfile
root = r"D:\AI\voidgen-mod"
toml = os.path.join(root, "src", "main", "resources", "META-INF", "neoforge.mods.toml")
s = io.open(toml, encoding="utf-8").read().replace('version="2.3.5"', 'version="2.3.6"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = os.path.join(root, "tools", "build.ps1")
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.3.5.jar", "voidgen-2.3.6.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
for name in ["processor_logic_from_blocks", "processor_engineering_from_blocks", "processor_calculation_from_blocks"]:
    p = os.path.join(root, "src", "main", "resources", "data", "voidgen", "recipe", name + ".json")
    json.loads(io.open(p, encoding="utf-8").read())
print("bumped 2.3.6, recipes parse")