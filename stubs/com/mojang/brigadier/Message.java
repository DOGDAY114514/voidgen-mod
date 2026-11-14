package com.mojang.brigadier;

/**
 * Compile-only stub for Brigadier's Message, which is a supertype of
 * net.minecraft.network.chat.FormattedText/Component. The real library jar is
 * supplied by the Minecraft runtime.
 */
public interface Message {
    String getString();
}
