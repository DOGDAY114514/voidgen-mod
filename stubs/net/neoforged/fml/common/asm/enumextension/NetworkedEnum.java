package net.neoforged.fml.common.asm.enumextension;

/** Compile-only stub for NeoForge's networked enum API (never packaged). */
public interface NetworkedEnum<T extends Enum<T>> {
    enum NetworkCheck {
        BIDIRECTIONAL,
        SERVERBOUND,
        CLIENTBOUND
    }
}
