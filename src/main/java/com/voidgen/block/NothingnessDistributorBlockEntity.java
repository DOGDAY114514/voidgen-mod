package com.voidgen.block;

import java.util.ArrayList;
import java.util.List;

import com.voidgen.VoidValue;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

/** 虚无发散器方块实体：从相邻收集装置抽取虚无值，再分发给 16 格内的发电机/熔炉。 */
public class NothingnessDistributorBlockEntity extends BlockEntity {
    private static final long PULL_PER_TICK = 1_000L;
    private static final long PUSH_PER_TARGET = 200L;

    private long buffer;
    private int scanCooldown;
    private final List<BlockPos> targets = new ArrayList<>();

    public NothingnessDistributorBlockEntity(BlockPos pos, BlockState state) {
        super(com.voidgen.VoidGen.NOTHING_DISTRIBUTOR_BE.get(), pos, state);
    }

    public long buffer() {
        return buffer;
    }

    public int targets() {
        return targets.size();
    }

    public long accept(long amount) {
        long room = VoidValue.DISTRIBUTOR_BUFFER - buffer;
        long accepted = Math.min(Math.max(0L, room), Math.max(0L, amount));
        buffer += accepted;
        if (accepted > 0) {
            setChanged();
        }
        return accepted;
    }

    public long drain(long amount) {
        long taken = Math.min(Math.max(0L, buffer), Math.max(0L, amount));
        buffer -= taken;
        if (taken > 0) {
            setChanged();
        }
        return taken;
    }

    public void tick(Level level) {
        if (level.isClientSide()) {
            return;
        }
        // 1) pull from an adjacent collector (any of the six faces)
        if (buffer < VoidValue.DISTRIBUTOR_BUFFER) {
            for (Direction direction : Direction.values()) {
                BlockEntity be = level.getBlockEntity(this.worldPosition.relative(direction));
                if (be instanceof NothingnessCollectorBlockEntity collector) {
                    long pulled = collector.drain(Math.min(PULL_PER_TICK, VoidValue.DISTRIBUTOR_BUFFER - buffer));
                    if (pulled > 0) {
                        accept(pulled);
                        break;
                    }
                }
            }
        }
        // 2) rescan targets periodically
        if (--scanCooldown <= 0) {
            scanCooldown = 20;
            scan(level);
        }
        // 3) feed machines
        if (buffer <= 0) {
            return;
        }
        for (BlockPos pos : targets) {
            if (buffer <= 0) {
                break;
            }
            BlockEntity be = level.getBlockEntity(pos);
            long accepted = 0L;
            if (be instanceof VoidGeneratorBlockEntity generator) {
                accepted = generator.addVoid(Math.min(PUSH_PER_TARGET, buffer));
            } else if (be instanceof VoidFurnaceBlockEntity furnace) {
                accepted = furnace.addVoid(Math.min(PUSH_PER_TARGET, buffer));
            }
            if (accepted > 0) {
                buffer -= accepted;
                setChanged();
            }
        }
    }

    private void scan(Level level) {
        targets.clear();
        BlockPos origin = this.worldPosition;
        for (BlockPos pos : BlockPos.betweenClosed(origin.offset(-VoidValue.DISTRIBUTOR_RADIUS, -VoidValue.DISTRIBUTOR_RADIUS, -VoidValue.DISTRIBUTOR_RADIUS),
                origin.offset(VoidValue.DISTRIBUTOR_RADIUS, VoidValue.DISTRIBUTOR_RADIUS, VoidValue.DISTRIBUTOR_RADIUS))) {
            BlockEntity be = level.getBlockEntity(pos);
            if (be instanceof VoidGeneratorBlockEntity || be instanceof VoidFurnaceBlockEntity) {
                targets.add(pos.immutable());
            }
        }
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putLong("Buffer", buffer);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        buffer = tag.getLong("Buffer");
    }
}
