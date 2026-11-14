import java.lang.reflect.Field;
import java.lang.reflect.Method;

/**
 * Offline probe: verifies that the reflective strings used by AeReturn exist in the
 * AE2 19.x jar. Run with the AE2 jar + the patched NeoForge/Minecraft jar on the classpath.
 */
public final class Ae2Check {
    public static void main(String[] args) throws Exception {
        ClassLoader cl = Ae2Check.class.getClassLoader();

        probe(cl, "appeng.api.AECapabilities", "GENERIC_INTERNAL_INV");
        probe(cl, "appeng.capabilities.Capabilities", "GENERIC_INTERNAL_INV");

        Class<?> inv = Class.forName("appeng.api.behaviors.GenericInternalInventory", false, cl);
        Class<?> key = Class.forName("appeng.api.stacks.AEKey", false, cl);
        Class<?> actionable = Class.forName("appeng.api.config.Actionable", false, cl);
        Method insert = inv.getMethod("insert", int.class, key, long.class, actionable);
        System.out.println("OK  GenericInternalInventory.insert: " + insert);

        Class<?> itemKey = Class.forName("appeng.api.stacks.AEItemKey", false, cl);
        System.out.println("OK  AEItemKey.of: " + itemKey.getMethod("of", Class.forName("net.minecraft.world.item.ItemStack", false, cl)));

        Field modulate = actionable.getField("MODULATE");
        System.out.println("OK  Actionable.MODULATE: " + modulate);
    }

    private static void probe(ClassLoader cl, String holder, String fieldName) {
        try {
            Class<?> c = Class.forName(holder, false, cl);
            Field f = c.getField(fieldName);
            System.out.println("OK  " + holder + "." + fieldName + " : " + f.getType().getName());
        } catch (Throwable t) {
            System.out.println("MISSING " + holder + "." + fieldName + " (" + t.getClass().getSimpleName() + ": " + t.getMessage() + ")");
        }
    }
}
