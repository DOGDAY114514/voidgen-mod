package com.voidgen.block;

import com.mojang.serialization.MapCodec;
import com.voidgen.VoidGen;
import com.voidgen.VoidStats;
import com.voidgen.item.NestUpgradeItem;
import com.voidgen.item.VoidConfiguratorItem;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.util.Mth;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.EntityBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

public class VoidFurnaceBlock extends Block implements EntityBlock {
    public static final IntegerProperty TIER = IntegerProperty.create("tier", 0, 5);

    public VoidFurnaceBlock(Properties properties) {
        super(properties);
        registerDefaultState(this.stateDefinition.any().setValue(TIER, 0));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(TIER);
    }

    public static int tierOf(BlockState state) {
        return state.hasProperty(TIER) ? state.getValue(TIER) : 0;
    }

    public static BlockState withTier(BlockState state, int tier) {
        return state.hasProperty(TIER) ? state.setValue(TIER, Mth.clamp(tier, 0, 5)) : state;
    }

    @Override
    protected MapCodec<? extends Block> codec() {
        return CODEC;
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
        return new VoidFurnaceBlockEntity(pos, state);
    }

    @Override
    protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean movedByPiston) {
        super.onPlace(state, level, pos, oldState, movedByPiston);
        // Create the optional AE2 grid node before neighbour block updates reach the cables,
        // so the first connection check already sees a live node host.
        if (!level.isClientSide() && level.getBlockEntity(pos) instanceof VoidFurnaceBlockEntity furnace) {
            furnace.gridHost();
        }
    }

    @Override
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(Level level, BlockState state, BlockEntityType<T> type) {
        if (level.isClientSide()) {
            return null;
        }
        return (lvl, pos, st, be) -> {
            if (be instanceof VoidFurnaceBlockEntity furnace) {
                furnace.tick(lvl);
            }
        };
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level,
                                              BlockPos pos, Player player, InteractionHand hand, BlockHitResult hit) {
        if (!(level.getBlockEntity(pos) instanceof VoidFurnaceBlockEntity furnace)) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        // The configurator has its own useOn (face cycling / shift toggles wireless output).
        if (stack.getItem() instanceof VoidConfiguratorItem) {
            return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
        }
        // Shift + right-click installs nest upgrades / cards directly from the outside.
        if (player.isShiftKeyDown()) {
            if (stack.getItem() instanceof NestUpgradeItem nest) {
                if (!level.isClientSide()) {
                    if (furnace.tryUpgrade(nest.tier())) {
                        if (!player.getAbilities().instabuild) {
                            stack.shrink(1);
                        }
                        level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.BLOCKS, 0.8F, 1.1F);
                        player.displayClientMessage(Component.translatable("status.voidgen.furnace_upgraded", nest.tier()), true);
                    } else {
                        player.displayClientMessage(Component.translatable("status.voidgen.furnace_upgrade_required", furnace.tier() + 1), true);
                    }
                }
                return ItemInteractionResult.SUCCESS;
            }
            if (VoidStats.isFurnaceCard(stack)) {
                if (!level.isClientSide()) {
                    if (furnace.tryInsertCard(stack)) {
                        if (!player.getAbilities().instabuild) {
                            stack.shrink(1);
                        }
                        level.playSound(null, pos, SoundEvents.ITEM_PICKUP, SoundSource.BLOCKS, 0.8F, 1.2F);
                    } else {
                        player.displayClientMessage(Component.translatable("status.voidgen.furnace_cards_full"), true);
                    }
                }
                return ItemInteractionResult.SUCCESS;
            }
        }
        // Plain right-click opens the internal panel.
        if (!level.isClientSide()) {
            player.openMenu(furnace);
        }
        return ItemInteractionResult.SUCCESS;
    }

    @Override
    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
        if (!level.isClientSide() && level.getBlockEntity(pos) instanceof VoidFurnaceBlockEntity furnace) {
            furnace.dropContents(level);
        }
        return super.playerWillDestroy(level, pos, state, player);
    }

    @Override
    public void playerDestroy(Level level, Player player, BlockPos pos, BlockState state, BlockEntity blockEntity, ItemStack tool) {
        if (player.getAbilities().instabuild) {
            return;
        }
        ItemStack drop = new ItemStack(VoidGen.VOID_FURNACE_ITEM.get());
        CompoundTag tag = new CompoundTag();
        tag.putInt("Tier", tierOf(state));
        drop.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
        Block.popResource(level, pos, drop);
    }

    @Override
    public void setPlacedBy(Level level, BlockPos pos, BlockState state, LivingEntity placer, ItemStack stack) {
        if (level.isClientSide) {
            return;
        }
        CustomData data = stack.get(DataComponents.CUSTOM_DATA);
        int tier = data == null ? 0 : data.copyTag().getInt("Tier");
        tier = Mth.clamp(tier, 0, 5);
        if (tier > 0) {
            level.setBlock(pos, withTier(state, tier), 3);
            if (level.getBlockEntity(pos) instanceof VoidFurnaceBlockEntity be) {
                be.setTier(tier);
            }
        }
    }
}
