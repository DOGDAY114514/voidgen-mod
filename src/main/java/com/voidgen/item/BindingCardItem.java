package com.voidgen.item;

import java.util.List;

import com.voidgen.block.VoidGeneratorBlockEntity;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

/**
 * Binding Card: binds to one Void Generator and lets the player fine-tune that
 * generator's wireless supply.
 *
 * <p>Right-click a Void Generator to bind (or unbind) the card. Right-click
 * another block to toggle it: blocks that would normally receive power get
 * excluded, blocks outside the generator's range get force-linked. The
 * generator's own area broadcast is unchanged.</p>
 *
 * <p>Right-clicks on machines are intercepted in {@link #onRightClickBlock}
 * before their GUI opens, so the card always gets to act first.</p>
 */
public class BindingCardItem extends Item {
    private static final String TAG_POS = "GenPos";
    private static final String TAG_DIM = "GenDim";

    public BindingCardItem(Properties properties) {
        super(properties);
    }

    private static CompoundTag tag(ItemStack stack) {
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
    }

    private static void write(ItemStack stack, CompoundTag tag) {
        stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
    }

    public static BlockPos boundPos(ItemStack stack) {
        CompoundTag tag = tag(stack);
        return tag.contains(TAG_POS) ? BlockPos.of(tag.getLong(TAG_POS)) : null;
    }

    public static String boundDim(ItemStack stack) {
        return tag(stack).getString(TAG_DIM);
    }

    private static void clear(ItemStack stack) {
        CompoundTag tag = tag(stack);
        tag.remove(TAG_POS);
        tag.remove(TAG_DIM);
        write(stack, tag);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        BlockPos bound = boundPos(stack);
        if (bound == null) {
            tooltip.add(Component.translatable("tooltip.voidgen.binding_card.unbound").withStyle(ChatFormatting.GRAY));
        } else {
            tooltip.add(Component.translatable("tooltip.voidgen.binding_card.bound",
                    bound.getX() + ", " + bound.getY() + ", " + bound.getZ()).withStyle(ChatFormatting.AQUA));
        }
        tooltip.add(Component.translatable("tooltip.voidgen.binding_card.usage").withStyle(ChatFormatting.DARK_GRAY));
    }

    /**
     * Runs before the clicked block gets to open its own GUI/use its own logic.
     * Without this, machines such as the void furnace would swallow the right-click
     * by opening their menu and the card would never toggle anything.
     */
    public static void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        if (event.getHand() != InteractionHand.MAIN_HAND) {
            return;
        }
        Level level = event.getLevel();
        if (level.isClientSide()) {
            return;
        }
        Player player = event.getEntity();
        ItemStack stack = event.getItemStack();
        if (!(stack.getItem() instanceof BindingCardItem)) {
            return;
        }
        BlockPos pos = event.getPos();
        // The generator itself is handled by Item#useOn (bind / unbind).
        if (level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity) {
            return;
        }
        toggleTarget(level, player, stack, pos);
        // Consume the click so no block GUI opens.
        event.setCanceled(true);
        event.setCancellationResult(InteractionResult.SUCCESS);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        Player player = context.getPlayer();
        if (player == null) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide()) {
            return InteractionResult.SUCCESS;
        }

        ItemStack stack = context.getItemInHand();
        BlockPos pos = context.getClickedPos();
        BlockEntity blockEntity = level.getBlockEntity(pos);

        // Binding happens on the generator itself.
        if (blockEntity instanceof VoidGeneratorBlockEntity generator) {
            String dim = level.dimension().location().toString();
            if (pos.equals(boundPos(stack)) && dim.equals(boundDim(stack))) {
                clear(stack);
                player.displayClientMessage(Component.translatable("status.voidgen.card_unbound"), true);
            } else {
                CompoundTag tag = tag(stack);
                tag.putLong(TAG_POS, pos.asLong());
                tag.putString(TAG_DIM, dim);
                write(stack, tag);
                player.displayClientMessage(Component.translatable("status.voidgen.card_bound",
                        pos.getX() + ", " + pos.getY() + ", " + pos.getZ()), true);
            }
            level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 0.5F, 1.6F);
            return InteractionResult.SUCCESS;
        }

        toggleTarget(level, player, stack, pos);
        return InteractionResult.SUCCESS;
    }

    /** Shared toggle logic used by both the item callback and the pre-GUI event. */
    private static void toggleTarget(Level level, Player player, ItemStack stack, BlockPos pos) {
        BlockPos genPos = boundPos(stack);
        if (genPos == null) {
            player.displayClientMessage(Component.translatable("status.voidgen.card_not_bound"), true);
            return;
        }
        if (!level.dimension().location().toString().equals(boundDim(stack))) {
            player.displayClientMessage(Component.translatable("status.voidgen.card_dim"), true);
            return;
        }
        BlockEntity genEntity = level.getBlockEntity(genPos);
        if (!(genEntity instanceof VoidGeneratorBlockEntity generator)) {
            clear(stack);
            player.displayClientMessage(Component.translatable("status.voidgen.card_lost"), true);
            return;
        }

        boolean hasEnergy = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null) != null;
        if (!hasEnergy && !generator.hasOverride(pos)) {
            player.displayClientMessage(Component.translatable("status.voidgen.card_no_energy"), true);
            return;
        }

        int result = generator.toggleSupply(pos);
        Component message = switch (result) {
            case 0 -> Component.translatable("status.voidgen.card_forced");
            case 1 -> Component.translatable("status.voidgen.card_excluded");
            case 2 -> Component.translatable("status.voidgen.card_restored");
            default -> Component.translatable("status.voidgen.card_force_removed");
        };
        player.displayClientMessage(message, true);
        level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 0.5F, 1.2F);
    }
}
