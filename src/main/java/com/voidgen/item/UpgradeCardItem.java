package com.voidgen.item;

import java.util.List;
import java.util.Locale;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * One of the four Voidgen upgrade cards. AE2's own acceleration / capacity cards are also
 * accepted by the generator's card slots (see {@link com.voidgen.VoidStats#typeOf}).
 */
public class UpgradeCardItem extends Item {
    public enum Type {
        ACCELERATION,
        OVERCLOCK,
        CAPACITY,
        RANGE
    }

    private final Type type;

    public UpgradeCardItem(Type type, Properties properties) {
        super(properties);
        this.type = type;
    }

    public Type type() {
        return type;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidgen.card." + type.name().toLowerCase(Locale.ROOT)));
    }
}
