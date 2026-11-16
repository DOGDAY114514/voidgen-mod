import io
p = r"D:\AI\voidgen-mod\README.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("v2.6.1 · 单文件 mod jar（249.9 KB）", "v2.6.2 · 单文件 mod jar（250.7 KB）")
s = s.replace("voidgen-2.6.1.jar", "voidgen-2.6.2.jar")
entry = (
    "### v2.6.2 虚空合成器卡任务修复\n"
    "> **原因**：AE2 合成 CPU 是在 `pushPattern` 返回**之后**才把期望产物登记进 waitingFor。旧实现同步把产物塞进 ME 存储，CPU 还没开始等，产物已经进了存储 → 等待列表永远清不掉，任务一直“请求中”。\n"
    "> **修复**：产物改为延后 1 tick 注入（`TickTask`），等 CPU 登记 waitingFor 后再插入；CPU 作为存储提供者会先截获这些产物并结单。若存储放不下，余量进入供应器回流仓，不会掉落。旧版本卡住的任务需要先取消再重新下单。\n\n"
)
marker = "## 更新日志\n\n"
assert marker in s
s = s.replace(marker, marker + entry, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("readme updated")