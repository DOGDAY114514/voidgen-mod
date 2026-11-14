package net.neoforged.fml.common;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import net.neoforged.api.distmarker.Dist;

/**
 * Compile-only stub of FML's EventBusSubscriber annotation (real class comes from FML).
 * Element signatures mirror FML: no explicit bus element, IModBusEvent subscribers are
 * routed to the mod bus automatically.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface EventBusSubscriber {
    Dist[] value() default {Dist.CLIENT, Dist.DEDICATED_SERVER};

    String modid() default "";
}
