package com.voidgen.ae;

import com.voidgen.block.VoidFurnaceBlockEntity;

import appeng.api.AECapabilities;
import appeng.api.networking.IInWorldGridNodeHost;

import net.minecraft.world.level.block.entity.BlockEntityType;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;

/**
 * AE2-dependent glue: registers the furnace as an in-world grid node host so
 * AE2 cables connect to it, and creates the node holder on demand.
 */
public final class FurnaceAeSupport {
    private FurnaceAeSupport() {
    }

    @SuppressWarnings("unchecked")
    public static void registerGridCapability(RegisterCapabilitiesEvent event, BlockEntityType<?> type) {
        event.registerBlockEntity(AECapabilities.IN_WORLD_GRID_NODE_HOST,
                (BlockEntityType<VoidFurnaceBlockEntity>) type,
                (furnace, side) -> {
                    Object host = furnace.gridHost();
                    return host instanceof IInWorldGridNodeHost nodeHost ? nodeHost : null;
                });
    }

    public static Object createHost(VoidFurnaceBlockEntity furnace) {
        return new FurnaceGridNode(furnace);
    }
}
