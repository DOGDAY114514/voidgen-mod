package com.voidgen.client;

import java.util.ArrayList;
import java.util.List;

import com.voidgen.VoidGen;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.util.FormattedCharSequence;

/**
 * In-game quick guide, opened with the G key (see {@link VoidGenClient}).
 * Scrollable: mouse wheel or arrow keys. G / Esc closes.
 */
public class VoidGuideScreen extends Screen {
    private static final int PANEL_W = 440;
    private static final int PAD = 10;
    private static final int LINE = 10;
    private static final int ACCENT = 0xFF4FD1C5;
    private static final int TEXT = 0xFFD6E0E0;
    private static final int HEAD = 0xFFEFF6F6;
    private static final int DIM = 0xFF8B9898;
    private static final int BG = 0xF0101216;
    private static final int BORDER = 0xFF2E4D4D;
    private static final int KEY_G = 71;
    private static final int KEY_UP = 265;
    private static final int KEY_DOWN = 264;
    private static final int KEY_PAGE_UP = 266;
    private static final int KEY_PAGE_DOWN = 267;

    private record Line(boolean header, String text) {
    }

    private static final List<Line> LINES = new ArrayList<>();

    private static void header(String text) {
        LINES.add(new Line(true, text));
    }

    private static void body(String text) {
        LINES.add(new Line(false, text));
    }

    static {
        header("虚无发电机");
        body("放下即凭空发电：基础 1,000 FE/t，每阶套娃 ×4（最高 V 阶 1,024,000 FE/t）。");
        body("自动向 6 个相邻方块和无线范围内「玩家放置的机器」供电；基础范围 16 格，每张范围卡 ×4，12 张范围卡 = 无限。");
        body("Shift + 右击打开面板：12 张升级卡槽 + AE 输出开关；手持套娃/升级卡 Shift + 右击可直接安装。");
        body("空手右击查看阶数/发电/储能/范围；绑定卡可对单台机器「解除」或「强制」供电。");

        header("虚无值系统");
        body("把圆石丢进虚空（掉出世界最低高度）：1 圆石 = 1 虚无值，按顺序存入背包/身上的虚无存储器。");
        body("存储器容量：铁 1,000 / 金 10,000 / 钻石 100,000 / 绿宝石 1,000,000 / 下界之星无限；存满会变成「充盈」版本，用来合成收集装置。");
        body("虚无收集装置 I~V：16 个存储器槽自动充能；旁边放虚无发散器，就会把虚无值输送给附近的发电机/熔炉。");
        body("虚无生物生成器：Shift + 右击打开生物列表并选择，右击生成生物；Shift + 右击虚无发散器可绑定扣费来源。");

        header("虚无熔炉");
        body("直接右击打开面板；9 输入 + 9 输出槽，每槽 8192 起（套娃/容量卡再翻倍）。");
        body("不需要燃料和 FE；加速卡/超频卡提升速度（7 张到 8192 件/刻封顶），容量卡扩大单槽上限。");
        body("无线输出到范围内的容器；AE 回传可以贴 ME 接口，也可以用线缆把熔炉直接连进 AE 网络。");

        header("AE2 联动（需装 AE2 19.x）");
        body("虚无磁盘 1K~256M：按 AE2 存储元件的方式实现，放进 ME 驱动器 / ME 箱子即可当存储元件用。");
        body("ME 虚无供应器：SUPPLY 模式消耗虚无值物品给附近机器供能；IMPORT 模式从旁边收集装置抽虚无值并变成物品，供 ME 输入总线吸进网络。");
        body("虚空合成器：接入 ME 网络，只接受产物是处理器的样板；CPU 下单后瞬间完成，材料照常从网络扣除，产物直接回 ME。");

        header("按键");
        body("G：打开 / 关闭本说明；Esc 关闭。");
        body("Shift + 滚轮（世界中）：绑定卡的自动连接开关。");
        body("发电机 Shift + 右击 / 熔炉右击：打开对应 GUI。");
    }

    private int scroll;

    public VoidGuideScreen() {
        super(Component.translatable("gui.voidgen.guide.title"));
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        this.renderBackground(graphics, mouseX, mouseY, partialTick);

        int left = (this.width - PANEL_W) / 2;
        int top = 24;
        int bottom = this.height - 24;
        graphics.fill(left, top, left + PANEL_W, bottom, BG);
        graphics.fill(left, top, left + PANEL_W, top + 2, BORDER);
        graphics.fill(left, bottom - 2, left + PANEL_W, bottom, BORDER);
        graphics.fill(left, top, left + 2, bottom, BORDER);
        graphics.fill(left + PANEL_W - 2, top, left + PANEL_W, bottom, BORDER);

        int titleWidth = this.font.width(this.title);
        graphics.drawString(this.font, this.title, left + (PANEL_W - titleWidth) / 2, top + 10, HEAD, false);

        int x = left + PAD;
        int contentW = PANEL_W - PAD * 2;
        int contentTop = top + 30;
        int contentBottom = bottom - 26;

        graphics.enableScissor(x - 2, contentTop - 2, x + contentW + 2, contentBottom + 2);
        int y = contentTop - this.scroll;
        for (Line line : LINES) {
            if (line.header()) {
                y += 6;
                graphics.drawString(this.font, Component.literal(line.text()), x, y, ACCENT, false);
                y += LINE + 2;
            } else {
                List<FormattedCharSequence> wrapped = this.font.split(Component.literal(line.text()), contentW - 6);
                for (FormattedCharSequence sequence : wrapped) {
                    if (y >= contentTop - LINE && y <= contentBottom) {
                        graphics.drawString(this.font, sequence, x + 4, y, TEXT, false);
                    }
                    y += LINE;
                }
                y += 2;
            }
        }
        graphics.disableScissor();

        int totalHeight = y - (contentTop - this.scroll);
        int maxScroll = Math.max(0, totalHeight - (contentBottom - contentTop));
        if (this.scroll > maxScroll) {
            this.scroll = maxScroll;
        }

        Component hint = Component.literal("滚轮 / ↑ ↓ 滚动 · G 或 Esc 关闭");
        int hintWidth = this.font.width(hint);
        graphics.drawString(this.font, hint, left + (PANEL_W - hintWidth) / 2, bottom - 16, DIM, false);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        this.scroll = Math.max(0, this.scroll - (int) Math.round(scrollY * 24.0D));
        return true;
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == KEY_G) {
            this.onClose();
            return true;
        }
        if (keyCode == KEY_UP) {
            this.scroll = Math.max(0, this.scroll - LINE * 2);
            return true;
        }
        if (keyCode == KEY_DOWN) {
            this.scroll += LINE * 2;
            return true;
        }
        if (keyCode == KEY_PAGE_UP) {
            this.scroll = Math.max(0, this.scroll - 120);
            return true;
        }
        if (keyCode == KEY_PAGE_DOWN) {
            this.scroll += 120;
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
