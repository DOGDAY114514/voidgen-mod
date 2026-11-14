package com.voidgen.block;

import com.voidgen.VoidGen;
import com.voidgen.item.VoidStorageItem;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.items.SlotItemHandler;

/** 铏氭棤鏀堕泦瑁呯疆 GUI锛?6 涓瓨鍌ㄥ櫒妲?+ 鍐呴儴缂撳啿鏉°€?*/
public class NothingnessCollectorMenu extends AbstractContainerMenu {
    public static final int STORAGE_SLOTS = 16;
    public static final int MENU_SLOTS = STORAGE_SLOTS + 36;

    private final ContainerData data;

    public NothingnessCollectorMenu(int containerId, Inventory inventory) {
        this(containerId, inventory, new ItemStackHandler(STORAGE_SLOTS), new SimpleContainerData(NothingnessCollectorBlockEntity.DATA_SLOTS));
    }

    public NothingnessCollectorMenu(int containerId, Inventory inventory, NothingnessCollectorBlockEntity collector) {
        this(containerId, inventory, collector.storages(), collector.data());
    }

    private NothingnessCollectorMenu(int containerId, Inventory inventory, ItemStackHandler storages, ContainerData data) {
        super(VoidGen.NOTHING_COLLECTOR_MENU.get(), containerId);
        this.data = data;
        for (int i = 0; i < STORAGE_SLOTS; i++) {
            int col = i % 4;
            int row = i / 4;
            this.addSlot(new SlotItemHandler(storages, i, 8 + col * 18, 76 + row * 18) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return stack.getItem() instanceof VoidStorageItem;
                }
            });
        }
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(inventory, col + row * 9 + 9, 8 + col * 18, 158 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(inventory, col, 8 + col * 18, 216));
        }
        this.addDataSlots(data);
    }

    public long buffer() {
        return (data.get(1) & 0xFFFFFFFFL) << 32 | (data.get(0) & 0xFFFFFFFFL);
    }

    public int rate() {
        return data.get(2);
    }

    public long capacity() {
        return (data.get(4) & 0xFFFFFFFFL) << 32 | (data.get(3) & 0xFFFFFFFFL);
    }

    public int tier() {
        return data.get(5);
    }

    public long total() {
        return (data.get(8) & 0xFFFFFFFFL) << 32 | (data.get(7) & 0xFFFFFFFFL);
    }

    public int storageCount() {
        return data.get(6);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack result = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot.hasItem()) {
            ItemStack stack = slot.getItem();
            result = stack.copy();
            if (index < STORAGE_SLOTS) {
                if (!this.moveItemStackTo(stack, STORAGE_SLOTS, MENU_SLOTS, true)) {
                    return ItemStack.EMPTY;
                }
            } else if (stack.getItem() instanceof VoidStorageItem) {
                if (!this.moveItemStackTo(stack, 0, STORAGE_SLOTS, false)) {
                    return ItemStack.EMPTY;
                }
            } else {
                return ItemStack.EMPTY;
            }
            if (stack.isEmpty()) {
                slot.setByPlayer(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
            slot.onTake(player, stack);
        }
        return result;
    }

    @Override
    public boolean stillValid(Player player) {
        return true;
    }
}

