package com.voidgen.block;

import java.util.List;

import com.voidgen.VoidGen;
import com.voidgen.VoidPowerNetwork;
import com.voidgen.VoidStats;
import com.voidgen.VoidValue;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.items.ItemStackHandler;

/**
 * ME 虚无供应器：
 * - SUPPLY 模式：吃掉槽内的「虚无值」物品（ME 输出总线送来），把虚无值推给附近需要虚无值的机器；
 * - IMPORT 模式：从相邻的虚无收集装置抽虚无值，填成「虚无值」物品（ME 输入总线可吸进 AE 虚无磁盘）。
 */
public class MeVoidSupplierBlockEntity extends BlockEntity {
    public static final int MODE_SUPPLY = 0;
    public static final int MODE_IMPORT = 1;
    public static final long CAPACITY = 10_000_000L;
    private static final long VOID_PER_ITEM = 1_000L;
    private static final long PUSH_PER_TARGET = 200L;
    private static final long PUSH_BUDGET = 4_000L;
    private static final int RADIUS = 16;
    private static final int CHECKS_PER_TICK = 32;

    private final ItemStackHandler slot = new ItemStackHandler(1) {
        @Override
        public boolean isItemValid(int index, ItemStack stack) {
            return stack.is(VoidGen.VOID_VALUE.get());
        }

        @Override
        protected void onContentsChanged(int index) {
            MeVoidSupplierBlockEntity.this.setChanged();
        }
    };

    private long buffer;
    private int mode = MODE_SUPPLY;
    private int cursor;

    public MeVoidSupplierBlockEntity(BlockPos pos, BlockState state) {
        super(VoidGen.ME_VOID_SUPPLIER_BE.get(), pos, state);
    }

    public void tick(Level level) {
        if (level.isClientSide()) {
            return;
        }
        if (mode == MODE_SUPPLY) {
            consumeItems();
            pushNearby(level);
        } else {
            pullAdjacent(level);
            fillSlot();
        }
    }

    private void consumeItems() {
        if (buffer >= CAPACITY) {
            return;
        }
        ItemStack stack = slot.getStackInSlot(0);
        if (stack.isEmpty() || !stack.is(VoidGen.VOID_VALUE.get())) {
            return;
        }
        long room = CAPACITY - buffer;
        int count = (int) Math.min(stack.getCount(), room / VOID_PER_ITEM);
        if (count <= 0) {
            return;
        }
        buffer += (long) count * VOID_PER_ITEM;
        stack.shrink(count);
        slot.setStackInSlot(0, stack);
    }

    private void pushNearby(Level level) {
        if (buffer <= 0) {
            return;
        }
        List<BlockPos> receivers = VoidPowerNetwork.receivers(level.dimension());
        if (receivers.isEmpty()) {
            return;
        }
        int size = receivers.size();
        int checks = Math.min(size, CHECKS_PER_TICK);
        long budget = Math.min(buffer, PUSH_BUDGET);
        long moved = 0;
        double rangeSq = (double) RADIUS * RADIUS;
        for (int i = 0; i < checks && budget > 0; i++) {
            BlockPos target = receivers.get((cursor + i) % size);
            if (!level.isLoaded(target) || target.distSqr(worldPosition) > rangeSq) {
                continue;
            }
            long want = Math.min(PUSH_PER_TARGET, budget);
            BlockEntity be = level.getBlockEntity(target);
            long got = 0;
            if (be instanceof VoidGeneratorBlockEntity generator) {
                got = generator.addVoid(want);
            } else if (be instanceof VoidFurnaceBlockEntity furnace) {
                got = furnace.addVoid(want);
            }
            moved += got;
            budget -= got;
        }
        if (moved > 0) {
            buffer -= moved;
            setChanged();
        }
        cursor = (cursor + CHECKS_PER_TICK) % Math.max(1, size);
    }

    private void pullAdjacent(Level level) {
        if (buffer >= CAPACITY) {
            return;
        }
        for (Direction direction : Direction.values()) {
            BlockEntity be = level.getBlockEntity(worldPosition.relative(direction));
            if (be instanceof NothingnessCollectorBlockEntity collector) {
                long got = collector.drain(Math.min(CAPACITY - buffer, 10_000L));
                if (got > 0) {
                    buffer += got;
                    setChanged();
                }
                if (buffer >= CAPACITY) {
                    return;
                }
            }
        }
    }

    private void fillSlot() {
        if (buffer < VOID_PER_ITEM) {
            return;
        }
        ItemStack current = slot.getStackInSlot(0);
        int currentCount = current.isEmpty() ? 0 : current.getCount();
        if (currentCount >= 64) {
            return;
        }
        long maxItems = Math.min(64 - currentCount, buffer / VOID_PER_ITEM);
        if (maxItems <= 0) {
            return;
        }
        int count = (int) maxItems;
        if (current.isEmpty()) {
            slot.setStackInSlot(0, new ItemStack(VoidGen.VOID_VALUE.get(), count));
        } else {
            current.grow(count);
            slot.setStackInSlot(0, current);
        }
        buffer -= (long) count * VOID_PER_ITEM;
        setChanged();
    }

    public void toggleMode() {
        mode = mode == MODE_SUPPLY ? MODE_IMPORT : MODE_SUPPLY;
        setChanged();
    }

    public int mode() {
        return mode;
    }

    public long buffer() {
        return buffer;
    }

    public int slotCount() {
        ItemStack stack = slot.getStackInSlot(0);
        return stack.isEmpty() ? 0 : stack.getCount();
    }

    public ItemStackHandler getItemHandler() {
        return slot;
    }

    public void dropContents(Level level) {
        ItemStack stack = slot.getStackInSlot(0);
        if (!stack.isEmpty()) {
            Block.popResource(level, worldPosition, stack);
            slot.setStackInSlot(0, ItemStack.EMPTY);
        }
    }

    public void statusLine() {
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putLong("Buffer", buffer);
        tag.putInt("Mode", mode);
        tag.put("Slot", slot.serializeNBT(registries));
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        buffer = tag.getLong("Buffer");
        mode = tag.getInt("Mode");
        slot.deserializeNBT(registries, tag.getCompound("Slot"));
    }
}
