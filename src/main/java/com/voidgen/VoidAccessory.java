package com.voidgen;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import com.voidgen.item.BindingCardItem;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/**
 * Server-side owner of the Binding Card accessory.
 *
 * <p>Vanilla has no accessory slot without mixins or Curios, so the equipped card lives in
 * the player's persistent data (key {@code voidgen}) and an overlay slot in the inventory
 * screen edits it through small custom payloads. While equipped the player can bind machines
 * by right-clicking them with an empty hand; Void Generators in the same dimension feed the
 * union of the bound sets of all equipped players. Auto-connect slowly binds player-placed
 * machines that need power within {@link #BIND_RADIUS} blocks.</p>
 */
public final class VoidAccessory {
    private static final String ROOT = "voidgen";
    private static final int BIND_RADIUS = 48;
    private static final int CHECK_COUNT = 32;

    private VoidAccessory() {
    }

    // ------------------------------------------------------------------ state

    private static CompoundTag data(Player player) {
        CompoundTag root = player.getPersistentData();
        if (root.contains(ROOT, Tag.TAG_COMPOUND)) {
            return root.getCompound(ROOT);
        }
        return new CompoundTag();
    }

    private static void store(Player player, CompoundTag data) {
        player.getPersistentData().put(ROOT, data);
    }

    public static boolean hasCard(Player player) {
        return data(player).getBoolean("Equipped");
    }

    private static List<BlockPos> boundsOf(Player player) {
        long[] raw = data(player).getLongArray("Bound");
        List<BlockPos> bounds = new ArrayList<>(raw.length);
        for (long packed : raw) {
            bounds.add(BlockPos.of(packed));
        }
        return bounds;
    }

    private static void setBounds(Player player, List<BlockPos> bounds) {
        CompoundTag data = data(player);
        data.putLongArray("Bound", bounds.stream().mapToLong(BlockPos::asLong).toArray());
        store(player, data);
    }

    // ------------------------------------------------------------------ equip / unequip

    public static boolean equip(ServerPlayer player) {
        if (hasCard(player)) {
            player.displayClientMessage(Component.translatable("status.voidgen.already_equipped"), true);
            return false;
        }
        Inventory inventory = player.getInventory();
        for (int slot = 0; slot < inventory.items.size(); slot++) {
            ItemStack stack = inventory.items.get(slot);
            if (stack.getItem() instanceof BindingCardItem) {
                stack.shrink(1);
                inventory.setChanged();
                player.containerMenu.broadcastChanges();
                CompoundTag data = data(player);
                data.putBoolean("Equipped", true);
                data.putBoolean("Auto", false);
                data.putLongArray("Bound", new long[0]);
                data.putLong("LastScan", 0L);
                data.putInt("ScanCursor", 0);
                store(player, data);
                player.displayClientMessage(Component.translatable("status.voidgen.equipped"), true);
                sendSync(player);
                return true;
            }
        }
        player.displayClientMessage(Component.translatable("status.voidgen.no_card"), true);
        return false;
    }

    public static boolean unequip(ServerPlayer player) {
        if (!hasCard(player)) {
            return false;
        }
        CompoundTag data = data(player);
        data.putBoolean("Equipped", false);
        data.putBoolean("Auto", false);
        data.putLongArray("Bound", new long[0]);
        store(player, data);
        ItemStack card = new ItemStack(VoidGen.BINDING_CARD.get());
        if (!player.getInventory().add(card)) {
            player.drop(card, false);
        }
        player.getInventory().setChanged();
        player.containerMenu.broadcastChanges();
        player.displayClientMessage(Component.translatable("status.voidgen.unequipped"), true);
        sendSync(player);
        return true;
    }

    public static void setAuto(ServerPlayer player, boolean enabled) {
        if (!hasCard(player)) {
            player.displayClientMessage(Component.translatable("status.voidgen.no_card"), true);
            return;
        }
        CompoundTag data = data(player);
        data.putBoolean("Auto", enabled);
        data.putLong("LastScan", 0L);
        store(player, data);
        player.displayClientMessage(Component.translatable(enabled ? "status.voidgen.auto_enabled" : "status.voidgen.auto_disabled"), true);
        sendSync(player);
    }

    // ------------------------------------------------------------------ binding

    private static void toggleBound(Player player, BlockPos pos) {
        List<BlockPos> bounds = boundsOf(player);
        if (bounds.remove(pos)) {
            setBounds(player, bounds);
            if (player instanceof ServerPlayer serverPlayer) {
                serverPlayer.displayClientMessage(Component.translatable("status.voidgen.unbound", bounds.size()), true);
                sendSync(serverPlayer);
            }
            return;
        }
        if (bounds.size() >= VoidStats.MAX_BOUND_TARGETS) {
            player.displayClientMessage(Component.translatable("status.voidgen.bound_full", VoidStats.MAX_BOUND_TARGETS), true);
            return;
        }
        bounds.add(pos.immutable());
        setBounds(player, bounds);
        if (player instanceof ServerPlayer serverPlayer) {
            serverPlayer.displayClientMessage(Component.translatable("status.voidgen.bound", bounds.size()), true);
            sendSync(serverPlayer);
        }
    }

