package com.voidgen.client;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import com.voidgen.VoidGen;
import com.voidgen.VoidNet;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.ICancellableEvent;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.InputEvent;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/**
 * Client-only wiring:
 * <ul>
 *     <li>registers the AE-style Void Generator screen</li>
 *     <li>draws the Binding Card accessory slot on the player inventory</li>
 *     <li>handles clicks on that slot (equip / unequip) and Shift+scroll (auto-connect on / off)</li>
 * </ul>
 * The server owns the real state; this class only mirrors the last sync payload and swaps
 * the auto flag optimistically until the next {@link VoidNet.SyncPayload} arrives.
 */
@EventBusSubscriber(modid = VoidGen.MODID, value = Dist.CLIENT)
public final class VoidGenClient {
    private static final int OVERLAY_X = 154;
    private static final int OVERLAY_Y = 48;
    private static final int SLOT_SIZE = 18;
    private static final long SCROLL_DEBOUNCE_MS = 300L;
    private static final int BORDER = 0xFF3A3F4A;
    private static final int ACCENT = 0xFF4FD1C5;
    private static final int SLOT_BG = 0xFF0E0E12;
    private static final int TEXT = 0xFFB8C4C4;
    private static final int DIM = 0xFF7A8B8B;

    private static boolean hasCard;
    private static boolean auto;
    private static int boundCount;
    private static long lastScrollToggle;

    private VoidGenClient() {
    }

    @SubscribeEvent
    public static void onRegisterScreens(RegisterMenuScreensEvent event) {
        event.register(VoidGen.VOIDGEN_MENU.get(), VoidGeneratorScreen::new);
        event.register(VoidGen.VOID_FURNACE_MENU.get(), VoidFurnaceScreen::new);
        event.register(VoidGen.NOTHING_COLLECTOR_MENU.get(), NothingnessCollectorScreen::new);
    }

    /** Applied from the S2C sync payload. */
    public static void applySync(VoidNet.SyncPayload payload) {
        hasCard = payload.hasCard();
        auto = payload.auto();
        boundCount = payload.bound();
    }

    @SubscribeEvent
    public static void onScreenRender(ScreenEvent.Render.Post event) {
        if (!(event.getScreen() instanceof InventoryScreen screen)) {
            return;
        }
        int x = (screen.width - 176) / 2 + OVERLAY_X;
        int y = (screen.height - 166) / 2 + OVERLAY_Y;
        GuiGraphics graphics = event.getGuiGraphics();
        drawSlot(graphics, x, y);
        Minecraft minecraft = Minecraft.getInstance();
        if (hasCard) {
            graphics.renderItem(new ItemStack(VoidGen.BINDING_CARD.get()), x + 1, y + 1);
            if (auto) {
                graphics.fill(x + SLOT_SIZE - 5, y + 2, x + SLOT_SIZE - 2, y + 5, ACCENT);
            }
            graphics.drawString(minecraft.font, "×" + boundCount, x + 2, y + SLOT_SIZE - 9, TEXT, false);
        } else {
            graphics.drawString(minecraft.font, "+", x + 7, y + 5, DIM, false);
        }
        if (isHovering(event.getMouseX(), event.getMouseY(), x, y)) {
            graphics.renderTooltip(minecraft.font, tooltip(), Optional.empty(), event.getMouseX(), event.getMouseY());
        }
    }

    @SubscribeEvent
    public static void onMousePressed(ScreenEvent.MouseButtonPressed.Pre event) {
        if (!(event.getScreen() instanceof InventoryScreen screen) || event.getButton() != 0) {
            return;
        }
        int x = (screen.width - 176) / 2 + OVERLAY_X;
        int y = (screen.height - 166) / 2 + OVERLAY_Y;
        if (!isHovering(event.getMouseX(), event.getMouseY(), x, y)) {
            return;
        }
        PacketDistributor.sendToServer(new VoidNet.AccessoryActionPayload(hasCard ? 1 : 0));
        ((ICancellableEvent) event).setCanceled(true);
    }

    @SubscribeEvent
    public static void onMouseScroll(InputEvent.MouseScrollingEvent event) {
        if (Minecraft.getInstance().screen != null || !hasCard || !Screen.hasShiftDown()) {
            return;
        }
        double delta = event.getScrollDeltaY();
        if (delta == 0.0D) {
            return;
        }
        long now = System.currentTimeMillis();
        if (now - lastScrollToggle < SCROLL_DEBOUNCE_MS) {
            return;
        }
        boolean desired = delta < 0.0D;
        if (desired == auto) {
            return;
        }
        lastScrollToggle = now;
        auto = desired;
        PacketDistributor.sendToServer(new VoidNet.AccessoryActionPayload(desired ? 2 : 3));
        ((ICancellableEvent) event).setCanceled(true);
    }

    private static void drawSlot(GuiGraphics graphics, int x, int y) {
        graphics.fill(x, y, x + SLOT_SIZE, y + SLOT_SIZE, BORDER);
        graphics.fill(x + 1, y + 1, x + SLOT_SIZE - 1, y + SLOT_SIZE - 1, SLOT_BG);
    }

    private static boolean isHovering(double mouseX, double mouseY, int x, int y) {
        return mouseX >= x && mouseX < x + SLOT_SIZE && mouseY >= y && mouseY < y + SLOT_SIZE;
    }

    private static List<Component> tooltip() {
        List<Component> lines = new ArrayList<>();
        lines.add(Component.translatable("gui.voidgen.accessory"));
        if (hasCard) {
            lines.add(Component.translatable("tooltip.voidgen.binding_card.bind"));
            lines.add(Component.translatable("tooltip.voidgen.binding_card.auto"));
            lines.add(Component.translatable(auto ? "gui.voidgen.auto_on" : "gui.voidgen.auto_off"));
            lines.add(Component.translatable("gui.voidgen.bound", boundCount));
        } else {
            lines.add(Component.translatable("tooltip.voidgen.binding_card"));
        }
        return lines;
    }
}
