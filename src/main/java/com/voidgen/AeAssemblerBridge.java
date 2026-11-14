package com.voidgen;

import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Reflection bridge for the AE2-dependent "void assembler" (pattern provider).
 * The block only exists when AE2 is installed; nothing here touches an AE2 type
 * at compile time.
 */
public final class AeAssemblerBridge {
    private AeAssemblerBridge() {
    }

    public static void install(DeferredRegister<Block> blocks,
                               DeferredRegister<Item> items,
                               DeferredRegister<BlockEntityType<?>> blockEntities) {
        if (!AeBridge.present()) {
            return;
        }
        try {
            Class<?> assembler = Class.forName("com.voidgen.ae.AeAssembler");
            assembler.getMethod("install", DeferredRegister.class, DeferredRegister.class, DeferredRegister.class)
                    .invoke(null, blocks, items, blockEntities);
        } catch (Throwable ignored) {
            // AE2 present but integration failed to load; keep the rest of the mod working.
        }
    }

    public static void registerGridCapability(RegisterCapabilitiesEvent event) {
        if (!AeBridge.present()) {
            return;
        }
        try {
            Class<?> assembler = Class.forName("com.voidgen.ae.AeAssembler");
            assembler.getMethod("registerGridCapability", RegisterCapabilitiesEvent.class).invoke(null, event);
        } catch (Throwable ignored) {
            // Optional integration.
        }
    }
}
