import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\block\MeVoidSupplierBlock.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace("    public void playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {",
              "    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {")
s = s.replace("        super.playerWillDestroy(level, pos, state, player);\n    }",
              "        return super.playerWillDestroy(level, pos, state, player);\n    }")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("fixed playerWillDestroy")