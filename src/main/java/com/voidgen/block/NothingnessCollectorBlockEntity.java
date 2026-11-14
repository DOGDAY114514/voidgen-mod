package com.voidgen.block;

import com.voidgen.VoidGen;
import com.voidgen.VoidValue;
import com.voidgen.item.VoidStorageItem;

import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.items.ItemStackHandler;

/**
 * 虚无收集装置：每 tick 产虚无值进内部缓冲，槽位里的存储器先从缓冲自动充能；
 * 全部虚无值 = 存储器里的虚无值 + 收集装置自身缓冲。
 */
public class NothingnessCollectorBlockEntity extends BlockEntity implements MenuProvider {
    public static final int STORAGE_SLOTS = 16;
    public static final int DATA_SLOTS = 10;

    private final ItemStackHandler storages = new ItemStackHandler(STORAGE_SLOTS) {
        @Override
        protected void onContentsChanged(int slot) {
            setChanged();
        }
    };
    private long buffer;
    private int ticker;

    private final ContainerData data = new ContainerData() {
        @Override
        public int get(int index) {
            long total = totalValue();
            return switch (index) {
                case 0 -> (int) (buffer & 0xFFFFFFFFL);
                case 1 -> (int) (buffer >>> 32);
                case 2 -> rate();
                case 3 -> (int) (capacity() & 0xFFFFFFFFL);
                case 4 -> (int) (capacity() >>> 32);
                case 5 -> tier();
                case 6 -> storageCount();
                case 7 -> (int) (total & 0xFFFFFFFFL);
                case 8 -> (int) (total >>> 32);
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
        }

        @Override
        public int getCount() {
            return DATA_SLOTS;
        }
    };

    public NothingnessCollectorBlockEntity(BlockPos pos, BlockState state) {
        super(VoidGen.NOTHING_COLLECTOR_BE.get(), pos, state);
    }

    public int tier() {
        return getBlockState().getBlock() instanceof NothingnessCollectorBlock collector ? collector.tier() : 1;
    }

    public int rate() {
        return switch (tier()) {
            case 1 -> 100;
            case 2 -> 200;
            case 3 -> 400;
            case 4 -> 800;
            default -> 1_600;
        };
    }

    public boolean infiniteStorage() {
        for (int i = 0; i < storages.getSlots(); i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (stack.getItem() instanceof VoidStorageItem storage && storage.cap() == Long.MAX_VALUE) {
                return true;
            }
        }
        return false;
    }

    public long capacity() {
        if (infiniteStorage()) {
            return Long.MAX_VALUE;
        }
        long cap = VoidValue.BASE_COLLECTOR_BUFFER;
        for (int i = 0; i < storages.getSlots(); i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (stack.getItem() instanceof VoidStorageItem storage) {
                cap += storage.cap();
            }
        }
        return cap;
    }

    public int storageCount() {
        int count = 0;
        for (int i = 0; i < storages.getSlots(); i++) {
            if (storages.getStackInSlot(i).getItem() instanceof VoidStorageItem) {
                count++;
            }
        }
        return count;
    }

    public long buffer() {
        return buffer;
    }

    /** 收集装置里的全部虚无值：缓冲 + 存储器。 */
    public long totalValue() {
        long total = buffer;
        for (int i = 0; i < storages.getSlots(); i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (stack.getItem() instanceof VoidStorageItem) {
                total += Math.max(0L, VoidValue.get(stack));
                if (total < 0) {
                    return Long.MAX_VALUE;
                }
            }
        }
        return total;
    }

    /** Used by a neighbouring 虚无发散器（先扣缓冲，再扣存储器）。 */
    public long drain(long amount) {
        return drainTotal(amount);
    }

    public long drainTotal(long amount) {
        long want = Math.max(0L, amount);
        if (want <= 0) {
            return 0L;
        }
        long taken = Math.min(buffer, want);
        buffer -= taken;
        want -= taken;
        for (int i = 0; i < storages.getSlots() && want > 0; i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (!(stack.getItem() instanceof VoidStorageItem)) {
                continue;
            }
            long have = VoidValue.get(stack);
            long take = Math.min(have, want);
            if (take > 0) {
                VoidValue.set(stack, have - take);
                want -= take;
                taken += take;
            }
        }
        if (taken > 0) {
            setChanged();
        }
        return taken;
    }

    public void tick(Level level) {
        if (level.isClientSide()) {
            return;
        }
        ticker++;
        if (ticker % 5 == 0) {
            setChanged();
        }
        long cap = capacity();
        long next = buffer + rate();
        if (next < buffer) {
            next = Long.MAX_VALUE;
        }
        buffer = Math.min(cap, next);
        chargeStorages();
    }

    /** 存储器优先从缓冲自动充能（每槽 1,000/tick），充满后保留堆叠数量变成充盈存储器。 */
    private void chargeStorages() {
        for (int i = 0; i < storages.getSlots() && buffer > 0; i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (!(stack.getItem() instanceof VoidStorageItem storage) || VoidValue.isFull(stack)) {
                continue;
            }
            long room = storage.cap() == Long.MAX_VALUE ? Long.MAX_VALUE : storage.cap() - VoidValue.get(stack);
            long take = Math.min(room, Math.min(buffer, 1_000L));
            if (take > 0) {
                VoidValue.add(stack, take);
                buffer -= take;
                if (VoidValue.isFull(stack)) {
                    storages.setStackInSlot(i, new ItemStack(storage.filled(), stack.getCount()));
                }
            }
        }
    }

    /** 破坏方块时把里面的存储器掉出来。 */
    public void dropContents(Level level) {
        for (int i = 0; i < storages.getSlots(); i++) {
            ItemStack stack = storages.getStackInSlot(i);
            if (!stack.isEmpty()) {
                Block.popResource(level, worldPosition, stack);
                storages.setStackInSlot(i, ItemStack.EMPTY);
            }
        }
    }

    public ItemStackHandler storages() {
        return storages;
    }

    public ContainerData data() {
        return data;
    }

    @Override
    public Component getDisplayName() {
        return Component.translatable("block.voidgen.nothing_collector_" + tier());
    }

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory inventory, Player player) {
        return new NothingnessCollectorMenu(containerId, inventory, this);
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putLong("Buffer", buffer);
        tag.put("Storages", storages.serializeNBT(registries));
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        buffer = tag.getLong("Buffer");
        if (tag.contains("Storages")) {
            storages.deserializeNBT(registries, tag.getCompound("Storages"));
        }
    }
}
