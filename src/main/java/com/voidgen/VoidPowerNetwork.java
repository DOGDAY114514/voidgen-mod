package com.voidgen;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.event.level.BlockEvent;
import net.neoforged.neoforge.event.level.ChunkEvent;

/**
 * Tracks blocks placed by players (only blocks that carry a block entity are interesting)
 * and feeds them from Void Generators within range. This is the wireless half of the
 * generator: no cables, no nodes - place a machine, place the generator, done.
 */
public final class VoidPowerNetwork {
    private static final int MAX_CHECKS_PER_TICK = 32;
    private static final Map<ResourceKey<Level>, List<BlockPos>> RECEIVERS = new ConcurrentHashMap<>();
    private static final Map<ResourceKey<Level>, Set<BlockPos>> SEEN = new ConcurrentHashMap<>();

    private VoidPowerNetwork() {
    }

    public static void onPlace(BlockEvent.EntityPlaceEvent event) {
        if (!(event.getEntity() instanceof Player)) {
            return;
        }
        if (!(event.getLevel() instanceof Level level) || level.isClientSide()) {
            return;
        }
        BlockPos pos = event.getBlockSnapshot().getPos();
        if (level.getBlockEntity(pos) == null) {
            return;
        }
        register(level, pos);
    }

    /** Adds a receiver position (idempotent). */
    public static void register(Level level, BlockPos pos) {
        if (level.isClientSide() || level.getBlockEntity(pos) == null) {
            return;
        }
        Set<BlockPos> seen = SEEN.computeIfAbsent(level.dimension(), key -> new HashSet<>());
        if (seen.add(pos)) {
            RECEIVERS.computeIfAbsent(level.dimension(), key -> new ArrayList<>()).add(pos);
        }
    }

    /**
     * Chunk-load discovery: scans the loaded chunk's block entities and registers every
     * machine that exposes an FE handler. This is what makes the generator "just connect"
     * to machines that existed before the mod was installed or before the server restarted.
     */
    public static void onChunkLoad(ChunkEvent.Load event) {
        if (!(event.getLevel() instanceof ServerLevel level) || level.isClientSide()) {
            return;
        }
        if (!(event.getChunk() instanceof LevelChunk chunk)) {
            return;
        }
        // Chunks loaded from disk keep their block entities as *pending NBT* until
        // something asks for them; LevelChunk.getBlockEntities() is therefore empty here.
        // getBlockEntitiesPos() also lists the pending ones, and the capability lookup
        // forces each pending block entity to be instantiated (LevelChunk.getBlockEntity
        // promotes it) before we register it.
        for (BlockPos pos : chunk.getBlockEntitiesPos()) {
            if (level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null) != null) {
                register(level, pos);
            }
        }
    }

    public static void onBreak(BlockEvent.BreakEvent event) {
        if (!(event.getLevel() instanceof Level level) || level.isClientSide()) {
            return;
        }
        List<BlockPos> list = RECEIVERS.get(level.dimension());
        if (list != null) {
            list.remove(event.getPos());
        }
        Set<BlockPos> seen = SEEN.get(level.dimension());
        if (seen != null) {
            seen.remove(event.getPos());
        }
    }

    public record PushResult(long moved, int cursor) {
    }

    /**
     * Live view of the player-placed receivers in one dimension. Used by the Binding Card's
     * auto-connect mode to discover machines that should be added to a generator's bound set.
     */
    public static List<BlockPos> receivers(ResourceKey<Level> dimension) {
        List<BlockPos> list = RECEIVERS.get(dimension);
        return list == null ? List.of() : list;
    }

    /** Cross-dimension push: no distance check, only chunk-loaded receivers in that level. */
    public static PushResult pushInfinite(Level level, BlockPos origin, long available, long ratePerTick, boolean aeOutput, int cursor, java.util.Set<BlockPos> skip) {
        List<BlockPos> list = RECEIVERS.get(level.dimension());
        if (list == null || list.isEmpty() || available <= 0 || ratePerTick <= 0) {
            return new PushResult(0, 0);
        }
        int size = list.size();
        long budget = Math.min(available, ratePerTick);
        long moved = 0;
        int checks = Math.min(MAX_CHECKS_PER_TICK, size);
        int start = Math.floorMod(cursor, size);
        for (int i = 0; i < checks && budget > 0; i++) {
            BlockPos pos = list.get((start + i) % size);
            if (pos.equals(origin) || !level.isLoaded(pos) || skip.contains(pos)) {
                continue;
            }
            BlockState state = level.getBlockState(pos);
            boolean aeAcceptor = VoidStats.isAeAcceptorBlock(state.getBlock());
            if (aeAcceptor && !aeOutput) {
                continue;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
            if (target == null || !target.canReceive()) {
                continue;
            }
            int accepted = target.receiveEnergy((int) Math.min(Integer.MAX_VALUE, budget), false);
            if (accepted > 0) {
                budget -= accepted;
                moved += accepted;
            }
        }
        return new PushResult(moved, (start + checks) % size);
    }

    public static PushResult push(Level level, BlockPos origin, long available, long ratePerTick, long range, boolean aeOutput, int cursor) {
        return push(level, origin, available, ratePerTick, range, aeOutput, cursor, java.util.Set.of());
    }

    /**
     * Same broadcast push, but positions in {@code skip} are ignored (the generator
     * handles them separately, e.g. binding-card overrides).
     */
    public static PushResult push(Level level, BlockPos origin, long available, long ratePerTick, long range, boolean aeOutput, int cursor, java.util.Set<BlockPos> skip) {
        List<BlockPos> list = RECEIVERS.get(level.dimension());
        if (list == null || list.isEmpty() || available <= 0 || ratePerTick <= 0) {
            return new PushResult(0, 0);
        }
        int size = list.size();
        long budget = Math.min(available, ratePerTick);
        long moved = 0;
        int checks = Math.min(MAX_CHECKS_PER_TICK, size);
        boolean infinite = range == Long.MAX_VALUE;
        double rangeSq = infinite ? 0.0D : (double) range * (double) range;
        double ox = origin.getX() + 0.5D;
        double oy = origin.getY() + 0.5D;
        double oz = origin.getZ() + 0.5D;
        int start = Math.floorMod(cursor, size);
        for (int i = 0; i < checks && budget > 0; i++) {
            BlockPos pos = list.get((start + i) % size);
            if (pos.equals(origin) || !level.isLoaded(pos) || skip.contains(pos)) {
                continue;
            }
            if (!infinite) {
                double dx = pos.getX() + 0.5D - ox;
                double dy = pos.getY() + 0.5D - oy;
                double dz = pos.getZ() + 0.5D - oz;
                if (dx * dx + dy * dy + dz * dz > rangeSq) {
                    continue;
                }
            }
            BlockState state = level.getBlockState(pos);
            boolean aeAcceptor = VoidStats.isAeAcceptorBlock(state.getBlock());
            if (aeAcceptor && !aeOutput) {
                continue;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, pos, null);
            if (target == null || !target.canReceive()) {
                continue;
            }
            int accepted = target.receiveEnergy((int) Math.min(Integer.MAX_VALUE, budget), false);
            if (accepted > 0) {
                budget -= accepted;
                moved += accepted;
            }
        }
        return new PushResult(moved, (start + checks) % size);
    }
}
