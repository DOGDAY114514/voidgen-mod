package com.voidgen.item;

import java.util.List;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** 虚无值物品：1 个 = 1,000 虚无值；用于在 ME 网络与本模组方块之间搬运虚无值。 */
public class VoidValueItem extends Item {
    public VoidValueItem(Properties properties) {
        super(properties);
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltip, flag);
        tooltip.add(Component.translatable("tooltip.voidgen.void_value").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable("tooltip.voidgen.void_value.hint").withStyle(ChatFormatting.DARK_GRAY));
    }
}
