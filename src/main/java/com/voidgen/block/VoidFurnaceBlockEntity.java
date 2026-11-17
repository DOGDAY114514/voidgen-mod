package com.voidgen.block;

import com.voidgen.AeBridge;
import com.voidgen.AeReturn;
import com.voidgen.GridHost;
import com.voidgen.VoidGen;
import com.voidgen.VoidPowerNetwork;
import com.voidgen.VoidStats;
import com.voidgen.item.UpgradeCardItem;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.MenuProvider;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.RecipeHolder;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleRecipeInput;
import net.minecraft.world.item.crafting.SmeltingRecipe;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.items.IItemHandler;
import net.neoforged.neoforge.items.ItemHandlerHelper;
import net.neoforged.neoforge.items.ItemStackHandler;

import java.util.Arrays;
import java.util.List;

/**
 * Free-smelting furnace: no fuel, no FE. 9 input slots, 9 output slots, 12 card slots.
 * Total throughput is spread over the 9 input slots with a rotating remainder so no slot starves.
 */
public class VoidFurnaceBlockEntity extends BlockEntity implements MenuProvider {
    public enum FaceMode { INPUT, OUTPUT, DISABLED }

    public static final int DATA_SLOTS = 8;
    private static final int PUSH_BUDGET = 4_096;
    private static final int WIRELESS_MIN_BUDGET = 4_096;
    private static final int WIRELESS_MAX_BUDGET = 65_536;
    private static final int WIRELESS_CHECK_LIMIT = 64;

    private final ItemStackHandler inputs;
    private final ItemStackHandler outputs;
    private final ItemStackHandler cards;
    private final FaceMode[] faces = new FaceMode[6];

