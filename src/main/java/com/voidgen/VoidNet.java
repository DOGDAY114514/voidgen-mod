package com.voidgen;

import java.util.Optional;

import com.voidgen.client.VoidGenClient;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

/**
 * Tiny networking layer for the Binding Card accessory:
 * <ul>
 *     <li>C2S {@link AccessoryActionPayload}: equip / unequip / auto on / auto off, sent from
 *     the inventory-screen overlay and from Shift + scroll in the world.</li>
 *     <li>S2C {@link SyncPayload}: equipped flag, auto flag and bound count for the overlay.</li>
 * </ul>
 */
public final class VoidNet {
    private VoidNet() {
    }

    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar("1");
        registrar.playToServer(AccessoryActionPayload.TYPE, AccessoryActionPayload.STREAM_CODEC, VoidNet::handleAction);
        registrar.playToClient(SyncPayload.TYPE, SyncPayload.STREAM_CODEC,
                (payload, context) -> context.enqueueWork(() -> VoidGenClient.applySync(payload)));
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

    private static void handleAction(AccessoryActionPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> {
            if (context.player() instanceof ServerPlayer player) {
                switch (payload.action()) {
                    case AccessoryActionPayload.EQUIP -> VoidAccessory.equip(player);
                    case AccessoryActionPayload.UNEQUIP -> VoidAccessory.unequip(player);
                    case AccessoryActionPayload.AUTO_ON -> VoidAccessory.setAuto(player, true);
                    case AccessoryActionPayload.AUTO_OFF -> VoidAccessory.setAuto(player, false);
                    default -> {
                    }
                }
            }
        });
    }

    /** C2S actions from the player accessory UI. */
    public record AccessoryActionPayload(int action) implements CustomPacketPayload {
        public static final int EQUIP = 0;
        public static final int UNEQUIP = 1;
        public static final int AUTO_ON = 2;
        public static final int AUTO_OFF = 3;

        public static final CustomPacketPayload.Type<AccessoryActionPayload> TYPE =
                new CustomPacketPayload.Type<>(ResourceLocation.fromNamespaceAndPath(VoidGen.MODID, "accessory_action"));

        public static final StreamCodec<RegistryFriendlyByteBuf, AccessoryActionPayload> STREAM_CODEC = StreamCodec.of(
                (buffer, payload) -> buffer.writeVarInt(payload.action()),
                buffer -> new AccessoryActionPayload(buffer.readVarInt()));

        @Override
        public CustomPacketPayload.Type<? extends CustomPacketPayload> type() {
            return TYPE;
        }
    }

    /** S2C state of the equipped accessory. */
    public record SyncPayload(boolean hasCard, boolean auto, int bound) implements CustomPacketPayload {
        public static final CustomPacketPayload.Type<SyncPayload> TYPE =
                new CustomPacketPayload.Type<>(ResourceLocation.fromNamespaceAndPath(VoidGen.MODID, "accessory_sync"));

        public static final StreamCodec<RegistryFriendlyByteBuf, SyncPayload> STREAM_CODEC = StreamCodec.of(
                (buffer, payload) -> {
                    buffer.writeBoolean(payload.hasCard());
                    buffer.writeBoolean(payload.auto());
                    buffer.writeVarInt(payload.bound());
                },
                buffer -> new SyncPayload(buffer.readBoolean(), buffer.readBoolean(), buffer.readVarInt()));

        @Override
        public CustomPacketPayload.Type<? extends CustomPacketPayload> type() {
            return TYPE;
        }
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
