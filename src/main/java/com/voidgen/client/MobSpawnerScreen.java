package com.voidgen.client;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import com.voidgen.VoidValue;
import com.voidgen.item.MobSpawnerItem;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SpawnEggItem;
import net.neoforged.neoforge.network.PacketDistributor;

/** 虚无生物生成器 GUI：7x5 生成蛋缩略图分页选择，右上角 < > 翻页，支持滚轮。 */
public class MobSpawnerScreen extends Screen {
    private static final int PAGE_SIZE = 35;
    private static final int COLS = 7;
    private static final int CELL = 20;

    // light palette, shared with the other voidgen screens
    private static final int BG = 0xFFE9E3D5;
    private static final int BORDER = 0xFF9A9282;
    private static final int PANEL = 0xFFF2ECDF;
    private static final int SLOT_FRAME = 0xFFB5AC9A;
    private static final int SLOT_BG = 0xFFD8D1C0;
    private static final int TEXT = 0xFF3A3940;
    private static final int DIM = 0xFF6F6A5E;
    private static final int ACCENT = 0xFF1E8E85;

    private static final int PREV_X = 118;
    private static final int NEXT_X = 136;
    private static final int NAV_Y = 6;
    private static final int NAV_W = 14;
    private static final int NAV_H = 12;

    private static List<EntityType<?>> MOBS;

    private int page;
    private int leftPos;
    private int topPos;

    public MobSpawnerScreen() {
        super(Component.translatable("item.voidgen.mob_spawner"));
    }

    @Override
    protected void init() {
        super.init();
        this.leftPos = (this.width - 176) / 2;
        this.topPos = (this.height - 190) / 2;
    }

    private static List<EntityType<?>> mobs() {
        if (MOBS == null) {
            List<EntityType<?>> list = new ArrayList<>();
            for (EntityType<?> type : BuiltInRegistries.ENTITY_TYPE) {
                if (type == EntityType.PLAYER || !type.canSummon()) {
                    continue;
                }
                if (SpawnEggItem.byId(type) != null) {
                    list.add(type);
                }
            }
            list.sort(Comparator.comparing(type -> type.getDescriptionId()));
            MOBS = list;
        }
        return MOBS;
    }

    private int pageCount() {
        return Math.max(1, (mobs().size() + PAGE_SIZE - 1) / PAGE_SIZE);
    }

    private void turnPage(int delta) {
        this.page = Math.floorMod(this.page + delta, pageCount());
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        this.renderBackground(graphics, mouseX, mouseY, partialTick);
        int x = this.leftPos;
        int y = this.topPos;

        graphics.fill(x, y, x + 176, y + 190, BG);
        graphics.fill(x, y, x + 176, y + 2, ACCENT);
        graphics.fill(x, y, x + 2, y + 190, BORDER);
        graphics.fill(x + 174, y, x + 176, y + 190, BORDER);
        graphics.fill(x, y + 188, x + 176, y + 190, BORDER);

        graphics.drawString(this.font, this.title, x + 8, y + 8, ACCENT, false);
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.spawner_page", this.page + 1, pageCount()),
                x + 88, y + 9, DIM, false);

        drawNav(graphics, x + PREV_X, y + NAV_Y, false, mouseX, mouseY);
        drawNav(graphics, x + NEXT_X, y + NAV_Y, true, mouseX, mouseY);

        ItemStack held = this.heldStack();
        String selected = held == null ? "" : MobSpawnerItem.selectedId(held);

        List<EntityType<?>> list = mobs();
        int start = this.page * PAGE_SIZE;
        int hovered = -1;
        for (int i = 0; i < PAGE_SIZE; i++) {
            int index = start + i;
            if (index >= list.size()) {
                break;
            }
            int col = i % COLS;
            int row = i / COLS;
            int cx = x + 8 + col * CELL;
            int cy = y + 28 + row * CELL;
            graphics.fill(cx, cy, cx + 18, cy + 18, SLOT_FRAME);
            graphics.fill(cx + 1, cy + 1, cx + 17, cy + 17, SLOT_BG);
            if (selected.equals(VoidValue.idOf(list.get(index)))) {
                graphics.fill(cx + 1, cy + 1, cx + 17, cy + 3, ACCENT);
                graphics.fill(cx + 1, cy + 15, cx + 17, cy + 17, ACCENT);
            }
            ItemStack icon = new ItemStack(SpawnEggItem.byId(list.get(index)));
            graphics.renderItem(icon, cx + 1, cy + 1);
            if (mouseX >= cx && mouseX < cx + 18 && mouseY >= cy && mouseY < cy + 18) {
                hovered = index;
                graphics.fill(cx + 1, cy + 1, cx + 17, cy + 17, 0x40FFFFFF);
            }
        }

