package com.voidgen.client;

import com.voidgen.VoidGen;

import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

/**
 * Client-only wiring: container screens plus the G-key in-game guide.
 */
@EventBusSubscriber(modid = VoidGen.MODID, value = Dist.CLIENT)
public final class VoidGenClient {
    private static final KeyMapping GUIDE_KEY = new KeyMapping("key.voidgen.guide", 71, "key.categories.voidgen");

    private VoidGenClient() {
    }

    @SubscribeEvent
    public static void onRegisterScreens(RegisterMenuScreensEvent event) {
        event.register(VoidGen.VOIDGEN_MENU.get(), VoidGeneratorScreen::new);
        event.register(VoidGen.VOID_FURNACE_MENU.get(), VoidFurnaceScreen::new);
        event.register(VoidGen.NOTHING_COLLECTOR_MENU.get(), NothingnessCollectorScreen::new);
    }

    @SubscribeEvent
    public static void onRegisterKeys(RegisterKeyMappingsEvent event) {
        event.register(GUIDE_KEY);
    }

    @SubscribeEvent
    public static void onClientTick(ClientTickEvent.Post event) {
        Minecraft minecraft = Minecraft.getInstance();
        while (GUIDE_KEY.consumeClick()) {
            if (minecraft.screen == null) {
                minecraft.setScreen(new VoidGuideScreen());
            }
        }
    }
}
