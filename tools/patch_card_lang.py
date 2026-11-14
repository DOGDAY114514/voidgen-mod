import json
base = r"D:\AI\voidgen-mod\src\main\resources\assets\voidgen\lang"
en = {
    "tooltip.voidgen.binding_card.stored": "Stored void energy: %s / %s FE",
    "tooltip.voidgen.binding_card.extract": "Right-click a void generator: pull FE out",
    "tooltip.voidgen.binding_card.discharge": "Right-click a machine: push FE in",
    "status.voidgen.card_extract": "Extracted %s FE from the void generator",
    "status.voidgen.card_charge": "Transferred %s FE",
    "status.voidgen.card_full": "Binding card is full",
    "status.voidgen.card_empty_source": "The void generator has no FE stored",
    "status.voidgen.card_nothing": "The binding card has no FE stored",
    "status.voidgen.card_no_target": "The target cannot accept FE",
}
zh = {
    "tooltip.voidgen.binding_card.stored": "已存虚无能量：%s / %s FE",
    "tooltip.voidgen.binding_card.extract": "手持右键虚无发电机：抽取 FE",
    "tooltip.voidgen.binding_card.discharge": "手持右键其他机器：输出 FE",
    "status.voidgen.card_extract": "已从虚无发电机抽取 %s FE",
    "status.voidgen.card_charge": "已输出 %s FE",
    "status.voidgen.card_full": "绑定卡已满",
    "status.voidgen.card_empty_source": "虚无发电机里没有电量",
    "status.voidgen.card_nothing": "绑定卡里没有电量",
    "status.voidgen.card_no_target": "目标无法接收电量",
}
for name, extra in (("en_us.json", en), ("zh_cn.json", zh)):
    p = base + "\\" + name
    with open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    data.update(extra)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(name, len(data))