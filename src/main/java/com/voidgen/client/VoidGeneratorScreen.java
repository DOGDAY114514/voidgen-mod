package com.voidgen.client;

import com.voidgen.VoidStats;
import com.voidgen.block.VoidGeneratorMenu;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;

/**
 * AE2-styled internal panel: dark tech frame, gradient energy bar, 12 upgrade-card slots and
 * one toggle button (container id 0 = AE2 energy output). The Binding Card is a player
 * accessory now, so it is not shown here anymore.
 */
public class VoidGeneratorScreen extends AbstractContainerScreen<VoidGeneratorMenu> {
    private static final int BG = 0xFFE9E3D5;
    private static final int PANEL = 0xFFF2ECDF;
    private static final int PANEL_BORDER = 0xFF9A9282;
    private static final int SLOT_BG = 0xFFD8D1C0;
    private static final int TEXT = 0xFF3A3940;
    private static final int DIM = 0xFF6F6A5E;
    private static final int ACCENT = 0xFF1E8E85;
    private static final int BAR_BG = 0xFFC7BFAD;
    private static final int BAR_FROM = 0xFF2FB3A7;
    private static final int BAR_TO = 0xFF7C5BD0;

    private static final int AE_X = 8;
    private static final int AE_Y = 74;
    private static final int AE_W = 96;
    private static final int AE_H = 14;

    public VoidGeneratorScreen(VoidGeneratorMenu menu, Inventory playerInventory, Component title) {
        super(menu, playerInventory, title);
        this.imageWidth = 176;
        this.imageHeight = 240;
        this.titleLabelX = 8;
        this.titleLabelY = 6;
        this.inventoryLabelX = 8;
        this.inventoryLabelY = 148;
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        this.renderTooltip(graphics, mouseX, mouseY);
    }

    @Override
    protected void renderBg(GuiGraphics graphics, float partialTick, int mouseX, int mouseY) {
        int left = this.leftPos;
        int top = this.topPos;

        graphics.fill(left, top, left + this.imageWidth, top + this.imageHeight, BG);
        graphics.fill(left, top, left + this.imageWidth, top + 2, ACCENT);
        graphics.fill(left, top + this.imageHeight - 2, left + this.imageWidth, top + this.imageHeight, PANEL_BORDER);
        graphics.fill(left, top, left + 2, top + this.imageHeight, PANEL_BORDER);
        graphics.fill(left + this.imageWidth - 2, top, left + this.imageWidth, top + this.imageHeight, PANEL_BORDER);

        // energy bar
        graphics.fill(left + 8, top + 18, left + 168, top + 28, BAR_BG);
        long capacity = this.menu.capacity();
        long energy = this.menu.energy();
        double fraction = capacity <= 0 ? 0.0D : Math.min(1.0D, (double) energy / (double) capacity);
        int barWidth = (int) Math.round(158.0D * fraction);
        if (barWidth > 0) {
            graphics.fillGradient(left + 9, top + 19, left + 9 + barWidth, top + 27, BAR_FROM, BAR_TO);
        }
        graphics.fill(left + 8, top + 18, left + 168, top + 19, PANEL_BORDER);
        graphics.fill(left + 8, top + 27, left + 168, top + 28, PANEL_BORDER);

        // AE toggle button
        drawButton(graphics, left + AE_X, top + AE_Y, AE_W, AE_H, isHovering(AE_X, AE_Y, AE_W, AE_H, mouseX, mouseY));

        // slot frames
        for (Slot slot : this.menu.slots) {
            int x = left + slot.x - 1;
            int y = top + slot.y - 1;
            graphics.fill(x, y, x + 18, y + 18, PANEL_BORDER);
            graphics.fill(x + 1, y + 1, x + 17, y + 17, SLOT_BG);
        }
    }

    private static void drawButton(GuiGraphics graphics, int x, int y, int w, int h, boolean hovered) {
        graphics.fill(x, y, x + w, y + h, PANEL);
        int border = hovered ? ACCENT : PANEL_BORDER;
        graphics.fill(x, y, x + w, y + 1, border);
        graphics.fill(x, y + h - 1, x + w, y + h, border);
        graphics.fill(x, y, x + 1, y + h, border);
        graphics.fill(x + w - 1, y, x + w, y + h, border);
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        graphics.drawString(this.font, this.title, this.titleLabelX, this.titleLabelY, ACCENT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.rate", VoidStats.fmtCompact(this.menu.rate())), 8, 30, TEXT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.energy", VoidStats.fmtCompact(this.menu.energy()), VoidStats.fmtCompact(this.menu.capacity())), 8, 42, TEXT, false);
        Component range = this.menu.range() == Long.MAX_VALUE
                ? Component.translatable("gui.voidgen.infinite")
                : Component.translatable("gui.voidgen.finite", VoidStats.fmtCompact(this.menu.range()));
        graphics.drawString(this.font, Component.translatable("gui.voidgen.range", range), 8, 54, TEXT, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.tier", this.menu.tier(), VoidStats.MAX_TIER), 8, 64, TEXT, false);

        boolean ae = this.menu.aeOutput();
        graphics.drawString(this.font, Component.translatable("gui.voidgen.ae",
                Component.translatable(ae ? "gui.voidgen.ae_on" : "gui.voidgen.ae_off")), 12, 77, ae ? ACCENT : DIM, false);
        graphics.drawString(this.font, Component.translatable("gui.voidgen.cards", VoidStats.CARD_SLOTS), 8, 90, DIM, false);

        graphics.drawString(this.font, this.playerInventoryTitle, this.inventoryLabelX, this.inventoryLabelY, DIM, false);
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == 0 && this.isHovering(AE_X, AE_Y, AE_W, AE_H, mouseX, mouseY)) {
            if (this.minecraft != null && this.minecraft.gameMode != null) {
                this.minecraft.gameMode.handleInventoryButtonClick(this.menu.containerId, 0);
            }
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }
}

