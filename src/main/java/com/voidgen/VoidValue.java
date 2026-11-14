package com.voidgen;

import net.minecraft.core.NonNullList;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;

import com.voidgen.item.VoidStorageItem;

/**
 * 虚无值 helpers: storage item data, player inventory fill/drain, mob spawn costs.
 * All 虚无值 lives on storage items (NBT via CUSTOM_DATA), never on the player entity.
 */
public final class VoidValue {
    public static final String KEY = "VoidValue";
    public static final long BASE_COLLECTOR_BUFFER = 1_000_000L;
    public static final long DISTRIBUTOR_BUFFER = 100_000L;
    public static final long MACHINE_BUFFER = 10_000L;
    public static final int DISTRIBUTOR_RADIUS = 16;

    private VoidValue() {
    }

    public static CompoundTag tag(ItemStack stack) {
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
    }

    public static void setTag(ItemStack stack, CompoundTag tag) {
        if (tag.isEmpty()) {
            stack.remove(DataComponents.CUSTOM_DATA);
        } else {
            stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
        }
    }

    public static long get(ItemStack stack) {
        if (!(stack.getItem() instanceof VoidStorageItem)) {
            return 0L;
        }
        return Math.max(0L, tag(stack).getLong(KEY));
    }

    public static long cap(ItemStack stack) {
        return stack.getItem() instanceof VoidStorageItem storage ? storage.cap() : 0L;
    }

    public static void set(ItemStack stack, long value) {
        CompoundTag tag = tag(stack);
        tag.putLong(KEY, Math.max(0L, value));
        setTag(stack, tag);
    }

    /** Adds up to capacity; returns the leftover that did not fit. */
    public static long add(ItemStack stack, long amount) {
        if (!(stack.getItem() instanceof VoidStorageItem storage) || amount <= 0) {
            return amount;
        }
        long current = get(stack);
        long cap = storage.cap();
        long room = cap == Long.MAX_VALUE ? Long.MAX_VALUE - current : cap - current;
        long accepted = Math.min(room, amount);
        if (accepted > 0) {
            set(stack, current + accepted);
        }
        return amount - accepted;
    }

    public static boolean isFull(ItemStack stack) {
        if (!(stack.getItem() instanceof VoidStorageItem storage)) {
            return false;
        }
        return storage.cap() != Long.MAX_VALUE && get(stack) >= storage.cap();
    }

    /** Fills storages in the player's inventory/armor/offhand; full ones become 充盈 variants. */
    public static long addToPlayer(Player player, long amount) {
        Inventory inventory = player.getInventory();
        long[] remaining = {amount};
        fillList(inventory.items, remaining);
        fillList(inventory.armor, remaining);
        fillList(inventory.offhand, remaining);
        return amount - remaining[0];
    }

    private static void fillList(NonNullList<ItemStack> stacks, long[] remaining) {
        for (int i = 0; i < stacks.size() && remaining[0] > 0; i++) {
            ItemStack stack = stacks.get(i);
            if (!(stack.getItem() instanceof VoidStorageItem storage) || isFull(stack)) {
                continue;
            }
            remaining[0] = add(stack, remaining[0]);
            if (isFull(stack)) {
                // keep the stack size: 4 full storages -> 4 filled storages
                stacks.set(i, new ItemStack(storage.filled(), stack.getCount()));
            }
        }
    }

    /** Drains storages in the player's inventory; returns the amount actually consumed. */
    public static long consumeFromPlayer(Player player, long amount) {
        Inventory inventory = player.getInventory();
        long[] consumed = {0L};
        drainList(inventory.items, amount, consumed);
        drainList(inventory.armor, amount, consumed);
        drainList(inventory.offhand, amount, consumed);
        return consumed[0];
    }

    private static void drainList(NonNullList<ItemStack> stacks, long amount, long[] consumed) {
        for (int i = 0; i < stacks.size() && consumed[0] < amount; i++) {
            ItemStack stack = stacks.get(i);
            if (!(stack.getItem() instanceof VoidStorageItem)) {
                continue;
            }
            long need = amount - consumed[0];
            long have = get(stack);
            long take = Math.min(have, need);
            if (take > 0) {
                set(stack, have - take);
                consumed[0] += take;
            }
        }
    }

    public static String format(long value) {
        return String.format("%,d", value);
    }

    public static String capText(ItemStack stack) {
        long cap = cap(stack);
        return cap == Long.MAX_VALUE ? "∞" : format(cap);
    }

    public static int mobCost(EntityType<?> type) {
        if (type == EntityType.WITHER || type == EntityType.ENDER_DRAGON || type == EntityType.WARDEN) {
            return 50_000;
        }
        if (type == EntityType.ELDER_GUARDIAN || type == EntityType.RAVAGER || type == EntityType.PIGLIN_BRUTE) {
            return 10_000;
        }
        MobCategory category = type.getCategory();
        return switch (category) {
            case MONSTER -> 2_000;
            case CREATURE, WATER_CREATURE -> 500;
            case AMBIENT, WATER_AMBIENT, AXOLOTLS -> 200;
            case MISC -> 1_000;
            default -> 1_000;
        };
    }

    public static EntityType<?> byId(String id) {
        ResourceLocation key = ResourceLocation.tryParse(id);
        if (key == null || !BuiltInRegistries.ENTITY_TYPE.containsKey(key)) {
            return null;
        }
        return BuiltInRegistries.ENTITY_TYPE.get(key);
    }

    public static String idOf(EntityType<?> type) {
        return BuiltInRegistries.ENTITY_TYPE.getKey(type).toString();
    }

    public static Item filledItem(int tier) {
        return switch (tier) {
            case 1 -> VoidGen.FILLED_VOID_STORAGE_IRON.get();
            case 2 -> VoidGen.FILLED_VOID_STORAGE_GOLD.get();
            case 3 -> VoidGen.FILLED_VOID_STORAGE_DIAMOND.get();
            case 4 -> VoidGen.FILLED_VOID_STORAGE_EMERALD.get();
            default -> VoidGen.VOID_STORAGE_NETHER.get();
        };
    }
}
