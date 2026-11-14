import io, os
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.2.0.jar"
size = os.path.getsize(jar)
kb = size / 1024.0
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("# Voidgen v2.1", "# Voidgen v2.2", 1)
import re
s = re.sub(r"v2\.1\.11 · 单文件 mod jar（[0-9.]+ KB）", "v2.2.0 · 单文件 mod jar（%.1f KB）" % kb, s)
section = """> **v2.2.0 ME 虚无供应器**：新增方块「ME 虚无供应器」与物品「虚无值」（1 个 = 1,000 虚无值）。
> - SUPPLY 模式（默认）：消耗槽内「虚无值」物品，把虚无值推给半径 16 格内的虚无发电机 / 虚无熔炉（每台 200/t，总预算 4,000/t）。
> - IMPORT 模式：从相邻的虚无收集装置抽虚无值，填成「虚无值」物品（最多 64 个/批），ME 输入总线可把它吸进 AE；虚无值存进虚无磁盘，在 AE 终端可见。
> - 右击方块切换模式；ME 输入/输出总线都可访问它的槽位（需要 AE2）。
> - 贴图为 8 帧动画：三色端口 + 移动光条 + 变色核心。
>
"""
s = s.replace("> **v2.1.5 分级虚无元件**", section + "> **v2.1.5 分级虚无元件**", 1)
s = s.replace("voidgen-2.1.11.jar", "voidgen-2.2.0.jar")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README updated, jar %.1f KB" % kb)