        if (hovered >= 0) {
            EntityType<?> type = list.get(hovered);
            Component tip = Component.translatable(type.getDescriptionId())
                    .append("\n")
                    .append(Component.translatable("gui.voidgen.spawner_cost", VoidValue.format(VoidValue.mobCost(type))))
                    .append("\n")
                    .append(Component.translatable("gui.voidgen.spawner_click"));
            graphics.renderTooltip(this.font, tip, mouseX, mouseY);
        }

        // player inventory hint text at the bottom
        graphics.drawString(this.font,
                Component.translatable("gui.voidgen.spawner_hint"),
                x + 8, y + 172, DIM, false);
    }

    private void drawNav(GuiGraphics graphics, int x, int y, boolean next, int mouseX, int mouseY) {
        boolean hover = mouseX >= x && mouseX < x + NAV_W && mouseY >= y && mouseY < y + NAV_H;
        graphics.fill(x, y, x + NAV_W, y + NAV_H, PANEL);
        int border = hover ? ACCENT : BORDER;
        graphics.fill(x, y, x + NAV_W, y + 1, border);
        graphics.fill(x, y + NAV_H - 1, x + NAV_W, y + NAV_H, border);
        graphics.fill(x, y, x + 1, y + NAV_H, border);
        graphics.fill(x + NAV_W - 1, y, x + NAV_W, y + NAV_H, border);
        String arrow = next ? ">" : "<";
        int tw = this.font.width(arrow);
        int color = hover ? ACCENT : TEXT;
        graphics.drawString(this.font, arrow, x + (NAV_W - tw) / 2, y + 2, color, false);
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button != 0) {
            return super.mouseClicked(mouseX, mouseY, button);
        }
        int x = this.leftPos;
        int y = this.topPos;

        if (within(mouseX, mouseY, x + PREV_X, y + NAV_Y, NAV_W, NAV_H)) {
            turnPage(-1);
            return true;
        }
        if (within(mouseX, mouseY, x + NEXT_X, y + NAV_Y, NAV_W, NAV_H)) {
            turnPage(1);
            return true;
        }

        if (mouseX >= x + 8 && mouseX < x + 8 + COLS * CELL && mouseY >= y + 28 && mouseY < y + 28 + 5 * CELL) {
            int col = (int) ((mouseX - x - 8) / CELL);
            int row = (int) ((mouseY - y - 28) / CELL);
            int index = this.page * PAGE_SIZE + row * COLS + col;
            List<EntityType<?>> list = mobs();
            if (index >= 0 && index < list.size()) {
                select(list.get(index));
                return true;
            }
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        if (scrollY != 0.0D) {
            turnPage(scrollY > 0.0D ? -1 : 1);
            return true;
        }
        return super.mouseScrolled(mouseX, mouseY, scrollX, scrollY);
    }

    private static boolean within(double mx, double my, int x, int y, int w, int h) {
        return mx >= x && mx < x + w && my >= y && my < y + h;
    }

    private void select(EntityType<?> type) {
        String id = VoidValue.idOf(type);
        LocalPlayer player = Minecraft.getInstance().player;
        ItemStack held = this.heldStack();
        if (held != null) {
            MobSpawnerItem.setSelectedId(held, id);
        }
        PacketDistributor.sendToServer(new com.voidgen.VoidNet.MobSelectPayload(id));
        if (player != null) {
            player.displayClientMessage(Component.translatable("status.voidgen.spawner_selected",
                    Component.translatable(type.getDescriptionId())), true);
        }
        this.minecraft.setScreen(null);
    }

    private ItemStack heldStack() {
        LocalPlayer player = Minecraft.getInstance().player;
        if (player == null) {
            return null;
        }
        ItemStack stack = player.getMainHandItem();
        return stack.getItem() instanceof MobSpawnerItem ? stack : null;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
