import io, os
from PIL import Image

# refresh the item comparison sheet against AE2 refs
tex = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\textures\item"
ref = r"D:\AI\voidgen-mod\docs\ref_processor"
scale = 10; cell = 16*scale; pad = 12
sheet = Image.new("RGBA", (2*cell + 3*pad, 2*cell + 3*pad), (22,24,30,255))
ours = ["void_processor", "void_circuit_board"]
refs = ["logic_processor.png", "printed_logic_processor.png"]
for i, n in enumerate(ours):
    img = Image.open(os.path.join(tex, n + ".png")).convert("RGBA").resize((cell, cell), Image.NEAREST)
    sheet.alpha_composite(img, (pad + i*(cell+pad), pad))
for i, n in enumerate(refs):
    img = Image.open(os.path.join(ref, n)).convert("RGBA").resize((cell, cell), Image.NEAREST)
    sheet.alpha_composite(img, (pad + i*(cell+pad), cell + 2*pad))
sheet.save(r"D:\AI\voidgen-mod\docs\void_processor_refs.png")

# README update
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.6.0 · 单文件 mod jar（249.9 KB）", "v2.6.1 · 单文件 mod jar（249.9 KB）")
s = s.replace("voidgen-2.6.0.jar", "voidgen-2.6.1.jar")
entry = (
    "### v2.6.1 处理器与电路板贴图\n"
    "> **参考 AE2 逻辑处理器 / 印刷逻辑电路**：虚浮处理器改成 AE2 逻辑处理器的等轴芯片造型（深紫芯片体 + 青色指示灯 + 金色引脚）；虚无电路板改成 AE2 印刷电路板的板卡造型（紫罗兰渐变板面 + 金色引脚），只保留轮廓与引脚位置，颜色与细节全部换成虚无配色。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")