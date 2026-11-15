package com.voidgen;

import java.util.ArrayList;
import java.util.List;

import com.voidgen.block.NothingnessCollectorBlock;
import com.voidgen.block.NothingnessCollectorBlockEntity;
import com.voidgen.block.NothingnessCollectorMenu;
import com.voidgen.block.NothingnessDistributorBlock;
import com.voidgen.block.NothingnessDistributorBlockEntity;
import com.voidgen.block.VoidFurnaceBlock;
import com.voidgen.block.VoidFurnaceBlockEntity;
import com.voidgen.block.VoidFurnaceMenu;
import com.voidgen.block.VoidGeneratorBlock;
import com.voidgen.block.VoidGeneratorBlockEntity;
import com.voidgen.block.VoidGeneratorMenu;
import com.voidgen.block.MeVoidSupplierBlock;
import com.voidgen.block.MeVoidSupplierBlockEntity;
import com.voidgen.item.FilledVoidStorageItem;
import com.voidgen.item.MobSpawnerItem;
import com.voidgen.item.NestUpgradeItem;
import com.voidgen.item.UpgradeCardItem;
import com.voidgen.item.VoidConfiguratorItem;
import com.voidgen.item.VoidFurnaceItem;
import com.voidgen.item.VoidGeneratorItem;
import com.voidgen.item.VoidValueItem;
import com.voidgen.item.VoidStorageItem;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.event.level.BlockEvent;
import net.neoforged.neoforge.event.level.ChunkEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Voidgen: a free-energy generator built for AE2 bases. Generates FE out of nothing,
 * stores it, feeds machines wirelessly and can be upgraded with AE2-style cards.
 */
