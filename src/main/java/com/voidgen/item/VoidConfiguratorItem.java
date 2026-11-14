package com.voidgen.item;

import com.voidgen.block.VoidFurnaceBlockEntity;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;

import java.util.List;

/**
 * Void Configurator: right-click a furnace face to cycle INPUT / OUTPUT / DISABLED,
 * shift-right-click to toggle wireless auto-output.
 */
public class VoidConfiguratorItem extends Item {
    public VoidConfiguratorItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        BlockEntity be = level.getBlockEntity(pos);
        if (!(be instanceof VoidFurnaceBlockEntity furnace) || context.getPlayer() == null) {
            return InteractionResult.PASS;
        }
        if (!level.isClientSide()) {
            if (context.getPlayer().isShiftKeyDown()) {
                furnace.toggleWireless();
                context.getPlayer().displayClientMessage(Component.translatable(
                        furnace.wirelessEnabled()
                                ? "status.voidgen.furnace_wireless_on"
                                : "status.voidgen.furnace_wireless_off"), true);
            } else {
                Direction face = context.getClickedFace();
                VoidFurnaceBlockEntity.FaceMode mode = furnace.cycleFace(face);
                context.getPlayer().displayClientMessage(Component.translatable("status.voidgen.furnace_face",
                        Component.translatable("gui.voidgen.face." + face.getSerializedName()),
                        Component.translatable("gui.voidgen.face_mode." + mode.name().toLowerCase())), true);
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidgen.void_configurator").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable("tooltip.voidgen.void_configurator.shift").withStyle(ChatFormatting.DARK_GRAY));
    }
}
