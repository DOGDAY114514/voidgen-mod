import zipfile, json
jar = r"D:\AI\voidgen-mod\dist\voidgen-2.1.8.jar"
with zipfile.ZipFile(jar) as z:
    names = z.namelist()
    en = json.loads(z.read("assets/voidgen/lang/en_us.json"))
    zh = json.loads(z.read("assets/voidgen/lang/zh_cn.json"))
    print("entries", len(names), "version", b'version="2.1.8"' in z.read("META-INF/neoforge.mods.toml"))
    print("lang", len(en), len(zh), set(en)==set(zh))
    for k in ["tooltip.voidgen.binding_card.stored","status.voidgen.card_extract","status.voidgen.card_charge"]:
        print(k, k in en, k in zh)
    print("BindingCardItem has useOn:", "useOn" in z.read("com/voidgen/item/BindingCardItem.class").decode("latin1"))