package com.voidgen;

import net.minecraft.nbt.CompoundTag;
import net.neoforged.neoforge.items.IItemHandler;

/**
 * Common side of the optional AE2 integration. Implemented by the AE2-dependent
 * grid-node holder (com.voidgen.ae.FurnaceGridNode) and never referenced directly
 * from classes that must load without AE2 installed.
 */
public interface GridHost {
    boolean isOnline();

    /** Pushes up to {@code budget} output items into the connected ME network. */
    long pushItems(IItemHandler outputs, int budget);

    void save(CompoundTag tag);

    void load(CompoundTag tag);

    void destroy();
}
