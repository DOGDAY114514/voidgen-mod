package com.voidgen;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

/* Networking for the mob spawner selection. */
public final class VoidNet {
    private VoidNet() {
    }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar("1");
        registrar.playToServer(MobSelectPayload.TYPE, MobSelectPayload.STREAM_CODEC, VoidNet::handleMobSelect);
    }

    private static void handleMobSelect(MobSelectPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> {
            if (context.player() instanceof ServerPlayer player) {
                ItemStack stack = player.getMainHandItem();
                if (stack.getItem() instanceof com.voidgen.item.MobSpawnerItem) {
                    com.voidgen.item.MobSpawnerItem.setSelectedId(stack, payload.id());
                }
            }
        });
    }

    /** C2S: the mob the player picked in the spawner GUI. */
    public record MobSelectPayload(String id) implements CustomPacketPayload {
        public static final CustomPacketPayload.Type<MobSelectPayload> TYPE =
                new CustomPacketPayload.Type<>(ResourceLocation.fromNamespaceAndPath(VoidGen.MODID, "mob_select"));

        public static final StreamCodec<RegistryFriendlyByteBuf, MobSelectPayload> STREAM_CODEC = StreamCodec.of(
                (buffer, payload) -> buffer.writeUtf(payload.id(), 256),
                buffer -> new MobSelectPayload(buffer.readUtf(256)));

        @Override
        public CustomPacketPayload.Type<? extends CustomPacketPayload> type() {
            return TYPE;
        }
    }
}