@Mod(VoidGen.MODID)
public class VoidGen {
    public static final String MODID = "voidgen";

    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, MODID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, MODID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, MODID);
    public static final DeferredRegister<MenuType<?>> MENUS = DeferredRegister.create(Registries.MENU, MODID);
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    public static final DeferredHolder<Block, VoidGeneratorBlock> VOID_GENERATOR = BLOCKS.register("void_generator",
            () -> new VoidGeneratorBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(4.0F, 5.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.METAL)));

    public static final DeferredHolder<Item, VoidGeneratorItem> VOID_GENERATOR_ITEM = ITEMS.register("void_generator",
            () -> new VoidGeneratorItem(VOID_GENERATOR.get(), new Item.Properties()));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<VoidGeneratorBlockEntity>> VOID_GENERATOR_BE =
            BLOCK_ENTITIES.register("void_generator", () -> BlockEntityType.Builder.<VoidGeneratorBlockEntity>of(
                    (pos, state) -> new VoidGeneratorBlockEntity(pos, state), VOID_GENERATOR.get()).build(null));

    public static final List<DeferredHolder<Item, NestUpgradeItem>> NEST_UPGRADES = new ArrayList<>();

    static {
        for (int i = 1; i <= 5; i++) {
            final int tier = i;
            NEST_UPGRADES.add(ITEMS.register("nest_upgrade_" + i, () -> new NestUpgradeItem(tier, new Item.Properties())));
        }
    }

    public static final DeferredHolder<Item, UpgradeCardItem> ACCEL_CARD = ITEMS.register("accel_card",
            () -> new UpgradeCardItem(UpgradeCardItem.Type.ACCELERATION, new Item.Properties()));

    public static final DeferredHolder<Item, UpgradeCardItem> OVERCLOCK_CARD = ITEMS.register("overclock_card",
            () -> new UpgradeCardItem(UpgradeCardItem.Type.OVERCLOCK, new Item.Properties()));

    public static final DeferredHolder<Item, UpgradeCardItem> CAPACITY_CARD = ITEMS.register("capacity_card",
            () -> new UpgradeCardItem(UpgradeCardItem.Type.CAPACITY, new Item.Properties()));

    public static final DeferredHolder<Item, UpgradeCardItem> RANGE_CARD = ITEMS.register("range_card",
            () -> new UpgradeCardItem(UpgradeCardItem.Type.RANGE, new Item.Properties()));

    /** Accessory card: scopes wireless power to the machines it binds (auto-connect mode). */
    // ---- AE2 storage disks: materials + the 1K..256M void disks ----

    public static final DeferredHolder<Item, Item> VOID_INGOT = ITEMS.register("void_ingot",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    public static final DeferredHolder<Block, Block> VOID_INGOT_BLOCK = BLOCKS.register("void_ingot_block",
            () -> new Block(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE)
                    .strength(5.0F, 6.0F).requiresCorrectToolForDrops().sound(SoundType.METAL)));

    public static final DeferredHolder<Item, BlockItem> VOID_INGOT_BLOCK_ITEM = ITEMS.register("void_ingot_block",
            () -> new BlockItem(VOID_INGOT_BLOCK.get(), new Item.Properties().rarity(Rarity.UNCOMMON)));

    // ---- floating crystal family (certus-series inspired) ----

    public static final DeferredHolder<Item, Item> FLOATING_CRYSTAL = ITEMS.register("floating_crystal",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    public static final DeferredHolder<Item, Item> FLOATING_CRYSTAL_DUST = ITEMS.register("floating_crystal_dust",
            () -> new Item(new Item.Properties()));

    public static final DeferredHolder<Block, Block> FLOATING_BUDDING_DAMAGED = budding("floating_budding_damaged");
    public static final DeferredHolder<Block, Block> FLOATING_BUDDING_CHIPPED = budding("floating_budding_chipped");
    public static final DeferredHolder<Block, Block> FLOATING_BUDDING_FLAWED = budding("floating_budding_flawed");
    public static final DeferredHolder<Block, Block> FLOATING_BUDDING_FLAWLESS = budding("floating_budding_flawless");

    public static final DeferredHolder<Item, BlockItem> FLOATING_BUDDING_DAMAGED_ITEM = buddingItem("floating_budding_damaged", FLOATING_BUDDING_DAMAGED);
    public static final DeferredHolder<Item, BlockItem> FLOATING_BUDDING_CHIPPED_ITEM = buddingItem("floating_budding_chipped", FLOATING_BUDDING_CHIPPED);
    public static final DeferredHolder<Item, BlockItem> FLOATING_BUDDING_FLAWED_ITEM = buddingItem("floating_budding_flawed", FLOATING_BUDDING_FLAWED);
    public static final DeferredHolder<Item, BlockItem> FLOATING_BUDDING_FLAWLESS_ITEM = buddingItem("floating_budding_flawless", FLOATING_BUDDING_FLAWLESS);

    private static DeferredHolder<Block, Block> budding(String id) {
        return BLOCKS.register(id, () -> new Block(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE)
                .strength(4.0F, 8.0F).requiresCorrectToolForDrops().sound(SoundType.STONE)));
    }

    private static DeferredHolder<Item, BlockItem> buddingItem(String id, DeferredHolder<Block, Block> block) {
        return ITEMS.register(id, () -> new BlockItem(block.get(), new Item.Properties()));
    }


    /** The 1K..256M void components, one per disk tier. */
    public static final java.util.List<DeferredHolder<Item, Item>> VOID_COMPONENTS = new java.util.ArrayList<>();

    static {
        for (String tier : VoidCellItems.TIERS) {
            VOID_COMPONENTS.add(ITEMS.register("void_component_" + tier,
                    () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON))));
        }
    }

    public static final DeferredHolder<Item, Item> VOID_CELL_HOUSING = ITEMS.register("void_cell_housing",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    /** Circuit board sliced from a void block; pressed into floating processors. */
    public static final DeferredHolder<Item, Item> VOID_CIRCUIT_BOARD = ITEMS.register("void_circuit_board",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    /** The processor used by 1M..256M void storage components. */
    public static final DeferredHolder<Item, Item> VOID_PROCESSOR = ITEMS.register("void_processor",
            () -> new Item(new Item.Properties().rarity(Rarity.UNCOMMON)));

    // ---- Void Furnace ----

    public static final DeferredHolder<Block, VoidFurnaceBlock> VOID_FURNACE = BLOCKS.register("void_furnace",
            () -> new VoidFurnaceBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(4.0F, 5.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.METAL)));

    public static final DeferredHolder<Item, VoidFurnaceItem> VOID_FURNACE_ITEM = ITEMS.register("void_furnace",
            () -> new VoidFurnaceItem(VOID_FURNACE.get(), new Item.Properties()));

    public static final DeferredHolder<Item, VoidConfiguratorItem> VOID_CONFIGURATOR = ITEMS.register("void_configurator",
            () -> new VoidConfiguratorItem(new Item.Properties().stacksTo(1)));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<VoidFurnaceBlockEntity>> VOID_FURNACE_BE =
            BLOCK_ENTITIES.register("void_furnace", () -> BlockEntityType.Builder.<VoidFurnaceBlockEntity>of(
                    (pos, state) -> new VoidFurnaceBlockEntity(pos, state), VOID_FURNACE.get()).build(null));

    public static final DeferredHolder<MenuType<?>, MenuType<VoidFurnaceMenu>> VOID_FURNACE_MENU = MENUS.register("void_furnace",
            () -> new MenuType<>(VoidFurnaceMenu::new, FeatureFlags.DEFAULT_FLAGS));

    public static final DeferredHolder<MenuType<?>, MenuType<VoidGeneratorMenu>> VOIDGEN_MENU = MENUS.register("void_generator",
            () -> new MenuType<>(VoidGeneratorMenu::new, FeatureFlags.DEFAULT_FLAGS));

    // ---- Nothingness (虚无) blocks / items ----

    public static final DeferredHolder<Block, NothingnessCollectorBlock> NOTHING_COLLECTOR_1 = registerCollector(1);
    public static final DeferredHolder<Block, NothingnessCollectorBlock> NOTHING_COLLECTOR_2 = registerCollector(2);
    public static final DeferredHolder<Block, NothingnessCollectorBlock> NOTHING_COLLECTOR_3 = registerCollector(3);
    public static final DeferredHolder<Block, NothingnessCollectorBlock> NOTHING_COLLECTOR_4 = registerCollector(4);
    public static final DeferredHolder<Block, NothingnessCollectorBlock> NOTHING_COLLECTOR_5 = registerCollector(5);

    public static final DeferredHolder<Item, BlockItem> NOTHING_COLLECTOR_1_ITEM = ITEMS.register("nothing_collector_1",
            () -> new BlockItem(NOTHING_COLLECTOR_1.get(), new Item.Properties()));
    public static final DeferredHolder<Item, BlockItem> NOTHING_COLLECTOR_2_ITEM = ITEMS.register("nothing_collector_2",
            () -> new BlockItem(NOTHING_COLLECTOR_2.get(), new Item.Properties()));
    public static final DeferredHolder<Item, BlockItem> NOTHING_COLLECTOR_3_ITEM = ITEMS.register("nothing_collector_3",
            () -> new BlockItem(NOTHING_COLLECTOR_3.get(), new Item.Properties()));
    public static final DeferredHolder<Item, BlockItem> NOTHING_COLLECTOR_4_ITEM = ITEMS.register("nothing_collector_4",
            () -> new BlockItem(NOTHING_COLLECTOR_4.get(), new Item.Properties()));
    public static final DeferredHolder<Item, BlockItem> NOTHING_COLLECTOR_5_ITEM = ITEMS.register("nothing_collector_5",
            () -> new BlockItem(NOTHING_COLLECTOR_5.get(), new Item.Properties()));

    public static final DeferredHolder<Block, NothingnessDistributorBlock> NOTHING_DISTRIBUTOR = BLOCKS.register("nothing_distributor",
            () -> new NothingnessDistributorBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(4.0F, 5.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.METAL)));
    public static final DeferredHolder<Item, BlockItem> NOTHING_DISTRIBUTOR_ITEM = ITEMS.register("nothing_distributor",
            () -> new BlockItem(NOTHING_DISTRIBUTOR.get(), new Item.Properties()));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<NothingnessCollectorBlockEntity>> NOTHING_COLLECTOR_BE =
            BLOCK_ENTITIES.register("nothing_collector", () -> BlockEntityType.Builder.<NothingnessCollectorBlockEntity>of(
                    (pos, state) -> new NothingnessCollectorBlockEntity(pos, state),
                    NOTHING_COLLECTOR_1.get(), NOTHING_COLLECTOR_2.get(), NOTHING_COLLECTOR_3.get(),
                    NOTHING_COLLECTOR_4.get(), NOTHING_COLLECTOR_5.get()).build(null));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<NothingnessDistributorBlockEntity>> NOTHING_DISTRIBUTOR_BE =
            BLOCK_ENTITIES.register("nothing_distributor", () -> BlockEntityType.Builder.<NothingnessDistributorBlockEntity>of(
                    (pos, state) -> new NothingnessDistributorBlockEntity(pos, state), NOTHING_DISTRIBUTOR.get()).build(null));

    // ---- ME 虚无供应器（v2.2） ----

    public static final DeferredHolder<Item, VoidValueItem> VOID_VALUE = ITEMS.register("void_value",
            () -> new VoidValueItem(new Item.Properties().stacksTo(64)));

    public static final DeferredHolder<Block, MeVoidSupplierBlock> ME_VOID_SUPPLIER = BLOCKS.register("me_void_supplier",
            () -> new MeVoidSupplierBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(4.0F, 5.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.METAL)));
    public static final DeferredHolder<Item, BlockItem> ME_VOID_SUPPLIER_ITEM = ITEMS.register("me_void_supplier",
            () -> new BlockItem(ME_VOID_SUPPLIER.get(), new Item.Properties()));
    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<MeVoidSupplierBlockEntity>> ME_VOID_SUPPLIER_BE =
            BLOCK_ENTITIES.register("me_void_supplier", () -> BlockEntityType.Builder.<MeVoidSupplierBlockEntity>of(
                    (pos, state) -> new MeVoidSupplierBlockEntity(pos, state), ME_VOID_SUPPLIER.get()).build(null));

    // ---- AE2 虚空合成器（仅当 AE2 存在时由反射安装） ----

    public static DeferredHolder<Block, ? extends Block> VOID_ASSEMBLER_BLOCK;
    public static DeferredHolder<Item, ? extends Item> VOID_ASSEMBLER_ITEM;
    public static DeferredHolder<BlockEntityType<?>, ? extends BlockEntityType<?>> VOID_ASSEMBLER_BE;

    public static final DeferredHolder<MenuType<?>, MenuType<NothingnessCollectorMenu>> NOTHING_COLLECTOR_MENU =
            MENUS.register("nothing_collector", () -> new MenuType<>(NothingnessCollectorMenu::new, FeatureFlags.DEFAULT_FLAGS));

    public static final DeferredHolder<Item, FilledVoidStorageItem> FILLED_VOID_STORAGE_IRON = ITEMS.register("filled_void_storage_iron",
            () -> new FilledVoidStorageItem(1, new Item.Properties()));
    public static final DeferredHolder<Item, FilledVoidStorageItem> FILLED_VOID_STORAGE_GOLD = ITEMS.register("filled_void_storage_gold",
            () -> new FilledVoidStorageItem(2, new Item.Properties()));
    public static final DeferredHolder<Item, FilledVoidStorageItem> FILLED_VOID_STORAGE_DIAMOND = ITEMS.register("filled_void_storage_diamond",
            () -> new FilledVoidStorageItem(3, new Item.Properties()));
    public static final DeferredHolder<Item, FilledVoidStorageItem> FILLED_VOID_STORAGE_EMERALD = ITEMS.register("filled_void_storage_emerald",
            () -> new FilledVoidStorageItem(4, new Item.Properties()));

    public static final DeferredHolder<Item, VoidStorageItem> VOID_STORAGE_IRON = ITEMS.register("void_storage_iron",
            () -> new VoidStorageItem(1, 1_000L, () -> FILLED_VOID_STORAGE_IRON.get(), new Item.Properties()));
    public static final DeferredHolder<Item, VoidStorageItem> VOID_STORAGE_GOLD = ITEMS.register("void_storage_gold",
            () -> new VoidStorageItem(2, 10_000L, () -> FILLED_VOID_STORAGE_GOLD.get(), new Item.Properties()));
    public static final DeferredHolder<Item, VoidStorageItem> VOID_STORAGE_DIAMOND = ITEMS.register("void_storage_diamond",
            () -> new VoidStorageItem(3, 100_000L, () -> FILLED_VOID_STORAGE_DIAMOND.get(), new Item.Properties()));
    public static final DeferredHolder<Item, VoidStorageItem> VOID_STORAGE_EMERALD = ITEMS.register("void_storage_emerald",
            () -> new VoidStorageItem(4, 1_000_000L, () -> FILLED_VOID_STORAGE_EMERALD.get(), new Item.Properties()));
    public static final DeferredHolder<Item, VoidStorageItem> VOID_STORAGE_NETHER = ITEMS.register("void_storage_nether",
            () -> new VoidStorageItem(5, Long.MAX_VALUE, () -> null, new Item.Properties().rarity(Rarity.EPIC)));

    public static final DeferredHolder<Item, MobSpawnerItem> MOB_SPAWNER = ITEMS.register("mob_spawner",
            () -> new MobSpawnerItem(new Item.Properties().stacksTo(1)));

    /** 虚无存储器容量：铁 1,000 → 下界之星无限（每级 ×10）。 */
    public static long storageCap(int tier) {
        return switch (tier) {
            case 1 -> 1_000L;
            case 2 -> 10_000L;
            case 3 -> 100_000L;
            case 4 -> 1_000_000L;
            default -> Long.MAX_VALUE;
        };
    }

    private static DeferredHolder<Block, NothingnessCollectorBlock> registerCollector(int tier) {
        return BLOCKS.register("nothing_collector_" + tier, () -> new NothingnessCollectorBlock(tier,
                BlockBehaviour.Properties.of()
                        .mapColor(MapColor.COLOR_PURPLE)
                        .strength(4.0F, 5.0F)
                        .requiresCorrectToolForDrops()
                        .sound(SoundType.METAL)));
    }

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> VOIDGEN_TAB = TABS.register("voidgen",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.voidgen"))
                    .icon(() -> new ItemStack(VOID_GENERATOR_ITEM.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(VOID_GENERATOR_ITEM.get());
                        for (DeferredHolder<Item, NestUpgradeItem> holder : NEST_UPGRADES) {
                            output.accept(holder.get());
                        }
                        output.accept(ACCEL_CARD.get());
                        output.accept(OVERCLOCK_CARD.get());
                        output.accept(CAPACITY_CARD.get());
                        output.accept(RANGE_CARD.get());
                        output.accept(VOID_FURNACE_ITEM.get());
                        output.accept(VOID_CONFIGURATOR.get());
                        output.accept(VOID_STORAGE_IRON.get());
                        output.accept(VOID_STORAGE_GOLD.get());
                        output.accept(VOID_STORAGE_DIAMOND.get());
                        output.accept(VOID_STORAGE_EMERALD.get());
                        output.accept(VOID_STORAGE_NETHER.get());
                        output.accept(FILLED_VOID_STORAGE_IRON.get());
                        output.accept(FILLED_VOID_STORAGE_GOLD.get());
                        output.accept(FILLED_VOID_STORAGE_DIAMOND.get());
                        output.accept(FILLED_VOID_STORAGE_EMERALD.get());
                        output.accept(NOTHING_COLLECTOR_1_ITEM.get());
                        output.accept(NOTHING_COLLECTOR_2_ITEM.get());
                        output.accept(NOTHING_COLLECTOR_3_ITEM.get());
                        output.accept(NOTHING_COLLECTOR_4_ITEM.get());
                        output.accept(NOTHING_COLLECTOR_5_ITEM.get());
                        output.accept(NOTHING_DISTRIBUTOR_ITEM.get());
                        output.accept(ME_VOID_SUPPLIER_ITEM.get());
                        if (VOID_ASSEMBLER_ITEM != null) {
                            output.accept(VOID_ASSEMBLER_ITEM.get());
                        }
                        output.accept(VOID_VALUE.get());
                        output.accept(MOB_SPAWNER.get());
                        output.accept(VOID_INGOT.get());
                        output.accept(VOID_INGOT_BLOCK_ITEM.get());
                        output.accept(FLOATING_CRYSTAL.get());
                        output.accept(FLOATING_CRYSTAL_DUST.get());
                        output.accept(FLOATING_BUDDING_DAMAGED_ITEM.get());
                        output.accept(FLOATING_BUDDING_CHIPPED_ITEM.get());
                        output.accept(FLOATING_BUDDING_FLAWED_ITEM.get());
                        output.accept(FLOATING_BUDDING_FLAWLESS_ITEM.get());
                        for (DeferredHolder<Item, Item> component : VOID_COMPONENTS) {
                            output.accept(component.get());
                        }
                        output.accept(VOID_CELL_HOUSING.get());
                        output.accept(VOID_CIRCUIT_BOARD.get());
                        output.accept(VOID_PROCESSOR.get());
                        for (DeferredHolder<Item, ? extends Item> cell : VoidCellItems.CELLS) {
                            output.accept(cell.get());
                        }
                    })
                    .build());

    public VoidGen(IEventBus modBus) {
        VoidCellItems.install(ITEMS);
        AeAssemblerBridge.install(BLOCKS, ITEMS, BLOCK_ENTITIES);

        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        BLOCK_ENTITIES.register(modBus);
        MENUS.register(modBus);
        TABS.register(modBus);

        modBus.addListener(RegisterCapabilitiesEvent.class, event -> event.registerBlockEntity(
                Capabilities.EnergyStorage.BLOCK, VOID_GENERATOR_BE.get(), (blockEntity, side) -> blockEntity.getEnergyStorage()));

        modBus.addListener(RegisterCapabilitiesEvent.class, event -> event.registerBlockEntity(
                Capabilities.ItemHandler.BLOCK, VOID_FURNACE_BE.get(), (blockEntity, side) -> blockEntity.getItemHandler(side)));

        modBus.addListener(RegisterCapabilitiesEvent.class, event -> event.registerBlockEntity(
                Capabilities.ItemHandler.BLOCK, ME_VOID_SUPPLIER_BE.get(), (blockEntity, side) -> blockEntity.getItemHandler()));

        // Optional AE2: expose the furnace as an in-world grid node host so cables connect.
        modBus.addListener(RegisterCapabilitiesEvent.class,
                event -> AeBridge.registerGridCapability(event, VOID_FURNACE_BE.get()));

        // Optional AE2: the void assembler is itself a grid node host (pattern provider).
        modBus.addListener(RegisterCapabilitiesEvent.class, AeAssemblerBridge::registerGridCapability);

        modBus.addListener(RegisterPayloadHandlersEvent.class, VoidNet::register);
        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.addListener(net.neoforged.neoforge.event.tick.ServerTickEvent.Post.class,
                event -> VoidGeneratorBlockEntity.tickAll(event.getServer()));

        NeoForge.EVENT_BUS.addListener(BlockEvent.EntityPlaceEvent.class, VoidPowerNetwork::onPlace);
        NeoForge.EVENT_BUS.addListener(ChunkEvent.Load.class, VoidPowerNetwork::onChunkLoad);
        NeoForge.EVENT_BUS.addListener(BlockEvent.BreakEvent.class, VoidPowerNetwork::onBreak);
        NeoForge.EVENT_BUS.addListener(EntityTickEvent.Post.class, VoidDropHandler::onEntityTick);
        NeoForge.EVENT_BUS.addListener(EntityTickEvent.Post.class, WaterCrystalHandler::onEntityTick);
    }
}
