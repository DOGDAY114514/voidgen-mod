import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("方块贴图是从 AE2 原版样板供应器贴图派生的七彩循环动画（8 帧，frametime 3，插值）。\n> **v2.3.1 贴图重绘**",
              "方块贴图为七彩循环动画（8 帧，frametime 3，插值），v2.3.1 起改为六边形虚空符印构图。\n\n> **v2.3.1 贴图重绘**")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")