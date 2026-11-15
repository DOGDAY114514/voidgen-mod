import io
p = r"D:\AI\voidgen-mod\src\main\java\com\voidgen\VoidNet.java"
s = io.open(p, encoding="utf-8").read()
s = s.replace("import java.util.Optional;\n\n", "")
s = s.replace("import com.voidgen.client.VoidGenClient;\n\n", "")
s = s.replace("""/**
 * Tiny networking layer for the Binding Card accessory:
 * <ul>
 *     <li>C2S {@link AccessoryActionPayload}: equip / unequip / auto on / auto off, sent from
 *     the inventory-screen overlay and from Shift + scroll in the world.</li>
 *     <li>S2C {@link SyncPayload}: equipped flag, auto flag and bound count for the overlay.</li>
 * </ul>
 */
""", "/* Networking for the mob spawner selection. */\n")
s = s.replace("        registrar.playToServer(AccessoryActionPayload.TYPE, AccessoryActionPayload.STREAM_CODEC, VoidNet::handleAction);\n", "")
s = s.replace("        registrar.playToClient(SyncPayload.TYPE, SyncPayload.STREAM_CODEC,\n                (payload, context) -> context.enqueueWork(() -> VoidGenClient.applySync(payload)));\n", "")
start = s.find("    private static void handleAction(AccessoryActionPayload payload, IPayloadContext context) {")
end = s.find("    /** C2S: the mob the player picked in the spawner GUI. */")
if start == -1 or end == -1:
    raise SystemExit("markers missing")
s = s[:start] + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("VoidNet edited")