    public static void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        Level level = event.getLevel();
        if (level.isClientSide() || event.getHand() != InteractionHand.MAIN_HAND) {
            return;
        }
        Player player = event.getEntity();
        if (!hasCard(player) || !player.getMainHandItem().isEmpty()) {
            return;
        }
        BlockPos pos = event.getPos();
        if (level.getBlockState(pos).is(VoidGen.VOID_GENERATOR.get()) || level.getBlockEntity(pos) == null) {
            return;
        }
        IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
        if (target == null || !target.canReceive()) {
            return;
        }
        toggleBound(player, pos);
    }

    // ------------------------------------------------------------------ auto-connect

    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.level().isClientSide()) {
            return;
        }
        autoScan(player);
    }

    private static void autoScan(ServerPlayer player) {
        CompoundTag data = data(player);
        if (!data.getBoolean("Equipped") || !data.getBoolean("Auto")) {
            return;
        }
        Level level = player.level();
        long now = level.getGameTime();
        if (now - data.getLong("LastScan") < 20L) {
            return;
        }
        data.putLong("LastScan", now);
        List<BlockPos> bounds = boundsOf(player);
        if (bounds.size() >= VoidStats.MAX_BOUND_TARGETS) {
            return;
        }
        List<BlockPos> receivers = VoidPowerNetwork.receivers(level.dimension());
        int size = receivers.size();
        if (size == 0) {
            return;
        }
        int start = Math.floorMod(data.getInt("ScanCursor"), size);
        int checks = Math.min(64, size);
        double radiusSq = (double) BIND_RADIUS * BIND_RADIUS;
        boolean added = false;
        for (int i = 0; i < checks && bounds.size() < VoidStats.MAX_BOUND_TARGETS; i++) {
            BlockPos pos = receivers.get((start + i) % size);
            if (!level.isLoaded(pos) || bounds.contains(pos)) {
                continue;
            }
            double dx = pos.getX() + 0.5D - player.getX();
            double dy = pos.getY() + 0.5D - player.getY();
            double dz = pos.getZ() + 0.5D - player.getZ();
            if (dx * dx + dy * dy + dz * dz > radiusSq) {
                continue;
            }
            if (level.getBlockState(pos).is(VoidGen.VOID_GENERATOR.get())) {
                continue;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
            if (target == null || !target.canReceive()) {
                continue;
            }
            bounds.add(pos.immutable());
            added = true;
        }
        setBounds(player, bounds);
        data.putInt("ScanCursor", (start + checks) % size);
        store(player, data);
        if (added) {
            sendSync(player);
        }
    }

    // ------------------------------------------------------------------ wireless push

    /** True when at least one player in this dimension has a Binding Card equipped. */
    public static boolean anyEquipped(Level level) {
        for (Player player : level.players()) {
            if (hasCard(player)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Feeds the union of the bound sets of every equipped player. Bound machines are an
     * explicit choice, so they ignore the generator's range; range only governs the legacy
     * broadcast mode and the auto-connect scan.
     */
    public static VoidPowerNetwork.PushResult push(Level level, BlockPos origin, long available, boolean aeOutput, int cursor) {
        List<BlockPos> targets = collectBounds(level);
        if (targets.isEmpty() || available <= 0) {
            return new VoidPowerNetwork.PushResult(0, 0);
        }
        int size = targets.size();
        int start = Math.floorMod(cursor, size);
        int checks = Math.min(CHECK_COUNT, size);
        long remaining = available;
        long moved = 0;
        List<BlockPos> stale = new ArrayList<>();
        for (int i = 0; i < checks && remaining > 0; i++) {
            BlockPos pos = targets.get((start + i) % size);
            if (pos.equals(origin) || !level.isLoaded(pos)) {
                continue;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
            if (target == null || !target.canReceive()) {
                stale.add(pos);
                continue;
            }
            if (VoidStats.isAeAcceptorBlock(level.getBlockState(pos).getBlock()) && !aeOutput) {
                continue;
            }
            int accepted = target.receiveEnergy((int) Math.min(Integer.MAX_VALUE, remaining), false);
            if (accepted > 0) {
                remaining -= accepted;
                moved += accepted;
            }
        }
        if (!stale.isEmpty()) {
            removeStale(level, stale);
        }
        return new VoidPowerNetwork.PushResult(moved, (start + checks) % size);
    }

    private static List<BlockPos> collectBounds(Level level) {
        Set<BlockPos> union = new LinkedHashSet<>();
        for (Player player : level.players()) {
            if (hasCard(player)) {
                union.addAll(boundsOf(player));
            }
        }
        return new ArrayList<>(union);
    }

    private static void removeStale(Level level, List<BlockPos> stale) {
        for (Player player : level.players()) {
            if (!hasCard(player)) {
                continue;
            }
            List<BlockPos> bounds = boundsOf(player);
            if (bounds.removeAll(stale)) {
                setBounds(player, bounds);
            }
        }
    }

    // ------------------------------------------------------------------ sync / lifecycle

    public static void sendSync(ServerPlayer player) {
        CompoundTag data = data(player);
        PacketDistributor.sendToPlayer(player,
                new VoidNet.SyncPayload(data.getBoolean("Equipped"), data.getBoolean("Auto"), data.getLongArray("Bound").length));
    }

    public static void onLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            sendSync(player);
        }
    }

    public static void onClone(PlayerEvent.Clone event) {
        CompoundTag source = event.getOriginal().getPersistentData();
        if (source.contains(ROOT, Tag.TAG_COMPOUND)) {
            event.getEntity().getPersistentData().put(ROOT, source.getCompound(ROOT).copy());
        }
    }
}
