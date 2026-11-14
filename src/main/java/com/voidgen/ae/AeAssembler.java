package com.voidgen.ae;

import com.voidgen.VoidGen;

import appeng.api.AECapabilities;

import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Registers the AE2-dependent void assembler when AE2 is present. The block is a
 * pattern provider whose instant "void crafting" only produces AE2 processors.
 */
public final class AeAssembler {
    private AeAssembler() {
    }

    public static DeferredHolder<BlockEntityType<?>, BlockEntityType<VoidAssemblerBlockEntity>> BE;

    public static void install(DeferredRegister<Block> blocks,
                               DeferredRegister<Item> items,
                               DeferredRegister<BlockEntityType<?>> blockEntities) {
        DeferredHolder<Block, VoidAssemblerBlock> block = blocks.register("void_assembler",
                () -> new VoidAssemblerBlock(BlockBehaviour.Properties.of()
                        .mapColor(MapColor.COLOR_PURPLE)
                        .strength(4.0F, 5.0F)
                        .requiresCorrectToolForDrops()
                        .sound(SoundType.METAL)));
        DeferredHolder<Item, BlockItem> item = items.register("void_assembler",
                () -> new BlockItem(block.get(), new Item.Properties()));
        BE = blockEntities.register("void_assembler",
                () -> BlockEntityType.Builder.<VoidAssemblerBlockEntity>of(
                        (pos, state) -> new VoidAssemblerBlockEntity(pos, state), block.get()).build(null));
        VoidGen.VOID_ASSEMBLER_BLOCK = block;
        VoidGen.VOID_ASSEMBLER_ITEM = item;
        VoidGen.VOID_ASSEMBLER_BE = BE;
    }

    public static void registerGridCapability(RegisterCapabilitiesEvent event) {
        if (BE == null) {
            return;
        }
        event.registerBlockEntity(AECapabilities.IN_WORLD_GRID_NODE_HOST, BE.get(), (be, side) -> be);
    }
}
