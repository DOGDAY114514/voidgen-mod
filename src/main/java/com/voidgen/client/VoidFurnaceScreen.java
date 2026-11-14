package com.voidgen.client;

import com.voidgen.VoidStats;
import com.voidgen.block.VoidFurnaceMenu;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public class VoidFurnaceScreen extends AbstractContainerScreen<VoidFurnaceMenu> {
    private static final int BG = 0xFFE9E3D5;
    private static final int HEADER = 0xFFD6EDE8;
    private static final int PANEL = 0xFFF2ECDF;
    private static final int BORDER = 0xFF9A9282;
    private static final int SLOT_FRAME = 0xFFB5AC9A;
    private static final int SLOT_BG = 0xFFD8D1C0;
    private static final int TEXT = 0xFF3A3940;
    private static final int DIM = 0xFF6F6A5E;
    private static final int ACCENT = 0xFF1E8E85;

    private static final int BUTTON_X = 8;
    private static final int BUTTON_Y = 152;
    private static final int BUTTON_W = 80;
    private static final int BUTTON_H = 14;

    private static final int AE_X = 92;
    private static final int AE_Y = 152;
    private static final int AE_W = 76;
    private static final int AE_H = 14;

    public VoidFurnaceScreen(VoidFurnaceMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
        this.imageWidth = 176;
        this.imageHeight = 260;
        this.titleLabelX = 8;
        this.titleLabelY = 6;
        this.inventoryLabelX = 8;
        this.inventoryLabelY = 176;
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        this.renderTooltip(graphics, mouseX, mouseY);
    }

    @Override
    protected void renderBg(GuiGraphics graphics, float partialTick, int mouseX, int mouseY) {
        int x = this.leftPos;
        int y = this.topPos;
        graphics.fill(x, y, x + this.imageWidth, y + this.imageHeight, BG);
        graphics.fill(x, y, x + this.imageWidth, y + 14, HEADER);
        for (var slot : this.menu.slots) {
            graphics.fill(x + slot.x - 1, y + slot.y - 1, x + slot.x + 17, y + slot.y + 17, SLOT_FRAME);
            graphics.fill(x + slot.x, y + slot.y, x + slot.x + 16, y + slot.y + 16, SLOT_BG);
        }
        graphics.fill(x + BUTTON_X, y + BUTTON_Y, x + BUTTON_X + BUTTON_W, y + BUTTON_Y + BUTTON_H, PANEL);
        graphics.fill(x + BUTTON_X, y + BUTTON_Y, x + BUTTON_X + BUTTON_W, y + BUTTON_Y + 1, BORDER);
        graphics.fill(x + AE_X, y + AE_Y, x + AE_X + AE_W, y + AE_Y + AE_H, PANEL);
        graphics.fill(x + AE_X, y + AE_Y, x + AE_X + AE_W, y + AE_Y + 1, BORDER);
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        graphics.drawString(this.font, this.title, this.titleLabelX, this.titleLabelY, ACCENT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.cards", VoidFurnaceMenu.CARD_SLOTS), 8, 66, DIM, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.furnace_rate", VoidStats.fmt(this.menu.rate())), 8, 132, TEXT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.furnace_slot", VoidStats.fmt(this.menu.capacity()), this.menu.accelCards()), 8, 144, TEXT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.furnace_wireless",
                Component.translatable(this.menu.wireless()
                        ? "gui.voidgen.furnace_wireless_on"
                        : "gui.voidgen.furnace_wireless_off")), 12, 155, this.menu.wireless() ? ACCENT : DIM, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.furnace_ae",
                Component.translatable(this.menu.aeReturn()
                        ? "gui.voidgen.furnace_ae_on"
                        : "gui.voidgen.furnace_ae_off")), 96, 155, this.menu.aeReturn() ? ACCENT : DIM, false);
        graphics.drawString(this.font, this.playerInventoryTitle, this.inventoryLabelX, this.inventoryLabelY, DIM, false);
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (this.isHovering(BUTTON_X, BUTTON_Y, BUTTON_W, BUTTON_H, mouseX, mouseY)) {
            if (this.minecraft != null && this.minecraft.gameMode != null) {
                this.minecraft.gameMode.handleInventoryButtonClick(this.menu.containerId, 0);
            }
            return true;
        }
        if (this.isHovering(AE_X, AE_Y, AE_W, AE_H, mouseX, mouseY)) {
            if (this.minecraft != null && this.minecraft.gameMode != null) {
                this.minecraft.gameMode.handleInventoryButtonClick(this.menu.containerId, 1);
            }
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }
}