    private final ContainerData data = new ContainerData() {
        @Override
        public int get(int index) {
            return switch (index) {
                case 0 -> rate();
                case 1 -> tier;
                case 2 -> accelCards();
                case 3 -> capacity();
                case 4 -> (wirelessEnabled ? 1 : 0) | (aeReturn ? 2 : 0);
                case 5 -> rangeInt();
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
            // display data is authoritative on the server side
        }

        @Override
        public int getCount() {
            return DATA_SLOTS;
        }
    };

    private int tier;
    private boolean wirelessEnabled;
    private boolean aeReturn;
    private long voidBuffer;
    private int rotation;
    private int wirelessCursor;
    private Object gridHost;
    private boolean gridHostAttempted;
    private CompoundTag pendingGridTag;

    @SuppressWarnings("unchecked")
    private final RecipeHolder<SmeltingRecipe>[] cachedRecipes = new RecipeHolder[VoidStats.FURNACE_SLOTS];
    private final Item[] cachedItems = new Item[VoidStats.FURNACE_SLOTS];

    public VoidFurnaceBlockEntity(BlockPos pos, BlockState state) {
        super(VoidGen.VOID_FURNACE_BE.get(), pos, state);
        Arrays.fill(faces, FaceMode.INPUT);
        this.inputs = new ItemStackHandler(VoidStats.FURNACE_SLOTS) {
            @Override
            protected int getStackLimit(int slot, ItemStack stack) {
                return capacity();
            }

            @Override
            protected void onContentsChanged(int slot) {
                setChanged();
            }
        };
        this.outputs = new ItemStackHandler(VoidStats.FURNACE_SLOTS) {
            @Override
            protected int getStackLimit(int slot, ItemStack stack) {
                return capacity();
            }

            @Override
            protected void onContentsChanged(int slot) {
                setChanged();
            }
        };
        this.cards = new ItemStackHandler(VoidStats.FURNACE_CARD_SLOTS) {
            @Override
            public boolean isItemValid(int slot, ItemStack stack) {
                return VoidStats.isFurnaceCard(stack);
            }

            @Override
            protected void onContentsChanged(int slot) {
                setChanged();
                refreshCaches();
            }
        };
    }

    // ------------------------------------------------------------------ accessors

    /** 破坏方块时把输入/输出/卡槽里的东西掉出来。 */
    public void dropContents(Level level) {
        dropHandler(level, inputs);
        dropHandler(level, outputs);
        dropHandler(level, cards);
    }

    private void dropHandler(Level level, ItemStackHandler handler) {
        for (int i = 0; i < handler.getSlots(); i++) {
            ItemStack stack = handler.getStackInSlot(i);
            if (!stack.isEmpty()) {
                net.minecraft.world.level.block.Block.popResource(level, worldPosition, stack);
                handler.setStackInSlot(i, ItemStack.EMPTY);
            }
        }
    }

    public ItemStackHandler inputs() {
        return inputs;
    }

    public ItemStackHandler outputs() {
        return outputs;
    }

    public ItemStackHandler cards() {
        return cards;
    }

    public ContainerData containerData() {
        return data;
    }

    public int accelCards() {
        return VoidStats.count(cards, UpgradeCardItem.Type.ACCELERATION)
                + VoidStats.count(cards, UpgradeCardItem.Type.OVERCLOCK);
    }

    public int capacityCards() {
        return VoidStats.count(cards, UpgradeCardItem.Type.CAPACITY);
    }

    public int rangeCards() {
        return VoidStats.count(cards, UpgradeCardItem.Type.RANGE);
    }

    public int capacity() {
        return VoidStats.furnaceCapacity(tier, capacityCards());
    }

    public int rate() {
        return VoidStats.furnaceRate(accelCards(), 0);
    }

    public long range() {
        return VoidStats.furnaceRange(rangeCards());
    }

    public int rangeInt() {
        long value = range();
        return value == Long.MAX_VALUE ? -1 : (int) Math.min(Integer.MAX_VALUE, value);
    }

    public int tier() {
        return tier;
    }

    /** Sets the tier from a placed item and mirrors it into the block state. */
    public void setTier(int newTier) {
        this.tier = Math.max(0, Math.min(VoidStats.MAX_TIER, newTier));
        syncTierState();
        setChanged();
    }

    /** Keeps the block state in sync with the stored tier. */
    public void syncTierState() {
        if (level == null || level.isClientSide()) {
            return;
        }
        BlockState state = getBlockState();
        if (state.getBlock() instanceof VoidFurnaceBlock
                && state.hasProperty(VoidFurnaceBlock.TIER)
                && state.getValue(VoidFurnaceBlock.TIER) != tier) {
            level.setBlock(worldPosition, state.setValue(VoidFurnaceBlock.TIER, Math.min(tier, 5)), 3);
        }
    }

    public boolean wirelessEnabled() {
        return wirelessEnabled;
    }

    public void toggleWireless() {
        wirelessEnabled = !wirelessEnabled;
        setChanged();
    }

    public boolean aeReturn() {
        return aeReturn;
    }

    public void toggleAeReturn() {
        aeReturn = !aeReturn;
        setChanged();
    }

    public FaceMode faceMode(Direction face) {
        return faces[face.ordinal()];
    }

    public FaceMode cycleFace(Direction face) {
        int index = face.ordinal();
        faces[index] = switch (faces[index]) {
            case INPUT -> FaceMode.OUTPUT;
            case OUTPUT -> FaceMode.DISABLED;
            case DISABLED -> FaceMode.INPUT;
        };
        setChanged();
        return faces[index];
    }

    public boolean tryUpgrade(int nextTier) {
        if (nextTier != tier + 1 || tier >= VoidStats.MAX_TIER) {
            return false;
        }
        tier = nextTier;
        syncTierState();
        setChanged();
        return true;
    }

    public boolean tryInsertCard(ItemStack stack) {
        if (!VoidStats.isFurnaceCard(stack)) {
            return false;
        }
        for (int i = 0; i < cards.getSlots(); i++) {
            ItemStack single = stack.copyWithCount(1);
            if (cards.insertItem(i, single, true).isEmpty()) {
                cards.insertItem(i, single, false);
                return true;
            }
        }
        return false;
    }

    /**
     * Sided item handler: INPUT faces may only insert into input slots, OUTPUT faces may only
     * extract from output slots, DISABLED faces expose nothing.
     */
    public IItemHandler getItemHandler(Direction side) {
        if (side != null && faceMode(side) == FaceMode.DISABLED) {
            return null;
        }
        return new SidedHandler(side);
    }

    // ------------------------------------------------------------------ ticking

    public void tick(Level level) {
        if (level.isClientSide()) {
            return;
        }
        syncTierState();
        // Make sure the optional AE2 grid node exists even before a cable asks for it.
        if (!gridHostAttempted) {
            gridHost();
        }
        process(level);
        if (level.getGameTime() % 5L == 0L) {
            pushOutputs(level);
        }
    }

    private void refreshCaches() {
        Arrays.fill(cachedItems, null);
        Arrays.fill(cachedRecipes, null);
    }

    private void process(Level level) {
        if (voidBuffer <= 0) {
            return;
        }
        voidBuffer -= Math.min(voidBuffer, 3L);
        int total = rate();
        if (total <= 0) {
            return;
        }
        int base = total / VoidStats.FURNACE_SLOTS;
        int extra = total % VoidStats.FURNACE_SLOTS;
        for (int i = 0; i < VoidStats.FURNACE_SLOTS; i++) {
            int slot = (rotation + i) % VoidStats.FURNACE_SLOTS;
            int share = base + (i < extra ? 1 : 0);
            if (share > 0) {
                smelt(level, slot, share);
            }
        }
        rotation = (rotation + 1) % VoidStats.FURNACE_SLOTS;
    }

    private void smelt(Level level, int slot, int max) {
        ItemStack input = inputs.getStackInSlot(slot);
        if (input.isEmpty()) {
            cachedItems[slot] = null;
            cachedRecipes[slot] = null;
            return;
        }
        Item item = input.getItem();
        if (cachedItems[slot] != item) {
            cachedItems[slot] = item;
            cachedRecipes[slot] = level.getRecipeManager()
                    .getRecipeFor(RecipeType.SMELTING, new SingleRecipeInput(input.copyWithCount(1)), level)
                    .orElse(null);
        }
        RecipeHolder<SmeltingRecipe> recipe = cachedRecipes[slot];
        if (recipe == null) {
            return;
        }
        ItemStack result = recipe.value().getResultItem(level.registryAccess());
        if (result.isEmpty()) {
            return;
        }
        int room = outputRoomFor(result);
        int amount = Math.min(max, Math.min(input.getCount(), room));
        if (amount <= 0) {
            return;
        }
        ItemStack extracted = inputs.extractItem(slot, amount, false);
        if (extracted.isEmpty()) {
            return;
        }
        ItemStack leftover = addToOutputs(result.copyWithCount(extracted.getCount()));
        if (!leftover.isEmpty()) {
            // put back whatever could not be stored (defensive; room check should prevent it)
            inputs.insertItem(slot, extracted.copyWithCount(leftover.getCount()), false);
        }
        setChanged();
    }

    private int outputRoomFor(ItemStack result) {
        int cap = capacity();
        long room = 0L;
        for (int i = 0; i < outputs.getSlots(); i++) {
            ItemStack stack = outputs.getStackInSlot(i);
            if (stack.isEmpty()) {
                room += cap;
            } else if (ItemStack.isSameItemSameComponents(stack, result)) {
                room += Math.max(0, cap - stack.getCount());
            }
        }
        return (int) Math.min(Integer.MAX_VALUE, room);
    }

    private ItemStack addToOutputs(ItemStack stack) {
        ItemStack remaining = stack.copy();
        for (int i = 0; i < outputs.getSlots() && !remaining.isEmpty(); i++) {
            ItemStack existing = outputs.getStackInSlot(i);
            if (!existing.isEmpty() && !ItemStack.isSameItemSameComponents(existing, remaining)) {
                continue;
            }
            remaining = outputs.insertItem(i, remaining, false);
        }
        return remaining;
    }

    private void pushOutputs(Level level) {
        int budget = PUSH_BUDGET;
        for (Direction face : Direction.values()) {
            if (budget <= 0) {
                return;
            }
            if (faceMode(face) != FaceMode.OUTPUT) {
                continue;
            }
            BlockPos target = worldPosition.relative(face);
            if (!level.isLoaded(target)) {
                continue;
            }
            IItemHandler handler = level.getCapability(Capabilities.ItemHandler.BLOCK, target, face.getOpposite());
            if (handler == null) {
                continue;
            }
            budget -= pushTo(handler, budget);
        }
        if (wirelessEnabled) {
            pushWireless(level, wirelessBudget());
        }
        if (aeReturn) {
            int aeBudget = wirelessBudget();
            GridHost grid = grid();
            if (grid != null && grid.isOnline()) {
                long moved = grid.pushItems(outputs, aeBudget);
                aeBudget -= (int) Math.min(aeBudget, moved);
            }
            if (aeBudget > 0) {
                pushAe(level, aeBudget);
            }
        }
    }

    /**
     * AE2 return fallback: feeds ME Interfaces physically attached to the furnace (one of the six
     * faces) when the furnace is not itself connected to a grid. Once the furnace is cabled up, the
     * direct grid-node path above feeds the interface's network instead.
     */
    private void pushAe(Level level, int budget) {
        if (!AeReturn.available()) {
            return;
        }
        for (Direction face : Direction.values()) {
            if (budget <= 0) {
                return;
            }
            BlockPos target = worldPosition.relative(face);
            if (!level.isLoaded(target)) {
                continue;
            }
            int moved = AeReturn.push(level, target, face.getOpposite(), outputs, budget);
            if (moved > 0) {
                budget -= moved;
            }
        }
    }

    /** Per-push wireless budget: 5 ticks worth of output, clamped between 4k and 64k items. */
    private int wirelessBudget() {
        long perTick = rate();
        long budget = Math.max(WIRELESS_MIN_BUDGET, perTick * 5L);
        return (int) Math.min(WIRELESS_MAX_BUDGET, budget);
    }

    private int pushTo(IItemHandler handler, int max) {
        int pushed = 0;
        for (int slot = 0; slot < outputs.getSlots() && pushed < max; slot++) {
            ItemStack stack = outputs.getStackInSlot(slot);
            if (stack.isEmpty()) {
                continue;
            }
            int amount = Math.min(stack.getCount(), max - pushed);
            ItemStack probe = stack.copyWithCount(amount);
            ItemStack rest = ItemHandlerHelper.insertItem(handler, probe, false);
            int moved = amount - rest.getCount();
            if (moved > 0) {
                outputs.extractItem(slot, moved, false);
                pushed += moved;
            }
        }
        return pushed;
    }

    private void pushWireless(Level level, int max) {
        List<BlockPos> receivers = VoidPowerNetwork.receivers(level.dimension());
        if (receivers.isEmpty()) {
            return;
        }
        long range = range();
        int checks = Math.min(receivers.size(), WIRELESS_CHECK_LIMIT);
        int pushed = 0;
        for (int i = 0; i < checks && pushed < max; i++) {
            if (receivers.isEmpty()) {
                return;
            }
            int index = (wirelessCursor + i) % receivers.size();
            BlockPos pos = receivers.get(index);
            if (pos.equals(worldPosition) || !level.isLoaded(pos)) {
                continue;
            }
            if (range != Long.MAX_VALUE) {
                double dx = pos.getX() - worldPosition.getX();
                double dy = pos.getY() - worldPosition.getY();
                double dz = pos.getZ() - worldPosition.getZ();
                if (dx * dx + dy * dy + dz * dz > (double) range * (double) range) {
                    continue;
                }
            }
            IItemHandler handler = level.getCapability(Capabilities.ItemHandler.BLOCK, pos, null);
            if (handler == null) {
                continue;
            }
            pushed += pushTo(handler, max - pushed);
        }
        wirelessCursor = (wirelessCursor + 1) % Math.max(1, receivers.size());
    }

    // ------------------------------------------------------------------ AE2 grid host (optional)

    /**
     * Lazily creates the AE2 grid node holder. Only AE2-dependent code is touched through
     * {@link AeBridge}, so the furnace still works when AE2 is not installed.
     */
    public Object gridHost() {
        if (!gridHostAttempted) {
            gridHostAttempted = true;
            gridHost = AeBridge.createHost(this);
        }
        return gridHost;
    }

    public CompoundTag pendingGridTag() {
        return pendingGridTag;
    }

    private GridHost grid() {
        return gridHost instanceof GridHost host ? host : null;
    }

    private void destroyGridHost() {
        if (gridHost instanceof GridHost host) {
            host.destroy();
            gridHost = null;
            gridHostAttempted = false;
        }
    }

    @Override
    public void setRemoved() {
        destroyGridHost();
        super.setRemoved();
    }

    @Override
    public void onChunkUnloaded() {
        destroyGridHost();
        super.onChunkUnloaded();
    }

    // ------------------------------------------------------------------ persistence

    public long addVoid(long amount) {
        long room = com.voidgen.VoidValue.MACHINE_BUFFER - voidBuffer;
        long accepted = Math.min(Math.max(0L, room), Math.max(0L, amount));
        if (accepted > 0) {
            voidBuffer += accepted;
            setChanged();
        }
        return accepted;
    }

    public long voidAmount() {
        return voidBuffer;
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.putInt("Tier", tier);
        tag.putLong("VoidBuffer", voidBuffer);
        tag.putBoolean("Wireless", wirelessEnabled);
        tag.putBoolean("AeReturn", aeReturn);
        byte[] faceBytes = new byte[6];
        for (int i = 0; i < 6; i++) {
            faceBytes[i] = (byte) faces[i].ordinal();
        }
        tag.putByteArray("Faces", faceBytes);
        tag.put("Inputs", inputs.serializeNBT(registries));
        tag.put("Outputs", outputs.serializeNBT(registries));
        tag.put("Cards", cards.serializeNBT(registries));
        if (gridHost instanceof GridHost grid) {
            CompoundTag gridTag = new CompoundTag();
            grid.save(gridTag);
            tag.put("VoidgenGridNode", gridTag);
        }
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        tier = tag.getInt("Tier");
        voidBuffer = tag.getLong("VoidBuffer");
        wirelessEnabled = tag.getBoolean("Wireless");
        aeReturn = tag.getBoolean("AeReturn");
        byte[] faceBytes = tag.getByteArray("Faces");
        for (int i = 0; i < 6 && i < faceBytes.length; i++) {
            int ordinal = faceBytes[i];
            faces[i] = ordinal >= 0 && ordinal < FaceMode.values().length
                    ? FaceMode.values()[ordinal]
                    : FaceMode.INPUT;
        }
        if (tag.contains("Inputs")) {
            inputs.deserializeNBT(registries, tag.getCompound("Inputs"));
        }
        if (tag.contains("Outputs")) {
            outputs.deserializeNBT(registries, tag.getCompound("Outputs"));
        }
        if (tag.contains("Cards")) {
            cards.deserializeNBT(registries, tag.getCompound("Cards"));
        }
        if (tag.contains("VoidgenGridNode")) {
            CompoundTag gridTag = tag.getCompound("VoidgenGridNode");
            if (gridHost instanceof GridHost grid) {
                grid.load(gridTag);
            } else {
                pendingGridTag = gridTag;
            }
        }
        refreshCaches();
    }

    // ------------------------------------------------------------------ menu

    @Override
    public Component getDisplayName() {
        return Component.translatable("block.voidgen.void_furnace");
    }

    @Override
    public AbstractContainerMenu createMenu(int containerId, Inventory inventory, Player player) {
        return new VoidFurnaceMenu(containerId, inventory, this);
    }

    // ------------------------------------------------------------------ sided handler

    private final class SidedHandler implements IItemHandler {
        private final Direction side;

        private SidedHandler(Direction side) {
            this.side = side;
        }

        @Override
        public int getSlots() {
            return inputs.getSlots() + outputs.getSlots();
        }

        @Override
        public ItemStack getStackInSlot(int slot) {
            return slot < inputs.getSlots()
                    ? inputs.getStackInSlot(slot)
                    : outputs.getStackInSlot(slot - inputs.getSlots());
        }

        @Override
        public int getSlotLimit(int slot) {
            return capacity();
        }

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            return slot < inputs.getSlots();
        }

        @Override
        public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
            if (side != null && faceMode(side) != FaceMode.INPUT) {
                return stack;
            }
            if (slot < 0 || slot >= inputs.getSlots()) {
                return stack;
            }
            return inputs.insertItem(slot, stack, simulate);
        }

        @Override
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            if (side != null && faceMode(side) != FaceMode.OUTPUT) {
                return ItemStack.EMPTY;
            }
            int outputSlot = slot - inputs.getSlots();
            if (outputSlot < 0) {
                return ItemStack.EMPTY;
            }
            return outputs.extractItem(outputSlot, amount, simulate);
        }
    }
}
