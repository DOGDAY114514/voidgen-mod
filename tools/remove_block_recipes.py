import glob, os
base = r"D:\AI\voidgen-mod\src\main\resources\data\voidgen\recipe"
for f in sorted(glob.glob(os.path.join(base, "processor_*_from_blocks.json"))):
    os.remove(f)
    print("removed", f)
print("remaining recipes:", len(glob.glob(os.path.join(base, "*.json"))))