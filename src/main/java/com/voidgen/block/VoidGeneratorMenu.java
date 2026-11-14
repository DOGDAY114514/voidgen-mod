package com.voidgen.block;

import com.voidgen.VoidGen;
import com.voidgen.VoidStats;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.items.SlotItemHandler;

/**
 * Container menu of the Void Generator: 12 upgrade-card slots, 8 synced data slots and one
 * clickable button (id 0 toggles the AE2 energy output). The Binding Card is a player
 * accessory and is handled entirely outside this menu.
 */
public class VoidGeneratorMenu extends AbstractContainerMenu {
    public static final int CARD_SLOTS = VoidStats.CARD_SLOTS;
    public static final int MENU_SLOTS = CARD_SLOTS;
    private static final int PLAYER_SLOTS = 36;

    private final ContainerData data;
    private final VoidGeneratorBlockEntity generator;

    /** Client-side constructor used by the MenuType. */
    public VoidGeneratorMenu(int containerId, Inventory playerInventory) {
        this(containerId, playerInventory, new ItemStackHandler(MENU_SLOTS), new SimpleContainerData(VoidGeneratorBlockEntity.DATA_SLOTS), null);
    }

    /** Server-side constructor. */
    public VoidGeneratorMenu(int containerId, Inventory playerInventory, VoidGeneratorBlockEntity generator) {
        this(containerId, playerInventory, generator.cards(), generator.data(), generator);
    }

    private VoidGeneratorMenu(int containerId, Inventory playerInventory, IItemHandler cards, ContainerData data, VoidGeneratorBlockEntity generator) {
        super(VoidGen.VOIDGEN_MENU.get(), containerId);
        this.data = data;
        this.generator = generator;

        for (int i = 0; i < CARD_SLOTS; i++) {
            int x = 8 + (i % 4) * 18;
            int y = 100 + (i / 4) * 18;
            this.addSlot(new SlotItemHandler(cards, i, x, y) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return VoidStats.isSlotCard(stack);
                }
            });
        }
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(playerInventory, 9 + row * 9 + col, 8 + col * 18, 158 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(playerInventory, col, 8 + col * 18, 216));
        }
        this.addDataSlots(data);
    }

    public long energy() {
        return ((long) data.get(1) << 32) | (data.get(0) & 0xFFFFFFFFL);
    }

    public long rate() {
        return data.get(2) & 0xFFFFFFFFL;
    }

    public long capacity() {
        return ((long) data.get(4) << 32) | (data.get(3) & 0xFFFFFFFFL);
    }

    public int tier() {
        return data.get(5);
    }

    public long range() {
        int range = data.get(6);
        return range < 0 ? Long.MAX_VALUE : range;
    }

    public boolean aeOutput() {
        return (data.get(7) & 1) != 0;
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (generator == null) {
            return false;
        }
        if (id == 0) {
            generator.toggleAe();
            return true;
        }
        return false;
    }

    @Override
    public boolean stillValid(Player player) {
        if (generator == null) {
            return true;
        }
        return player.distanceToSqr(generator.getBlockPos().getX() + 0.5D, generator.getBlockPos().getY() + 0.5D, generator.getBlockPos().getZ() + 0.5D) <= 64.0D * 64.0D;
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack result = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (slot != null && slot.hasItem()) {
            ItemStack stack = slot.getItem();
            result = stack.copy();
            if (index < MENU_SLOTS) {
                if (!this.moveItemStackTo(stack, MENU_SLOTS, MENU_SLOTS + PLAYER_SLOTS, true)) {
                    return ItemStack.EMPTY;
                }
            } else if (VoidStats.isSlotCard(stack)) {
                if (!this.moveItemStackTo(stack, 0, CARD_SLOTS, false)) {
                    return ItemStack.EMPTY;
                }
            } else {
                return ItemStack.EMPTY;
            }
            if (stack.isEmpty()) {
                slot.set(ItemStack.EMPTY);
            } else {
                slot.setChanged();
            }
            if (stack.getCount() == result.getCount()) {
                return ItemStack.EMPTY;
            }
            slot.onTake(player, stack);
        }
        return result;
    }
}
