package com.voidgen;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.event.tick.EntityTickEvent;

/** 圆石掉进虚空：按 1 圆石 = 1 虚无值 充入投掷者背包里的虚无存储器。 */
public final class VoidDropHandler {
    private VoidDropHandler() {
    }

    public static void onEntityTick(EntityTickEvent.Post event) {
        if (!(event.getEntity() instanceof ItemEntity item)) {
            return;
        }
        if (item.level().isClientSide() || item.getItem().getItem() != Items.COBBLESTONE) {
            return;
        }
        if (item.getY() >= item.level().getMinBuildHeight() - 4) {
            return;
        }
        int count = item.getItem().getCount();
        if (item.getOwner() instanceof ServerPlayer player) {
            long accepted = VoidValue.addToPlayer(player, count);
            if (accepted > 0) {
                player.displayClientMessage(Component.translatable("status.voidgen.void_drop",
                        VoidValue.format(accepted)).withStyle(ChatFormatting.AQUA), true);
            } else {
                player.displayClientMessage(Component.translatable("status.voidgen.void_drop_full"), true);
            }
        }
        item.discard();
    }
}
