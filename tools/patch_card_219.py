import io, json

root = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang"
new = {
    "en_us": {
        "tooltip.voidgen.binding_card.bound": "Linked generator: %s",
        "tooltip.voidgen.binding_card.unbound": "Unlinked - right-click a Void Generator",
        "tooltip.voidgen.binding_card.usage": "Right-click a block: exclude / force-link its supply",
        "status.voidgen.card_bound": "Binding card linked to Void Generator (%s)",
        "status.voidgen.card_unbound": "Binding card unlinked",
        "status.voidgen.card_not_bound": "Link the card to a Void Generator first",
        "status.voidgen.card_dim": "Card and generator are in different dimensions",
        "status.voidgen.card_lost": "Linked generator no longer exists",
        "status.voidgen.card_excluded": "Stopped supplying this block",
        "status.voidgen.card_restored": "Restored default supply for this block",
        "status.voidgen.card_forced": "Force-linked this block (out-of-range supply)",
        "status.voidgen.card_force_removed": "Removed the force link for this block",
        "status.voidgen.card_no_energy": "This block does not accept void power"
    },
    "zh_cn": {
        "tooltip.voidgen.binding_card.bound": "已绑定发电机：%s",
        "tooltip.voidgen.binding_card.unbound": "未绑定 —— 右键虚无发电机绑定",
        "tooltip.voidgen.binding_card.usage": "右键方块：解除 / 强制绑定该方块的供电",
        "status.voidgen.card_bound": "绑定卡已绑定虚无发电机（%s）",
        "status.voidgen.card_unbound": "绑定卡已解除绑定",
        "status.voidgen.card_not_bound": "请先用绑定卡右键虚无发电机",
        "status.voidgen.card_dim": "绑定卡与发电机不在同一维度",
        "status.voidgen.card_lost": "绑定的发电机已不存在",
        "status.voidgen.card_excluded": "已停止向该方块供电",
        "status.voidgen.card_restored": "已恢复该方块的默认供电",
        "status.voidgen.card_forced": "已强制绑定该方块（无视范围供电）",
        "status.voidgen.card_force_removed": "已取消该方块的强制绑定",
        "status.voidgen.card_no_energy": "该方块不接受虚无供电"
    }
}
for lang, add in new.items():
    p = root + "\\" + lang + ".json"
    data = json.load(io.open(p, encoding="utf-8"))
    drop = [k for k in data if k.startswith("tooltip.voidgen.binding_card.")
            or k in ("status.voidgen.card_full", "status.voidgen.card_extract", "status.voidgen.card_empty_source",
                     "status.voidgen.card_nothing", "status.voidgen.card_charge", "status.voidgen.card_no_target")]
    for k in drop:
        del data[k]
    data.update(add)
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(lang, "keys", len(data))

stats = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidStats.java"
s = io.open(stats, encoding="utf-8").read()
import re
s = re.sub(r"\n[ \t]*public static final long BINDING_CARD_(CAPACITY|TRANSFER) = [^\n]*\n", "\n", s)
io.open(stats, "w", encoding="utf-8", newline="\n").write(s)

toml = r"D:\AI\voidgen-mod\src\main\resources\META-INF\neoforge.mods.toml"
s = io.open(toml, encoding="utf-8").read().replace('version="2.1.8"', 'version="2.1.9"')
io.open(toml, "w", encoding="utf-8", newline="\n").write(s)
bp = r"D:\AI\voidgen-mod\tools\build.ps1"
s = io.open(bp, encoding="utf-8").read().replace("voidgen-2.1.8.jar", "voidgen-2.1.9.jar")
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)
print("bumped 2.1.9")