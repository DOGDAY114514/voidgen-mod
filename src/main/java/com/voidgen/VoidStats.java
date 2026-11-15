package com.voidgen;

import com.voidgen.item.UpgradeCardItem;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.ItemStackHandler;

/**
 * All balance numbers in one place.
 *
 * <p>Endgame target: 9.2E = 920,000,000 FE/t (the wireless transfer cap). Tier V (4^5)
 * times 12 card slots of x2 is far above the cap, so the last few cards simply saturate it.</p>
 */
public final class VoidStats {
    public static final int CARD_SLOTS = 12;
    public static final int MAX_BOUND_TARGETS = 512;
    public static final int MAX_TIER = 5;

    public static final long BASE_RATE = 1_000L;
    public static final long BASE_BUFFER = 1_000_000L;
    public static final long MAX_RATE = 920_000_000L;   // 9.2E FE/t
    public static final long MAX_BUFFER = Long.MAX_VALUE;

    public static final int RANGE_BASE = 16;
    public static final int RANGE_CARDS_INFINITE = 12;

    // ---- Void Furnace ----
    public static final int FURNACE_SLOTS = 9;
    public static final int FURNACE_CARD_SLOTS = 12;
    public static final int FURNACE_BASE_STACK = 8_192;
    public static final int FURNACE_BASE_PER_SLOT = 64;
    public static final int FURNACE_MAX_TOTAL = 8_192;
    public static final int FURNACE_WIRELESS_BASE = 16;

    /** Portable FE buffer carried by the Binding Card. */
    /** FE moved per right-click with the Binding Card. */

    private static final ResourceLocation AE_ACCELERATION = ResourceLocation.tryParse("appeng:acceleration_card");
    private static final ResourceLocation AE_CAPACITY = ResourceLocation.tryParse("appeng:capacity_card");
    private static final ResourceLocation AE_ENERGY_ACCEPTOR = ResourceLocation.tryParse("appeng:energy_acceptor");

    // AE2 15+/19+ (MC 1.20.1+/1.21.1) uses the `ae2` namespace.
    private static final ResourceLocation AE2_SPEED = ResourceLocation.tryParse("ae2:speed_card");
    private static final ResourceLocation AE2_CAPACITY = ResourceLocation.tryParse("ae2:capacity_card");
    private static final ResourceLocation AE2_ENERGY_ACCEPTOR = ResourceLocation.tryParse("ae2:energy_acceptor");

    private VoidStats() {
    }

    public static long rate(int tier, int accelerationCards, int overclockCards) {
        long value = BASE_RATE;
        for (int i = 0; i < Math.min(tier, 8); i++) {
            value *= 4L;
        }
        int boost = Math.min(20, accelerationCards + overclockCards);
        value *= 1L << boost;
        return Math.min(value, MAX_RATE);
    }

    public static long capacity(int tier, int capacityCards) {
        long value = BASE_BUFFER;
        for (int i = 0; i < Math.min(tier, 8); i++) {
            value = satMul(value, 4L);
        }
        value = satMul(value, 1L << Math.min(capacityCards, 20));
        return Math.min(value, MAX_BUFFER);
    }

    private static long satMul(long a, long b) {
        if (a <= 0L || b <= 0L) {
            return 0L;
        }
        if (a > Long.MAX_VALUE / b) {
            return Long.MAX_VALUE;
        }
        return a * b;
    }

    public static long range(int rangeCards) {
        if (rangeCards >= RANGE_CARDS_INFINITE) {
            return Long.MAX_VALUE;
        }
        long value = RANGE_BASE;
        for (int i = 0; i < Math.min(rangeCards, 11); i++) {
            value *= 4L;
        }
        return value;
    }

    public static boolean isAeEnergyAcceptor(ItemStack stack) {
        ResourceLocation key = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return idEquals(key, AE_ENERGY_ACCEPTOR) || idEquals(key, AE2_ENERGY_ACCEPTOR);
    }

