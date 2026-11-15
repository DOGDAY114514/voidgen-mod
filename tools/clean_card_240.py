import io, os, re
root = r"D:\AI\voidgen-mod\src\main\java\com\voidgen"
# delete accessory + card classes
for rel in ("VoidAccessory.java", "item/BindingCardItem.java"):
    p = os.path.join(root, rel)
    if os.path.exists(p):
        os.remove(p)
        print("deleted", rel)
# VoidStats: drop binding card helper + import
p = os.path.join(root, "VoidStats.java")
s = io.open(p, encoding="utf-8").read()
s = s.replace("import com.voidgen.item.BindingCardItem;\n", "")
s = s.replace("""    public static boolean isBindingCard(ItemStack stack) {
        return stack.getItem() instanceof BindingCardItem;
    }

""", "")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("VoidStats cleaned")
# remaining references
for dirpath, _, files in os.walk(root):
    for f in files:
        if f.endswith(".java"):
            fp = os.path.join(dirpath, f)
            t = io.open(fp, encoding="utf-8").read()
            for key in ("BindingCard", "VoidAccessory"):
                if key in t:
                    print("ref", key, fp)