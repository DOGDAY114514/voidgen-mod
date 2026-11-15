package com.voidgen;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.event.tick.EntityTickEvent;

/**
 * World interaction for the floating crystal family: an {@code ae2:certus_quartz_crystal}
 * item dropped in water together with floating crystal dust slowly turns into a
 * floating crystal (one dust consumed per crystal).
 */
public final class WaterCrystalHandler {
    private static final String TICKS_TAG = "VoidgenWaterTicks";
    private static final int NEEDED_TICKS = 100;
    private static final double DUST_RADIUS = 3.0;

    private WaterCrystalHandler() {
    }

    public static void onEntityTick(EntityTickEvent.Post event) {
        if (!(event.getEntity() instanceof ItemEntity crystal)) {
            return;
        }
        if (!(crystal.level() instanceof ServerLevel level)) {
            return;
        }
        var tag = crystal.getPersistentData();
        ItemStack stack = crystal.getItem();
        if (!isCertus(stack)) {
            if (tag.contains(TICKS_TAG)) {
                tag.remove(TICKS_TAG);
            }
            return;
        }
        if (!crystal.isInWater()) {
            tag.remove(TICKS_TAG);
            return;
        }
        int ticks = tag.getInt(TICKS_TAG) + 1;
        if (ticks < NEEDED_TICKS) {
            tag.putInt(TICKS_TAG, ticks);
            return;
        }
        for (ItemEntity dust : level.getEntitiesOfClass(ItemEntity.class, crystal.getBoundingBox().inflate(DUST_RADIUS))) {
            if (dust == crystal || !dust.isInWater()) {
                continue;
            }
            if (dust.getItem().getItem() != VoidGen.FLOATING_CRYSTAL_DUST.get()) {
                continue;
            }
            tag.putInt(TICKS_TAG, 0);
            dust.getItem().shrink(1);
            if (dust.getItem().isEmpty()) {
                dust.discard();
            }
            ItemStack out = new ItemStack(VoidGen.FLOATING_CRYSTAL.get());
            if (stack.getCount() > 1) {
                stack.shrink(1);
                level.addFreshEntity(new ItemEntity(level, crystal.getX(), crystal.getY(), crystal.getZ(), out));
            } else {
                crystal.setItem(out);
            }
            return;
        }
        tag.putInt(TICKS_TAG, NEEDED_TICKS - 1);
    }

    private static boolean isCertus(ItemStack stack) {
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return id != null && "ae2".equals(id.getNamespace()) && "certus_quartz_crystal".equals(id.getPath());
    }
}
