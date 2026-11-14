package com.voidgen.block;

import com.mojang.serialization.MapCodec;
import com.voidgen.VoidStats;
import com.voidgen.item.NestUpgradeItem;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Void Generator block. Interaction:
 * <ul>
 *     <li>shift + right click: open the internal GUI (AE2-style panel, 12 card slots)</li>
 *     <li>Nest Upgrade I-V: tier upgrade (must be sequential)</li>
 *     <li>any upgrade card (including AE2 acceleration/capacity cards): insert into the GUI</li>
 *     <li>empty hand: action-bar status readout</li>
 * </ul>
 * The Binding Card is a player accessory and is not inserted here: right-clicking other
 * machines with an empty hand while it is equipped binds them.
 */
public class VoidGeneratorBlock extends Block implements EntityBlock {
    public VoidGeneratorBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends Block> codec() {
        return CODEC;
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new VoidGeneratorBlockEntity(pos, state);
    }

    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        // v2.2.3: ticking is driven by ServerTickEvent.Post (VoidGeneratorBlockEntity.tickAll),
        // so force-loaded chunks keep working without entity ticks.
        return null;
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player, InteractionHand hand, BlockHitResult hitResult) {
        if (player.isShiftKeyDown()) {
            if (!level.isClientSide && level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity generator) {
                player.openMenu(generator);
            }
            return ItemInteractionResult.SUCCESS;
        }
        if (!(level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity generator)) {
            return super.useItemOn(stack, state, level, pos, player, hand, hitResult);
        }
        if (stack.getItem() instanceof NestUpgradeItem upgrade) {
            if (!level.isClientSide) {
                if (generator.tryUpgrade(upgrade.tier())) {
                    if (!player.getAbilities().instabuild) {
                        stack.shrink(1);
                    }
                    level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.BLOCKS, 1.0F, 1.0F);
                    player.displayClientMessage(Component.translatable("status.voidgen.upgraded", generator.tier()), true);
                } else {
                    player.displayClientMessage(Component.translatable("status.voidgen.upgrade_required", generator.tier() + 1), true);
                }
            }
            return ItemInteractionResult.SUCCESS;
        }
        if (VoidStats.isSlotCard(stack)) {
            if (!level.isClientSide) {
                if (generator.tryInsertCard(stack)) {
                    if (!player.getAbilities().instabuild) {
                        stack.shrink(1);
                    }
                    level.playSound(null, pos, SoundEvents.ITEM_PICKUP, SoundSource.BLOCKS, 0.7F, 1.4F);
                    player.displayClientMessage(Component.translatable("status.voidgen.card_inserted"), true);
                } else {
                    player.displayClientMessage(Component.translatable("status.voidgen.slots_full"), true);
                }
            }
            return ItemInteractionResult.SUCCESS;
        }
        if (stack.isEmpty() && !level.isClientSide) {
            player.displayClientMessage(Component.translatable("status.voidgen.void_generator",
                    generator.tier(),
                    VoidStats.fmtCompact(generator.rate()),
                    VoidStats.fmtCompact(generator.energy()),
                    VoidStats.fmtCompact(generator.capacity()),
                    rangeText(generator.range())), true);
            player.displayClientMessage(Component.translatable("status.voidgen.void_value_line",
                    VoidStats.fmtCompact(generator.voidAmount())), true);
        }
        return super.useItemOn(stack, state, level, pos, player, hand, hitResult);
    }

    @Override
    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
        if (!level.isClientSide() && level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity generator) {
            generator.dropContents(level);
        }
        return super.playerWillDestroy(level, pos, state, player);
    }

    private static Component rangeText(long range) {
        if (range == Long.MAX_VALUE) {
            return Component.translatable("gui.voidgen.infinite");
        }
        return Component.translatable("gui.voidgen.finite", VoidStats.fmtCompact(range));
    }
}
