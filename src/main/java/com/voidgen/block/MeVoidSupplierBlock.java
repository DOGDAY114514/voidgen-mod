package com.voidgen.block;

import com.mojang.serialization.MapCodec;
import com.voidgen.VoidStats;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;

/** ME 虚无供应器：AE 与本模组虚无值之间的桥。 */
public class MeVoidSupplierBlock extends Block implements EntityBlock {
    public static final MapCodec<MeVoidSupplierBlock> CODEC = simpleCodec(MeVoidSupplierBlock::new);

    public MeVoidSupplierBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends Block> codec() {
        return CODEC;
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new MeVoidSupplierBlockEntity(pos, state);
    }

    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide()) {
            return null;
        }
        return (lvl, pos, st, be) -> {
            if (be instanceof MeVoidSupplierBlockEntity supplier) {
                supplier.tick(lvl);
            }
        };
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide && level.getBlockEntity(pos) instanceof MeVoidSupplierBlockEntity supplier) {
            supplier.toggleMode();
            player.displayClientMessage(Component.translatable("status.voidgen.supplier_mode",
                    Component.translatable(supplier.mode() == 0 ? "status.voidgen.supplier_supply" : "status.voidgen.supplier_import")), true);
            player.displayClientMessage(Component.translatable("status.voidgen.supplier_status",
                    VoidStats.fmtCompact(supplier.buffer()), supplier.slotCount()), false);
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
        if (!level.isClientSide && level.getBlockEntity(pos) instanceof MeVoidSupplierBlockEntity supplier) {
            supplier.dropContents(level);
        }
        return super.playerWillDestroy(level, pos, state, player);
    }
}
