package com.voidgen.item;

import com.voidgen.VoidValue;
import com.voidgen.block.NothingnessDistributorBlock;
import com.voidgen.block.NothingnessDistributorBlockEntity;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;

/** 虚无生物生成器：选好生物后消耗虚无值生成；Shift+右键发散器绑定提取源。 */
public class MobSpawnerItem extends Item {
    public static final String MOB = "Mob";
    public static final String DIST = "Dist";

    public MobSpawnerItem(Properties properties) {
        super(properties);
    }

    public static String selectedId(ItemStack stack) {
        return VoidValue.tag(stack).getString(MOB);
    }

    public static void setSelectedId(ItemStack stack, String id) {
        var tag = VoidValue.tag(stack);
        tag.putString(MOB, id);
        VoidValue.setTag(stack, tag);
    }

    public static BlockPos boundPos(ItemStack stack) {
        var tag = VoidValue.tag(stack);
        return tag.contains(DIST) ? BlockPos.of(tag.getLong(DIST)) : null;
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        Player player = context.getPlayer();
        ItemStack stack = context.getItemInHand();
        BlockState state = level.getBlockState(context.getClickedPos());
        if (player == null) {
            return InteractionResult.PASS;
        }
        if (player.isShiftKeyDown()) {
            if (state.getBlock() instanceof NothingnessDistributorBlock
                    && level.getBlockEntity(context.getClickedPos()) instanceof NothingnessDistributorBlockEntity) {
                if (!level.isClientSide()) {
                    var tag = VoidValue.tag(stack);
                    tag.putLong(DIST, context.getClickedPos().asLong());
                    VoidValue.setTag(stack, tag);
                    player.displayClientMessage(Component.translatable("status.voidgen.spawner_bound",
                            context.getClickedPos().toShortString()), true);
                }
                return InteractionResult.sidedSuccess(level.isClientSide());
            }
            if (level.isClientSide()) {
                openScreen(stack);
            }
            return InteractionResult.sidedSuccess(level.isClientSide());
        }
        if (!level.isClientSide()) {
            BlockPos spawnPos = context.getClickedPos().relative(context.getClickedFace());
            return trySpawn(level, player, stack, spawnPos, context.getClickedFace());
        }
        return InteractionResult.SUCCESS;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.isShiftKeyDown()) {
            if (level.isClientSide()) {
                openScreen(stack);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }
        return InteractionResultHolder.pass(stack);
    }

    private InteractionResult trySpawn(Level level, Player player, ItemStack stack, BlockPos pos, Direction face) {
        String id = selectedId(stack);
        EntityType<?> type = id.isEmpty() ? null : VoidValue.byId(id);
        if (type == null) {
            player.displayClientMessage(Component.translatable("status.voidgen.spawner_no_mob"), true);
            return InteractionResult.FAIL;
        }
        if (!level.isEmptyBlock(pos) && level.getBlockState(pos).isSolidRender(level, pos)) {
            player.displayClientMessage(Component.translatable("status.voidgen.spawner_blocked"), true);
            return InteractionResult.FAIL;
        }
        long cost = VoidValue.mobCost(type);
        long paid = 0L;
        BlockPos bound = boundPos(stack);
        if (bound != null && level.getBlockEntity(bound) instanceof NothingnessDistributorBlockEntity distributor) {
            paid = distributor.drain(cost);
        }
        if (paid < cost) {
            long rest = cost - paid;
            long fromPlayer = VoidValue.consumeFromPlayer(player, rest);
            if (fromPlayer < rest) {
                // refund whatever was already taken from the distributor
                if (paid > 0 && bound != null && level.getBlockEntity(bound) instanceof NothingnessDistributorBlockEntity distributor) {
                    distributor.accept(paid);
                }
                player.displayClientMessage(Component.translatable("status.voidgen.spawner_no_value",
                        VoidValue.format(cost)), true);
                return InteractionResult.FAIL;
            }
            paid = cost;
        }
        Entity entity = type.create(level);
        if (entity == null) {
            player.displayClientMessage(Component.translatable("status.voidgen.spawner_failed"), true);
            return InteractionResult.FAIL;
        }
        entity.moveTo(pos.getX() + 0.5D, pos.getY(), pos.getZ() + 0.5D, player.getYRot(), 0.0F);
        if (entity instanceof Mob mob) {
            mob.setPersistenceRequired();
        }
        level.addFreshEntity(entity);
        player.displayClientMessage(Component.translatable("status.voidgen.spawner_spawned",
                Component.translatable(type.getDescriptionId()), VoidValue.format(cost)), true);
        return InteractionResult.SUCCESS;
    }

    private static void openScreen(ItemStack stack) {
        com.voidgen.client.MobSpawnerClient.open();
    }
}
