package com.voidgen.ae;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import appeng.api.config.Actionable;
import appeng.api.crafting.IPatternDetails;
import appeng.api.networking.IGrid;
import appeng.api.networking.IManagedGridNode;
import appeng.api.networking.security.IActionHost;
import appeng.api.networking.security.IActionSource;
import appeng.api.stacks.AEItemKey;
import appeng.api.stacks.GenericStack;
import appeng.api.stacks.KeyCounter;
import appeng.api.storage.MEStorage;
import appeng.helpers.patternprovider.PatternProviderLogic;
import appeng.helpers.patternprovider.PatternProviderLogicHost;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.TickTask;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.entity.BlockEntity;

/**
 * "Void crafting" pattern provider logic: when the crafting CPU pushes a pattern,
 * the outputs are inserted straight into the ME network. No machine is required,
 * but the pattern's inputs are still consumed from the ME network: AE2 extracts
 * them from the crafting CPU before calling us and keeps them consumed when we
 * return {@code true} (it refunds them when we return {@code false}).
 *
 * <p>Accepted outputs are AE2 processor-chain items, detected dynamically from the
 * item registry: any item whose registry id contains {@code processor}, plus the
 * {@code printed_*} intermediates made by the inscriber.</p>
 *
 * <p>Important: the actual insertion is deferred to the next server tick. AE2 only
 * adds the expected outputs to the CPU's {@code waitingFor} list <em>after</em>
 * {@link #pushPattern} returns; inserting synchronously would put the items into
 * storage before the CPU watches for them, leaving the job stuck in "requesting"
 * forever. Pushing them one tick later lets the crafting CPU intercept them
 * (it is registered as a storage provider on the grid) and finish the job.</p>
 */
public class VoidAssemblerLogic extends PatternProviderLogic {
    private static volatile Set<Item> processorCache;

    private final PatternProviderLogicHost hostRef;

    public VoidAssemblerLogic(IManagedGridNode node, PatternProviderLogicHost host) {
        super(node, host);
        this.hostRef = host;
    }

    @Override
    public boolean isBusy() {
        return false;
    }

    @Override
    public boolean pushPattern(IPatternDetails details, KeyCounter[] inputs) {
        IGrid grid = getGrid();
        if (grid == null) {
            return false;
        }

        List<GenericStack> outputs = details.getOutputs();
        if (outputs.isEmpty()) {
            return false;
        }
        for (GenericStack output : outputs) {
            if (!(output.what() instanceof AEItemKey itemKey) || !isAeProcessor(itemKey.getItem())) {
                return false;
            }
        }

        // Refuse "free" patterns: consuming nothing to create processors would be
        // duplicating items out of thin air. A real crafting pattern always has at
        // least one input stack.
        int inputEntries = 0;
        if (inputs != null) {
            for (KeyCounter counter : inputs) {
                inputEntries += counter.size();
            }
        }
        if (inputEntries <= 0) {
            return false;
        }

        BlockEntity host = hostRef.getBlockEntity();
        if (!(host.getLevel() instanceof ServerLevel serverLevel)) {
            return false;
        }
        MinecraftServer server = serverLevel.getServer();

        MEStorage storage = grid.getStorageService().getInventory();
        IActionSource source = IActionSource.ofMachine((IActionHost) host);
        // Simulate first, so a job is only accepted when every output can be stored.
        for (GenericStack output : outputs) {
            if (storage.insert(output.what(), output.amount(), Actionable.SIMULATE, source) < output.amount()) {
                return false;
            }
        }

        List<GenericStack> pending = new ArrayList<>(outputs.size());
        for (GenericStack output : outputs) {
            pending.add(new GenericStack(output.what(), output.amount()));
        }
        // Run after the current tick: by then the CPU has registered waitingFor.
        server.tell(new TickTask(server.getTickCount(), () -> insertOutputs(pending)));
        return true;
    }

    private void insertOutputs(List<GenericStack> outputs) {
        IGrid grid = getGrid();
        if (grid == null) {
            return;
        }
        MEStorage storage = grid.getStorageService().getInventory();
        IActionSource source = IActionSource.ofMachine((IActionHost) hostRef.getBlockEntity());
        for (GenericStack output : outputs) {
            long inserted = storage.insert(output.what(), output.amount(), Actionable.MODULATE, source);
            long leftover = output.amount() - inserted;
            if (leftover > 0) {
                // The return inventory is pushed back into the network by AE2 later,
                // so nothing is ever dropped on the floor.
                getReturnInv().insert(output.what(), leftover, Actionable.MODULATE, source);
            }
        }
    }

    /** Processor-chain detection: processors plus the inscriber's printed intermediates. */
    public static boolean isAeProcessor(Item item) {
        Set<Item> cache = processorCache;
        if (cache == null) {
            cache = scanProcessors();
            processorCache = cache;
        }
        return cache.contains(item);
    }

    private static Set<Item> scanProcessors() {
        Set<Item> found = new HashSet<>();
        for (Item item : BuiltInRegistries.ITEM) {
            ResourceLocation id = BuiltInRegistries.ITEM.getKey(item);
            String path = id.getPath();
            boolean printed = path.startsWith("printed_");
            boolean processor = path.contains("processor");
            boolean press = path.contains("press");
            if ((processor || printed) && !press) {
                found.add(item);
            }
        }
        return found;
    }
}
