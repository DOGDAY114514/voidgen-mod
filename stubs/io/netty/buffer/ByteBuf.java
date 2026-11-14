package io.netty.buffer;

/**
 * Compile-only stub for netty's ByteBuf: the cached NeoForge jar references it from
 * FriendlyByteBuf signatures, but netty itself is not on disk. Never packaged.
 */
public class ByteBuf {
    public ByteBuf writeVarInt(int value) {
        return this;
    }

    public int readVarInt() {
        return 0;
    }

    public ByteBuf writeBoolean(boolean value) {
        return this;
    }

    public boolean readBoolean() {
        return false;
    }
}
