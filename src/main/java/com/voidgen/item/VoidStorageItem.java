package com.voidgen.item;

import java.util.List;
import java.util.function.Supplier;

import com.voidgen.VoidValue;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** 虚无存储器：容量随等级（铁 1,000 -> 下界之星无限），存满后变成充盈版本。 */
public class VoidStorageItem extends Item {
    private final int tier;
    private final long cap;
    private final Supplier<Item> filled;

    public VoidStorageItem(int tier, long cap, Supplier<Item> filled, Properties properties) {
        super(properties);
        this.tier = tier;
        this.cap = cap;
        this.filled = filled;
    }

    public int tier() {
        return tier;
    }

    public long cap() {
        return cap;
    }

    public Item filled() {
        return filled.get();
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        long value = VoidValue.get(stack);
        tooltip.add(Component.translatable("tooltip.voidgen.store", VoidValue.format(value), cap == Long.MAX_VALUE ? "∞" : VoidValue.format(cap)));
        if (cap == Long.MAX_VALUE) {
            tooltip.add(Component.translatable("tooltip.voidgen.store.infinite"));
        } else if (value >= cap) {
            tooltip.add(Component.translatable("tooltip.voidgen.store.full"));
        } else {
            tooltip.add(Component.translatable("tooltip.voidgen.store.void_drop"));
        }
    }
}
