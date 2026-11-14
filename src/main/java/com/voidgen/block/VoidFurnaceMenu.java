package com.voidgen.block;

import com.voidgen.VoidGen;
import com.voidgen.VoidStats;

import net.minecraft.network.chat.Component;
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

public class VoidFurnaceMenu extends AbstractContainerMenu {
    public static final int INPUT_SLOTS = VoidStats.FURNACE_SLOTS;
    public static final int OUTPUT_SLOTS = VoidStats.FURNACE_SLOTS;
    public static final int CARD_SLOTS = VoidStats.FURNACE_CARD_SLOTS;
    public static final int MENU_SLOTS = INPUT_SLOTS + OUTPUT_SLOTS + CARD_SLOTS;
    public static final int PLAYER_SLOTS = 36;

    private final ContainerData data;
    private final VoidFurnaceBlockEntity furnace;

    public VoidFurnaceMenu(int containerId, Inventory inventory) {
        this(containerId, inventory,
                new ItemStackHandler(INPUT_SLOTS),
                new ItemStackHandler(OUTPUT_SLOTS),
                new ItemStackHandler(CARD_SLOTS),
                new SimpleContainerData(VoidFurnaceBlockEntity.DATA_SLOTS),
                null);
    }

    public VoidFurnaceMenu(int containerId, Inventory inventory, VoidFurnaceBlockEntity furnace) {
        this(containerId, inventory, furnace.inputs(), furnace.outputs(), furnace.cards(),
                furnace.containerData(), furnace);
    }

    private VoidFurnaceMenu(int containerId, Inventory inventory,
                            IItemHandler inputs, IItemHandler outputs, IItemHandler cards,
                            ContainerData data, VoidFurnaceBlockEntity furnace) {
        super(VoidGen.VOID_FURNACE_MENU.get(), containerId);
        this.data = data;
        this.furnace = furnace;

        // 3x3 input grid
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                this.addSlot(new SlotItemHandler(inputs, row * 3 + col, 8 + col * 18, 20 + row * 18));
            }
        }
        // 3x3 output grid
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                this.addSlot(new SlotItemHandler(outputs, row * 3 + col, 116 + col * 18, 20 + row * 18) {
                    @Override
                    public boolean mayPlace(ItemStack stack) {
                        return false;
                    }
                });
            }
        }
        // 4x3 card grid
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 4; col++) {
                this.addSlot(new SlotItemHandler(cards, row * 4 + col, 8 + col * 18, 74 + row * 18) {
                    @Override
                    public boolean mayPlace(ItemStack stack) {
                        return VoidStats.isFurnaceCard(stack);
                    }
                });
            }
        }
        // player inventory
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                this.addSlot(new Slot(inventory, col + row * 9 + 9, 8 + col * 18, 184 + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            this.addSlot(new Slot(inventory, col, 8 + col * 18, 242));
        }
        this.addDataSlots(data);
    }

    public int rate() {
        return data.get(0);
    }

    public int tier() {
        return data.get(1);
    }

    public int accelCards() {
        return data.get(2);
    }

    public int capacity() {
        return data.get(3);
    }

    public boolean wireless() {
        return (data.get(4) & 1) != 0;
    }

    public boolean aeReturn() {
        return (data.get(4) & 2) != 0;
    }

    public int rangeInt() {
        return data.get(5);
    }

    @Override
    public boolean stillValid(Player player) {
        if (furnace == null) {
            return true;
        }
        double x = furnace.getBlockPos().getX() + 0.5D;
        double y = furnace.getBlockPos().getY() + 0.5D;
        double z = furnace.getBlockPos().getZ() + 0.5D;
        return player.distanceToSqr(x, y, z) <= 4096.0D;
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (id == 0 && furnace != null) {
            furnace.toggleWireless();
            player.displayClientMessage(Component.translatable(
                    furnace.wirelessEnabled()
                            ? "status.voidgen.furnace_wireless_on"
                            : "status.voidgen.furnace_wireless_off"), true);
            return true;
        }
        if (id == 1 && furnace != null) {
            furnace.toggleAeReturn();
            player.displayClientMessage(Component.translatable(
                    furnace.aeReturn()
                            ? "status.voidgen.furnace_ae_on"
                            : "status.voidgen.furnace_ae_off"), true);
            return true;
        }
        return false;
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        ItemStack copy = ItemStack.EMPTY;
        Slot slot = this.slots.get(index);
        if (!slot.hasItem()) {
            return copy;
        }
        ItemStack stack = slot.getItem();
        copy = stack.copy();
        if (index < MENU_SLOTS) {
            if (!this.moveItemStackTo(stack, MENU_SLOTS, MENU_SLOTS + PLAYER_SLOTS, true)) {
                return ItemStack.EMPTY;
            }
        } else {
            boolean moved;
            if (VoidStats.isFurnaceCard(stack)) {
                moved = this.moveItemStackTo(stack, INPUT_SLOTS + OUTPUT_SLOTS, MENU_SLOTS, false);
            } else {
                moved = this.moveItemStackTo(stack, 0, INPUT_SLOTS, false);
            }
            if (!moved) {
                return ItemStack.EMPTY;
            }
        }
        if (stack.isEmpty()) {
            slot.set(ItemStack.EMPTY);
        } else {
            slot.setChanged();
        }
        return copy;
    }
}
