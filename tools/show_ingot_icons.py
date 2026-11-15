import os
from PIL import Image
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures"
items = ["item/void_ingot.png", "item/void_ingot_block.png", "item/void_component_1k.png"]
scale = 10
pad = 12
W = pad + len(items) * (160 + pad)
img = Image.new("RGBA", (W, 160 + 2 * pad), (22, 24, 30, 255))
for i, rel in enumerate(items):
    t = Image.open(os.path.join(base, rel)).convert("RGBA")
    img.alpha_composite(t.resize((160, 160), Image.NEAREST), (pad + i * (160 + pad), pad))
out = r"D:\AI\voidgen-mod\docs\current_ingot_icons.png"
img.save(out)
print("saved", out, img.size)