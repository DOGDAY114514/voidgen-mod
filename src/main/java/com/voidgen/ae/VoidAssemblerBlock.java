package com.voidgen.ae;

import com.mojang.serialization.MapCodec;

import appeng.helpers.patternprovider.PatternProviderLogicHost;
import appeng.menu.locator.MenuLocators;

import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** AE2-styled pattern provider that performs instant void crafting for AE2 processors. */
public class VoidAssemblerBlock extends Block implements EntityBlock {
    public VoidAssemblerBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends Block> codec() {
        return simpleCodec(VoidAssemblerBlock::new);
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new VoidAssemblerBlockEntity(pos, state);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide) {
            if (level.getBlockEntity(pos) instanceof PatternProviderLogicHost host) {
                host.openMenu(player, MenuLocators.forBlockEntity(host.getBlockEntity()));
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
}
