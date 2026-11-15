import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("单文件 mod jar（244.1 KB）", "单文件 mod jar（249.1 KB）")
s = s.replace("voidgen-2.3.7.jar", "voidgen-2.3.8.jar")
guide = """## 游戏内说明（G 键）

- 进游戏后按 **G** 打开「Voidgen 使用说明」窗口：滚轮 / ↑ ↓ / PageUp PageDown 滚动，Esc 或再按 G 关闭。
- 窗口内分节列出：虚无发电机、虚无值系统、虚无熔炉、AE2 联动（磁盘 / ME 供应器 / 虚空合成器）、常用按键。
- 按键可以在「选项 → 控制 → Voidgen」里改。

"""
s = s.replace("## 玩法\n", guide + "## 玩法\n", 1)
s = s.replace("## 更新日志\n\n", "## 更新日志\n\n> **v2.3.8 游戏内说明**：新增 G 键使用说明窗口（`VoidGuideScreen`）——分节介绍发电机、虚无值系统、熔炉、AE2 联动与按键；滚轮 / 方向键滚动，Esc 或再按 G 关闭。\n\n", 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")