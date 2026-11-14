package com.voidgen;

import java.util.ArrayList;
import java.util.List;

import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * The void storage disks. With AE2 installed these are real AE2 storage cells
 * (BasicStorageCell); without AE2 they degrade to inert items so ids/recipes stay valid.
 */
public final class VoidCellItems {
    public static final String[] TIERS = {"1k", "4k", "16k", "64k", "256k", "1m", "4m", "16m", "64m", "256m"};
    public static final long[] BYTES = {
            1_024L, 4_096L, 16_384L, 65_536L, 262_144L,
            1_048_576L, 4_194_304L, 16_777_216L, 67_108_864L, 268_435_456L
    };
    public static final List<DeferredHolder<Item, ? extends Item>> CELLS = new ArrayList<>();

    private VoidCellItems() {
    }

    public static void install(DeferredRegister<Item> items) {
        if (AeBridge.present()) {
            try {
                Class.forName("com.voidgen.ae.AeCellItems")
                        .getMethod("install", DeferredRegister.class)
                        .invoke(null, items);
                return;
            } catch (ReflectiveOperationException | LinkageError ignored) {
                // fall through to inert items
            }
        }
        for (String tier : TIERS) {
            CELLS.add(items.register("void_cell_" + tier,
                    () -> new Item(new Item.Properties().stacksTo(1))));
        }
    }

    public static String modelName(int index) {
        return "void_cell_" + TIERS[index];
    }
}
