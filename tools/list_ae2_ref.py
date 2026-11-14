import os
from PIL import Image

ref = r"D:\AI\voidgen-mod\docs\ae2_ref"
files = sorted(os.listdir(ref))
print("\n".join(files))