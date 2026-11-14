import io
for p in [r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidGen.java"]:
    s = io.open(p, encoding="utf-8").read()
    print("==", p)
    for i, line in enumerate(s.splitlines(), 1):
        if any(k in line for k in ("VOID_COMPONENT", "VOID_INGOT", "VOID_CELL_HOUSING", "VOIDGEN_TAB", "COMPONENT", "cell_")):
            print(i, line)