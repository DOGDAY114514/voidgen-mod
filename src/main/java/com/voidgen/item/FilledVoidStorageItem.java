package com.voidgen.item;

import java.util.List;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** 充盈的虚无存储器：由存满的存储器转化而来，是收集装置/更高阶物品的合成材料。 */
public class FilledVoidStorageItem extends Item {
    private final int tier;

    public FilledVoidStorageItem(int tier, Properties properties) {
        super(properties);
        this.tier = tier;
    }

    public int tier() {
        return tier;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidgen.filled_storage"));
    }
}