    public static boolean isAeCard(ItemStack stack) {
        return typeOf(stack) != null && !(stack.getItem() instanceof UpgradeCardItem);
    }

    public static UpgradeCardItem.Type typeOf(ItemStack stack) {
        if (stack.getItem() instanceof UpgradeCardItem card) {
            return card.type();
        }
        ResourceLocation key = BuiltInRegistries.ITEM.getKey(stack.getItem());
        if (idEquals(key, AE_ACCELERATION) || idEquals(key, AE2_SPEED)) {
            return UpgradeCardItem.Type.ACCELERATION;
        }
        if (idEquals(key, AE_CAPACITY) || idEquals(key, AE2_CAPACITY)) {
            return UpgradeCardItem.Type.CAPACITY;
        }
        return null;
    }

    public static boolean isSlotCard(ItemStack stack) {
        return typeOf(stack) != null;
    }

    public static boolean isFurnaceCard(ItemStack stack) {
        UpgradeCardItem.Type type = typeOf(stack);
        return type == UpgradeCardItem.Type.ACCELERATION
                || type == UpgradeCardItem.Type.OVERCLOCK
                || type == UpgradeCardItem.Type.CAPACITY
                || type == UpgradeCardItem.Type.RANGE;
    }

    /** Total items smelted per tick: 64 per slot at base, doubled per speed card, hard cap 8192. */
    public static int furnaceRate(int accelerationCards, int overclockCards) {
        int boost = Math.min(20, accelerationCards + overclockCards);
        long total = (long) FURNACE_BASE_PER_SLOT * FURNACE_SLOTS * (1L << boost);
        return (int) Math.min(FURNACE_MAX_TOTAL, total);
    }

    /** Items held by one furnace slot: 8192 base, doubled per nest tier and per capacity card. */
    public static int furnaceCapacity(int tier, int capacityCards) {
        long value = FURNACE_BASE_STACK;
        for (int i = 0; i < Math.min(tier, 8); i++) {
            value *= 2L;
        }
        value *= 1L << Math.min(capacityCards, 20);
        return (int) Math.min(987_654_321L, value);
    }

    public static long furnaceRange(int rangeCards) {
        if (rangeCards >= RANGE_CARDS_INFINITE) {
            return Long.MAX_VALUE;
        }
        long value = FURNACE_WIRELESS_BASE;
        for (int i = 0; i < Math.min(rangeCards, 11); i++) {
            value *= 4L;
        }
        return value;
    }

    public static int count(ItemStackHandler handler, UpgradeCardItem.Type type) {
        int count = 0;
        for (int slot = 0; slot < handler.getSlots(); slot++) {
            ItemStack stack = handler.getStackInSlot(slot);
            if (typeOf(stack) == type) {
                count += stack.getCount();
            }
        }
        return count;
    }

    public static String fmt(long value) {
        return String.format("%,d", value);
    }

    /** Human-friendly magnitude for the huge generator numbers (K/M/G/T/P/E). */
    public static String fmtCompact(long value) {
        if (value < 1_000_000L) {
            return String.format("%,d", value);
        }
        if (value >= 1_000_000_000_000_000_000L) {
            return String.format("%.2fE", value / 1.0E18);
        }
        if (value >= 1_000_000_000_000_000L) {
            return String.format("%.2fP", value / 1.0E15);
        }
        if (value >= 1_000_000_000_000L) {
            return String.format("%.2fT", value / 1.0E12);
        }
        if (value >= 1_000_000_000L) {
            return String.format("%.2fG", value / 1.0E9);
        }
        return String.format("%.2fM", value / 1.0E6);
    }

    public static boolean isAeAcceptorBlock(net.minecraft.world.level.block.Block block) {
        ResourceLocation key = BuiltInRegistries.BLOCK.getKey(block);
        return idEquals(key, AE_ENERGY_ACCEPTOR) || idEquals(key, AE2_ENERGY_ACCEPTOR);
    }

    private static boolean idEquals(ResourceLocation key, ResourceLocation expected) {
        return key != null && expected != null && key.equals(expected);
    }
}
