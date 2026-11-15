import io, os, json
# guide text
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\client\VoidGuideScreen.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace('body("空手右击查看阶数/发电/储能/范围；绑定卡可对单台机器「解除」或「强制」供电。");',
              'body("空手右击查看阶数/发电/储能/范围；无线供电会自动连接范围内的机器，并跨维度给其他维度里已加载的机器供电。");')
s = s.replace('body("Shift + 滚轮（世界中）：绑定卡的自动连接开关。");',
              'body("无线供电：范围内的机器、以及其他维度里已加载的机器都会自动接上，不需要绑定卡。");')
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
# remove card-only lang keys
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang"
remove = {
 "gui.voidgen.accessory", "gui.voidgen.auto_off", "gui.voidgen.auto_on", "gui.voidgen.bound",
 "item.voidgen.binding_card",
 "status.voidgen.already_equipped", "status.voidgen.auto_disabled", "status.voidgen.auto_enabled",
 "status.voidgen.bound", "status.voidgen.bound_full", "status.voidgen.equipped",
 "status.voidgen.unbound", "status.voidgen.unequipped",
 "status.voidgen.card_bound", "status.voidgen.card_unbound", "status.voidgen.card_not_bound",
 "tooltip.voidgen.binding_card", "tooltip.voidgen.binding_card.bound", "tooltip.voidgen.binding_card.unbound",
 "tooltip.voidgen.binding_card.usage",
}
counts = {}
for loc in ("en_us", "zh_cn"):
    fp = os.path.join(base, loc + ".json")
    data = json.loads(io.open(fp, encoding="utf-8").read())
    before = len(data)
    for k in list(data):
        if k in remove:
            del data[k]
    io.open(fp, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    counts[loc] = (before, len(data))
print("lang:", counts)