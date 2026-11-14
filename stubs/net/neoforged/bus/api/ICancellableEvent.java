package net.neoforged.bus.api;

/**
 * Compile-only stub for FML's cancellable event marker interface (the real class lives in
 * FancyModLoader, which is not part of the cached NeoForge jar).
 */
public interface ICancellableEvent {
    void setCanceled(boolean canceled);

    boolean isCanceled();
}
