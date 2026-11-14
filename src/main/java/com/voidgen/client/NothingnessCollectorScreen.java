package com.voidgen.client;

import com.voidgen.VoidValue;
import com.voidgen.block.NothingnessCollectorMenu;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;

/** AE 风格：虚无收集装置面板。 */
public class NothingnessCollectorScreen extends AbstractContainerScreen<NothingnessCollectorMenu> {
    private static final int BG = 0xFFE9E3D5;
    private static final int BORDER = 0xFF9A9282;
    private static final int PANEL = 0xFFF2ECDF;
    private static final int SLOT_BG = 0xFFD8D1C0;
    private static final int TEXT = 0xFF3A3940;
    private static final int DIM = 0xFF6F6A5E;
    private static final int ACCENT = 0xFF1E8E85;
    private static final int BAR_FROM = 0xFF2FB3A7;
    private static final int BAR_TO = 0xFF7C5BD0;

    public NothingnessCollectorScreen(NothingnessCollectorMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
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
        int x = this.leftPos;
        int y = this.topPos;
        graphics.fill(x, y, x + this.imageWidth, y + this.imageHeight, BG);
        graphics.fill(x, y, x + this.imageWidth, y + 2, BORDER);
        graphics.fill(x, y + this.imageHeight - 2, x + this.imageWidth, y + this.imageHeight, BORDER);
        graphics.fill(x, y, x + 2, y + this.imageHeight, BORDER);
        graphics.fill(x + this.imageWidth - 2, y, x + this.imageWidth, y + this.imageHeight, BORDER);

        // buffer bar
        graphics.fill(x + 8, y + 16, x + 168, y + 26, 0xFFC7BFAD);
        long cap = Math.max(1L, this.menu.capacity());
        double fraction = Math.min(1.0D, (double) this.menu.buffer() / (double) cap);
        int fillWidth = (int) Math.round(160 * fraction);
        if (fillWidth > 0) {
            graphics.fillGradient(x + 8, y + 16, x + 8 + fillWidth, y + 26, BAR_FROM, BAR_TO);
        }

        for (Slot slot : this.menu.slots) {
            if (slot.x < 100 && slot.y < 140) {
                graphics.fill(x + slot.x - 1, y + slot.y - 1, x + slot.x + 17, y + slot.y + 17, PANEL);
                graphics.fill(x + slot.x, y + slot.y, x + slot.x + 16, y + slot.y + 16, SLOT_BG);
            }
        }
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        graphics.drawString(this.font, this.title, this.titleLabelX, this.titleLabelY, ACCENT, false);
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.collector_rate", VoidValue.format(this.menu.rate())),
                8, 30, TEXT, false);
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.collector_buffer", VoidValue.format(this.menu.buffer()),
                        this.menu.capacity() == Long.MAX_VALUE ? "∞" : VoidValue.format(this.menu.capacity())),
                8, 42, TEXT, false);
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.collector_tier_slots", this.menu.tier(), this.menu.storageCount()),
                8, 66, DIM, false);
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.collector_total", VoidValue.format(this.menu.total())),
                8, 54, TEXT, false);
        graphics.drawString(this.font, this.playerInventoryTitle, this.inventoryLabelX, this.inventoryLabelY, DIM, false);
    }
}
