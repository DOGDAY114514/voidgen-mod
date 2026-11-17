import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\client\VoidGuideScreen.java"
s = io.open(p, encoding="utf-8").read()
old = 'body("空手右击查看阶数/发电/储能/范围；绑定卡可对单台机器「解除」或「强制」'
if old in s:
    s = s.replace(old, 'body("空手右击查看阶数/发电/储能/范围；升级过的机器拆掉会保留等级，再放下仍是原等级外观。'
                          '每个等级方块外观不同；也可以直接用「机器 + 五个套娃」合成满级。', 1)
else:
    pass
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("guide updated")