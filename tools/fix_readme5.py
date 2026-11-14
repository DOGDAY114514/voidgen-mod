import io

p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.0.4 · 单文件 mod jar（154.6 KB）", "v2.0.5 · 单文件 mod jar（155.5 KB）")
s = s.replace("> **v2.0.4 乱码修复**", """> **v2.0.5 GUI 调整**
> - 所有模组 GUI（虚无发电机 / 虚无熔炉 / 虚无收集装置 / 虚无生物生成器）改成**亮色面板**：米白底 + 深灰描边 + 青绿强调色，物品槽为浅灰底。
> - 虚无生物生成器修复翻页：右上角新增 `<` `>` 按钮，也可以用鼠标滚轮翻页，页码仍然显示「第 x/y 页」。
> - 生成器/熔炉的开关按钮、能量条、文字颜色同步改成亮色主题。

> **v2.0.4 乱码修复**""")
s = s.replace("dist/voidgen-2.0.4.jar", "dist/voidgen-2.0.5.jar")
s = s.replace("voidgen-2.0.4.jar", "voidgen-2.0.5.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("done; 2.0.4 refs left:", s.count("2.0.4"))