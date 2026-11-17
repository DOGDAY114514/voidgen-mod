import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidPowerNetwork.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace("IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);",
              "IEnergyStorage target = energy(level, pos);")
s = s.replace("if (level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null) != null) {",
              "if (energy(level, pos) != null) {")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("replaced")