package com.voidgen.ae;

import com.voidgen.VoidGen;

import java.util.EnumSet;
import java.util.Set;

import appeng.api.orientation.BlockOrientation;
import appeng.api.stacks.AEItemKey;
import appeng.blockentity.crafting.PatternProviderBlockEntity;
import appeng.helpers.patternprovider.PatternProviderLogic;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.state.BlockState;

/** Pattern provider block entity backed by {@link VoidAssemblerLogic}. */
public class VoidAssemblerBlockEntity extends PatternProviderBlockEntity {
    public VoidAssemblerBlockEntity(BlockPos pos, BlockState state) {
        super(AeAssembler.BE.get(), pos, state);
    }

    @Override
    protected PatternProviderLogic createLogic() {
        return new VoidAssemblerLogic(getMainNode(), this);
    }

    // Our block has no PUSH_DIRECTION state property, so the base implementation
    // (which reads it from the block state) would throw. We never push to machines.
    @Override
    public Set<Direction> getGridConnectableSides(BlockOrientation orientation) {
        return EnumSet.allOf(Direction.class);
    }

    @Override
    public EnumSet<Direction> getTargets() {
        return EnumSet.noneOf(Direction.class);
    }

    @Override
    public ItemStack getMainMenuIcon() {
        return new ItemStack(VoidGen.VOID_ASSEMBLER_ITEM.get());
    }

    @Override
    public AEItemKey getTerminalIcon() {
        return AEItemKey.of(getMainMenuIcon());
    }
}
