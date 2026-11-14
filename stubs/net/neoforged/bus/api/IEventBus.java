package net.neoforged.bus.api;

import java.util.function.Consumer;

/**
 * Compile-only stub for FancyModLoader's event bus. Matches the real
 * net.neoforged:bus interface descriptors used by compiled mod classes.
 */
public interface IEventBus {
    void register(Object target);

    <T> void addListener(Class<T> eventType, Consumer<T> consumer);
}
