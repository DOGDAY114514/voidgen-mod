import os
root = r"D:\AI\voidgen-mod\src\main\resources"
for rel in [r"assets\voidgen\models\item\void_component.json",
            r"data\voidgen\recipe\void_component.json"]:
    p = os.path.join(root, rel)
    if os.path.exists(p):
        os.remove(p)
        print("removed", rel)