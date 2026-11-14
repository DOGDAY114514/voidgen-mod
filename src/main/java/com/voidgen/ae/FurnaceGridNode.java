package com.voidgen.ae;

import com.voidgen.GridHost;
import com.voidgen.VoidGen;
import com.voidgen.block.VoidFurnaceBlockEntity;

import appeng.api.networking.GridHelper;
import appeng.api.networking.IGrid;
import appeng.api.networking.IGridNode;
import appeng.api.networking.IGridNodeListener;
import appeng.api.networking.IInWorldGridNodeHost;
import appeng.api.networking.IManagedGridNode;
import appeng.api.networking.energy.IEnergySource;
import appeng.api.networking.security.IActionSource;
import appeng.api.stacks.AEItemKey;
import appeng.api.storage.MEStorage;
import appeng.api.storage.StorageHelper;
import appeng.api.util.AECableType;

import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.items.IItemHandler;

/**
 * In-world AE2 grid node for the void furnace. Cable connection = the furnace
 * becomes part of that ME network; AE return pushes outputs straight into the
 * network storage instead of going through a neighbouring interface.
 */
public final class FurnaceGridNode implements IInWorldGridNodeHost, IGridNodeListener<FurnaceGridNode>, GridHost {
    private final VoidFurnaceBlockEntity furnace;
    private final IManagedGridNode node;
    private boolean destroyed;

    public FurnaceGridNode(VoidFurnaceBlockEntity furnace) {
        this.furnace = furnace;
        this.node = GridHelper.createManagedNode(this, this);
        this.node.setVisualRepresentation(VoidGen.VOID_FURNACE_ITEM.get());
        this.node.setInWorldNode(true);
        this.node.setTagName("voidgen_furnace_node");

        CompoundTag pending = furnace.pendingGridTag();
        if (pending != null) {
            this.node.loadFromNBT(pending);
        }

        Level level = furnace.getLevel();
        if (level != null) {
            this.node.create(level, furnace.getBlockPos());
        }
    }

    @Override
    public IGridNode getGridNode(Direction side) {
        return node.getNode();
    }

    @Override
    public AECableType getCableConnectionType(Direction side) {
        return AECableType.SMART;
    }

    @Override
    public void onSaveChanges(FurnaceGridNode host, IGridNode node) {
        furnace.setChanged();
    }

    @Override
    public boolean isOnline() {
        return node.isOnline();
    }

    @Override
    public long pushItems(IItemHandler outputs, int budget) {
        IGrid grid = node.getGrid();
        if (grid == null || budget <= 0) {
            return 0;
        }
        MEStorage storage = grid.getStorageService().getInventory();
        IEnergySource energy = grid.getEnergyService();
        IActionSource source = IActionSource.empty();

        long pushed = 0;
        for (int slot = 0; slot < outputs.getSlots() && pushed < budget; slot++) {
            ItemStack stack = outputs.getStackInSlot(slot);
            if (stack.isEmpty()) {
                continue;
            }
            AEItemKey key = AEItemKey.of(stack);
            if (key == null) {
                continue;
            }
            long amount = Math.min(stack.getCount(), budget - pushed);
            long moved = StorageHelper.poweredInsert(energy, storage, key, amount, source);
            if (moved > 0) {
                outputs.extractItem(slot, (int) Math.min(Integer.MAX_VALUE, moved), false);
                pushed += moved;
            }
        }
        return pushed;
    }

    @Override
    public void save(CompoundTag tag) {
        if (!destroyed) {
            node.saveToNBT(tag);
        }
    }

    @Override
    public void load(CompoundTag tag) {
        if (!destroyed) {
            node.loadFromNBT(tag);
        }
    }

    @Override
    public void destroy() {
        if (!destroyed) {
            destroyed = true;
            node.destroy();
        }
    }
}
