import io

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.0.2 · 单文件 mod jar（154.5 KB）", "v2.0.3 · 单文件 mod jar（154.6 KB）")
s = s.replace("> **v2.0.2 贴图重绘**", """> **v2.0.3 虚无存储器贴图重做**
> - 存储器改成玻璃罐形态：金属罐盖 + 等级色罐身/液体 + 液面波纹 + 玻璃高光 + 底部金属圈；铁/金/钻石/绿宝石/下界之星五色可辨。
> - 充盈版整罐发光：等级色罐身 + 白色亮芯 + 星点，和普通版一眼区分。
> - 其余贴图保持 v2.0.2。

> **v2.0.2 贴图重绘**""")
s = s.replace("dist/voidgen-2.0.2.jar", "dist/voidgen-2.0.3.jar")
s = s.replace("voidgen-2.0.2.jar", "voidgen-2.0.3.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done; 2.0.2 refs left:", s.count("2.0.2"))