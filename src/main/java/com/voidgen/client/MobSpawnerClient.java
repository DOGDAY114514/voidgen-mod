package com.voidgen.client;

import net.minecraft.client.Minecraft;

/** Client-only entry point so the common item class never loads client screens on a server. */
public final class MobSpawnerClient {
    private MobSpawnerClient() {
    }

    public static void open() {
        Minecraft.getInstance().setScreen(new MobSpawnerScreen());
    }
}
