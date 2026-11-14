import os
root = r"D:\AI\voidgen-mod\docs\ae2_ref\assets"
for dirpath, dirnames, filenames in os.walk(root):
    for f in filenames:
        p = os.path.join(dirpath, f)
        print(os.path.relpath(p, root), os.path.getsize(p))