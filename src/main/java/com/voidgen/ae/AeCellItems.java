package com.voidgen.ae;

import appeng.api.stacks.AEKeyType;
import appeng.items.storage.BasicStorageCell;
import com.voidgen.VoidCellItems;

import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * AE2-backed registration of the void storage disks. Only loaded when AE2 is present
 * (reachable via VoidCellItems' reflection call), so the base mod never hard-links AE2.
 * The disks are ordinary AE2 IBasicCellItem cells; AE2's BasicCellHandler manages their
 * content in the ME network automatically.
 */
public final class AeCellItems {
    private AeCellItems() {
    }

    public static void install(DeferredRegister<Item> items) {
        for (int tier = 0; tier < VoidCellItems.TIERS.length; tier++) {
            final int index = tier;
            VoidCellItems.CELLS.add(items.register("void_cell_" + VoidCellItems.TIERS[tier],
                    () -> createCell(index)));
        }
    }

    private static Item createCell(int index) {
        try {
            return new BasicStorageCell(
                    new Item.Properties().stacksTo(1),
                    0.5 + 0.5 * index,
                    (int) Math.min(Integer.MAX_VALUE, VoidCellItems.BYTES[index]),
                    8,
                    63,
                    AEKeyType.items());
        } catch (Throwable t) {
            // Should never happen with AE2 present, but keep the registry alive if a
            // future AE2 changes its validation rules.
            return new Item(new Item.Properties().stacksTo(1));
        }
    }
}
