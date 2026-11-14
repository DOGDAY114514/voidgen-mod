package com.voidgen;

import com.voidgen.block.VoidFurnaceBlockEntity;

import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;

/**
 * Reflection bridge to the AE2-dependent classes. Nothing here touches an AE2
 * type at compile time, so the mod keeps loading when AE2 is not installed.
 */
public final class AeBridge {
    private static Boolean present;

    private AeBridge() {
    }

    public static boolean present() {
        if (present == null) {
            try {
                // initialize=false: do not run AE2's static setup during capability registration.
                Class.forName("appeng.api.AECapabilities", false, AeBridge.class.getClassLoader());
                present = Boolean.TRUE;
            } catch (Throwable ignored) {
                present = Boolean.FALSE;
            }
        }
        return present.booleanValue();
    }

    public static void registerGridCapability(RegisterCapabilitiesEvent event, BlockEntityType<?> type) {
        if (!present()) {
            return;
        }
        try {
            Class<?> support = Class.forName("com.voidgen.ae.FurnaceAeSupport");
            support.getMethod("registerGridCapability", RegisterCapabilitiesEvent.class, BlockEntityType.class)
                    .invoke(null, event, type);
        } catch (Throwable ignored) {
            // AE2 present but integration class failed to load; stay optional.
        }
    }

    public static Object createHost(VoidFurnaceBlockEntity furnace) {
        if (!present()) {
            return null;
        }
        try {
            Class<?> support = Class.forName("com.voidgen.ae.FurnaceAeSupport");
            return support.getMethod("createHost", VoidFurnaceBlockEntity.class).invoke(null, furnace);
        } catch (Throwable ignored) {
            return null;
        }
    }
}
