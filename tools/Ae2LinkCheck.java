public final class Ae2LinkCheck {
    private static final ClassLoader LOADER = Ae2LinkCheck.class.getClassLoader();

    public static void main(String[] args) throws Exception {
        Class<?> bridge = Class.forName("com.voidgen.AeBridge");
        System.out.println("AeBridge loaded: " + bridge.getName());

        Object present = bridge.getMethod("present").invoke(null);
        System.out.println("AeBridge.present() = " + present);

        Class<?> ac = Class.forName("appeng.api.AECapabilities", false, LOADER);
        java.lang.reflect.Field cap = ac.getField("IN_WORLD_GRID_NODE_HOST");
        System.out.println("IN_WORLD_GRID_NODE_HOST type = " + cap.getType().getName());

        Class<?> support = Class.forName("com.voidgen.ae.FurnaceAeSupport", false, LOADER);
        support.getMethod("registerGridCapability",
                Class.forName("net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent", false, LOADER),
                Class.forName("net.minecraft.world.level.block.entity.BlockEntityType", false, LOADER));
        System.out.println("FurnaceAeSupport.registerGridCapability resolved");

        Class<?> node = Class.forName("com.voidgen.ae.FurnaceGridNode", false, LOADER);
        System.out.println("FurnaceGridNode loaded: " + node.getName());
        System.out.println("interfaces: " + java.util.Arrays.toString(node.getInterfaces()));

        System.out.println("LINK CHECK OK");
    }
}
