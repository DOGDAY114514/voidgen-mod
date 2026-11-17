package com.voidgen.item;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.block.Block;

import java.util.List;

public class VoidFurnaceItem extends BlockItem {
    public VoidFurnaceItem(Block block, Properties properties) {
        super(block, properties);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        int tier = data == null ? 0 : data.copyTag().getInt("Tier");
        if (tier > 0) {
            tooltip.add(Component.translatable("tooltip.voidgen.tier", tier));
        }
        tooltip.add(Component.translatable("tooltip.voidgen.void_furnace").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable("tooltip.voidgen.void_furnace.controls").withStyle(ChatFormatting.DARK_GRAY));
    }
}
