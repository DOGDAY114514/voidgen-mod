package com.voidgen;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.capabilities.BlockCapability;
import net.neoforged.neoforge.items.IItemHandler;

import java.lang.reflect.Method;

/**
 * Optional AE2 bridge: pushes items into AE2's {@code GENERIC_INTERNAL_INV} capability.
 *
 * <p>For AE2's ME Interface that capability wraps the interface storage; AE2 itself flushes
 * stored-but-unrequested stacks into the ME network on its next tick, so this is enough to
 * "return" furnace output to AE. Everything is reflective: the mod compiles without AE2 and
 * degrades to a no-op when AE2 (or a compatible API) is missing.</p>
 */
public final class AeReturn {
    private static boolean tried;
    private static boolean ready;

    private static BlockCapability<?, ?> capability;
    private static Method insertMethod;
    private static Method sizeMethod;
    private static Method itemKeyOf;
    private static Object actionableModulate;

    private AeReturn() {
    }

    public static boolean available() {
        init();
        return ready;
    }

    private static synchronized void init() {
        if (tried) {
            return;
        }
        tried = true;
        try {
            // AE2 19.x (MC 1.21.1) keeps the cap in appeng.api.AECapabilities;
            // older builds used appeng.capabilities.Capabilities.
            for (String holder : new String[]{"appeng.api.AECapabilities", "appeng.capabilities.Capabilities"}) {
                try {
                    Class<?> caps = Class.forName(holder);
                    for (var field : caps.getFields()) {
                        if (!"GENERIC_INTERNAL_INV".equals(field.getName())) {
                            continue;
                        }
                        Object value = field.get(null);
                        if (value instanceof BlockCapability<?, ?> blockCapability) {
                            capability = blockCapability;
                        }
                    }
                } catch (ClassNotFoundException ignored) {
                    // try next holder
                }
                if (capability != null) {
                    break;
                }
            }

            Class<?> inventory = Class.forName("appeng.api.behaviors.GenericInternalInventory");
            sizeMethod = inventory.getMethod("size");

            Class<?> keyClass = Class.forName("appeng.api.stacks.AEKey");
            Class<?> actionable = Class.forName("appeng.api.config.Actionable");
            insertMethod = inventory.getMethod("insert", int.class, keyClass, long.class, actionable);

            for (Object constant : actionable.getEnumConstants()) {
                if ("MODULATE".equals(String.valueOf(constant))) {
                    actionableModulate = constant;
                }
            }

            itemKeyOf = Class.forName("appeng.api.stacks.AEItemKey").getMethod("of", ItemStack.class);
            ready = capability != null
                    && insertMethod != null
                    && sizeMethod != null
                    && itemKeyOf != null
                    && actionableModulate != null;
        } catch (Throwable ignored) {
            ready = false;
        }
    }

    /**
     * Push up to {@code max} items from {@code handler} into the AE2 generic inventory at {@code pos}.
     *
     * @return number of items actually moved
     */
    @SuppressWarnings("unchecked")
    public static int push(Level level, BlockPos pos, Direction side, IItemHandler handler, int max) {
        if (max <= 0 || !available()) {
            return 0;
        }
        try {
            BlockCapability<Object, Direction> cap =
                    (BlockCapability<Object, Direction>) (BlockCapability<?, ?>) capability;
            Object inventory = level.getCapability(cap, pos, side);
            if (inventory == null) {
                return 0;
            }
            int moved = 0;
            for (int slot = 0; slot < handler.getSlots() && moved < max; slot++) {
                ItemStack stack = handler.getStackInSlot(slot);
                if (stack.isEmpty()) {
                    continue;
                }
                int amount = Math.min(stack.getCount(), max - moved);
                int inserted = insertInto(inventory, stack, amount);
                if (inserted > 0) {
                    handler.extractItem(slot, inserted, false);
                    moved += inserted;
                }
            }
            return moved;
        } catch (Throwable ignored) {
            return 0;
        }
    }

    private static int insertInto(Object inventory, ItemStack stack, int amount) {
        try {
            int size = (int) sizeMethod.invoke(inventory);
            Object key = itemKeyOf.invoke(null, stack.copyWithCount(Math.min(amount, stack.getCount())));
            int inserted = 0;
            for (int slot = 0; slot < size && inserted < amount; slot++) {
                long moved = (long) insertMethod.invoke(inventory, slot, key, (long) (amount - inserted), actionableModulate);
                if (moved > 0) {
                    inserted += (int) Math.min(Integer.MAX_VALUE, moved);
                }
            }
            return inserted;
        } catch (Throwable ignored) {
            return 0;
        }
    }
}
