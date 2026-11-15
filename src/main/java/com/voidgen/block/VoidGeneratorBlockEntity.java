package com.voidgen.block;

import com.voidgen.VoidGen;
import com.voidgen.VoidPowerNetwork;
import com.voidgen.VoidStats;
import com.voidgen.item.UpgradeCardItem;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.item.ItemStack;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.energy.IEnergyStorage;
import net.neoforged.neoforge.items.ItemStackHandler;

/**
 * The Void Generator block entity: generates FE out of nothing, stores it, pushes it to
 * adjacent machines, then wirelessly.
 *
 * <p>Wireless routing depends on the Binding Card, which lives on the player (accessory
 * slot), not on the generator: if at least one player in the dimension has a card equipped,
 * generators feed the union of all their bound machines; otherwise they fall back to the
 * legacy broadcast to every player-placed machine in range.</p>
 */
public class VoidGeneratorBlockEntity extends BlockEntity implements IEnergyStorage, MenuProvider {
    public static final int DATA_SLOTS = 8;
    public static final int UPGRADE_SLOTS = VoidStats.CARD_SLOTS;
    public static final int MENU_SLOTS = UPGRADE_SLOTS;

    private final ItemStackHandler cards = new ItemStackHandler(MENU_SLOTS) {
        @Override
        protected void onContentsChanged(int slot) {
            setChanged();
        }

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            return VoidStats.isSlotCard(stack);
        }
    };

    private long energy;
    private long voidBuffer;
    private int tier;
    private boolean aeOutput;
    private int wirelessCursor;

    private final ContainerData data = new ContainerData() {
        @Override
        public int get(int index) {
            return switch (index) {
                case 0 -> (int) (energy & 0xFFFFFFFFL);
                case 1 -> (int) (energy >>> 32);
                case 2 -> (int) Math.min(Integer.MAX_VALUE, rate());
                case 3 -> (int) (capacity() & 0xFFFFFFFFL);
                case 4 -> (int) (capacity() >>> 32);
                case 5 -> tier;
                case 6 -> rangeInt();
                case 7 -> aeOutput ? 1 : 0;
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
            // The block entity is authoritative on the server; client-side deltas are
            // written into the SimpleContainerData used by the client menu instead.
        }

        @Override
        public int getCount() {
            return DATA_SLOTS;
        }
    };

    public VoidGeneratorBlockEntity(BlockPos pos, BlockState state) {
        super(VoidGen.VOID_GENERATOR_BE.get(), pos, state);
    }

    // Global tick registry (v2.2.3): generators tick from ServerTickEvent.Post, so a
    // force-loaded chunk keeps running even when its chunk is not entity-ticking.
    private static final java.util.Map<ResourceKey<Level>, java.util.Set<BlockPos>> ACTIVE = new java.util.concurrent.ConcurrentHashMap<>();

    @Override
    public void setLevel(Level level) {
        super.setLevel(level);
        if (level != null && !level.isClientSide()) {
            ACTIVE.computeIfAbsent(level.dimension(), key -> java.util.concurrent.ConcurrentHashMap.newKeySet()).add(worldPosition);
        }
    }

    @Override
    public void setRemoved() {
        Level level = getLevel();
        if (level != null) {
            java.util.Set<BlockPos> set = ACTIVE.get(level.dimension());
            if (set != null) {
                set.remove(worldPosition);
            }
        }
        super.setRemoved();
    }

    public static void tickAll(MinecraftServer server) {
        for (ServerLevel level : server.getAllLevels()) {
            java.util.Set<BlockPos> set = ACTIVE.get(level.dimension());
            if (set == null || set.isEmpty()) {
                continue;
            }
            for (BlockPos pos : new java.util.ArrayList<>(set)) {
                if (!level.isLoaded(pos)) {
                    continue;
                }
                if (level.getBlockEntity(pos) instanceof VoidGeneratorBlockEntity generator) {
                    generator.tick(level);
                }
            }
        }
    }

    // ------------------------------------------------------------------ ticking

    public void tick(Level level) {
        if (level.isClientSide()) {
            return;
        }
        boolean changed = false;
        long rate = rate();
        long capacity = capacity();
        if (voidBuffer > 0) {
            // 虚无发电机工作时要消耗虚无值：每 tick 5 点。
            voidBuffer -= Math.min(voidBuffer, 5L);
            if (energy < capacity) {
                long added = Math.min(rate, capacity - energy);
                if (added > 0) {
                    energy += added;
                    changed = true;
                }
            }
        }
        long budget = Math.min(energy, rate);
        if (budget > 0) {
            long moved = pushAdjacent(level, budget);
            if (moved > 0) {
                energy -= moved;
                changed = true;
            }
        }
        long rateLeft = rate;
        long wirelessBudget = Math.min(energy, rateLeft);
        if (wirelessBudget > 0) {
            VoidPowerNetwork.PushResult result = VoidPowerNetwork.push(
                    level, worldPosition, wirelessBudget, rate, range(), aeOutput, wirelessCursor);
            if (result.moved() > 0) {
                energy -= result.moved();
                rateLeft -= result.moved();
                changed = true;
            }
            wirelessCursor = result.cursor();
        }
        // cross-dimension broadcast (v2.2.2): the same generator feeds player-placed
        // receivers in every loaded dimension, not only its own.
        if (rateLeft > 0 && energy > 0 && level.getServer() != null) {
            for (net.minecraft.server.level.ServerLevel other : level.getServer().getAllLevels()) {
                if (other == level || rateLeft <= 0 || energy <= 0) {
                    continue;
                }
                long want = Math.min(energy, rateLeft);
                VoidPowerNetwork.PushResult cross = VoidPowerNetwork.pushInfinite(other, worldPosition, want, rateLeft, aeOutput, wirelessCursor, java.util.Set.of());
                if (cross.moved() > 0) {
                    energy -= cross.moved();
                    rateLeft -= cross.moved();
                    changed = true;
                }
                wirelessCursor = cross.cursor();
            }
        }
        if (changed) {
            setChanged();
        }
    }

    private long pushAdjacent(Level level, long budget) {
        long movedTotal = 0;
        long remaining = budget;
        for (Direction direction : Direction.values()) {
            if (remaining <= 0) {
                break;
            }
            IEnergyStorage target = level.getCapability(Capabilities.EnergyStorage.BLOCK, worldPosition.relative(direction), direction.getOpposite());
            if (target == null || !target.canReceive()) {
                continue;
            }
            int accepted = target.receiveEnergy((int) Math.min(Integer.MAX_VALUE, remaining), false);
            if (accepted > 0) {
                remaining -= accepted;
                movedTotal += accepted;
            }
        }
        return movedTotal;
    }

    // ------------------------------------------------------------------ stats

    public long rate() {
        return VoidStats.rate(tier,
                VoidStats.count(cards, UpgradeCardItem.Type.ACCELERATION),
                VoidStats.count(cards, UpgradeCardItem.Type.OVERCLOCK));
    }

    public long capacity() {
        return VoidStats.capacity(tier, VoidStats.count(cards, UpgradeCardItem.Type.CAPACITY));
    }

    public long range() {
        return VoidStats.range(VoidStats.count(cards, UpgradeCardItem.Type.RANGE));
    }

    public int rangeInt() {
        long range = range();
        return range == Long.MAX_VALUE ? -1 : (int) Math.min(Integer.MAX_VALUE, range);
    }

    public long energy() {
        return energy;
    }

    public int tier() {
        return tier;
    }

    public boolean aeOutput() {
        return aeOutput;
    }

    public ItemStackHandler cards() {
        return cards;
    }

    public ContainerData data() {
        return data;
    }

    public IEnergyStorage getEnergyStorage() {
        return this;
    }

    public boolean tryUpgrade(int upgradeTier) {
        if (upgradeTier == tier + 1 && upgradeTier <= VoidStats.MAX_TIER) {
            tier = upgradeTier;
            setChanged();
            return true;
        }
        return false;
    }

    public void toggleAe() {
        aeOutput = !aeOutput;
        setChanged();
    }

    public boolean tryInsertCard(ItemStack stack) {
        if (!VoidStats.isSlotCard(stack)) {
            return false;
        }
        ItemStack single = stack.copyWithCount(1);
        for (int slot = 0; slot < UPGRADE_SLOTS; slot++) {
            ItemStack remainder = cards.insertItem(slot, single, true);
            if (remainder.isEmpty()) {
                cards.insertItem(slot, single, false);
                return true;
            }
        }
        return false;
    }

    // ------------------------------------------------------------------ energy api

    @Override
    public int receiveEnergy(int maxReceive, boolean simulate) {
        return 0;
    }

    @Override
    public int extractEnergy(int maxExtract, boolean simulate) {
        int extracted = (int) Math.min(Math.min(maxExtract, energy), Integer.MAX_VALUE);
        if (extracted > 0 && !simulate) {
            energy -= extracted;
            setChanged();
        }
        return extracted;
    }

    @Override
    public int getEnergyStored() {
        return (int) Math.min(energy, Integer.MAX_VALUE);
    }

    @Override
    public int getMaxEnergyStored() {
        return (int) Math.min(capacity(), Integer.MAX_VALUE);
    }

    @Override
    public boolean canExtract() {
        return true;
    }

    @Override
    public boolean canReceive() {
        return false;
    }

    // ------------------------------------------------------------------ persistence

    public long addVoid(long amount) {
        long room = com.voidgen.VoidValue.MACHINE_BUFFER - voidBuffer;
        long accepted = Math.min(Math.max(0L, room), Math.max(0L, amount));
        if (accepted > 0) {
            voidBuffer += accepted;
            setChanged();
        }
        return accepted;
    }

    public long voidAmount() {
        return voidBuffer;
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putLong("Energy", energy);
        tag.putLong("VoidBuffer", voidBuffer);
        tag.putInt("Tier", tier);
        tag.putBoolean("AeOutput", aeOutput);
        tag.put("Cards", cards.serializeNBT(registries));
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        energy = tag.getLong("Energy");
        voidBuffer = tag.getLong("VoidBuffer");
        tier = tag.getInt("Tier");
        aeOutput = tag.getBoolean("AeOutput");
        if (tag.contains("Cards")) {
            cards.deserializeNBT(registries, tag.getCompound("Cards"));
        }
    }

    /** 破坏方块时把卡槽里的卡掉出来。 */
    public void dropContents(Level level) {
        for (int i = 0; i < cards.getSlots(); i++) {
            ItemStack stack = cards.getStackInSlot(i);
            if (!stack.isEmpty()) {
                net.minecraft.world.level.block.Block.popResource(level, worldPosition, stack);
                cards.setStackInSlot(i, ItemStack.EMPTY);
            }
        }
    }

    // ------------------------------------------------------------------ menu

    @Override
    public Component getDisplayName() {
        return Component.translatable("block.voidgen.void_generator");
    }

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory playerInventory, Player player) {
        return new VoidGeneratorMenu(containerId, playerInventory, this);
    }
}
