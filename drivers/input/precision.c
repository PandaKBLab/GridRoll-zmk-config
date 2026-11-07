/* SPDX-License-Identifier: MIT */
#define DT_DRV_COMPAT gridroll_behavior_precision
#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <zephyr/device.h>
#include <drivers/behavior.h>
#include <zmk/behavior.h>
#include <zmk/pointing/input_processor_runtime.h>

struct precision_config { const char *processor_name; };
struct precision_data { uint64_t held_positions; };

static int precision_apply(const struct device *dev, bool slow) {
    const struct precision_config *cfg = dev->config;
    const struct device *mouse = zmk_input_processor_runtime_find_by_name(cfg->processor_name);
    if (!mouse) {
        return -ENODEV;
    }
    struct zmk_input_processor_runtime_config normal;
    /* The pinned API returns the normal RAM baseline, not a temporary override.
     * It includes both saved and memory-only DYA edits. Never restore every
     * processor setting: this behavior owns scaling only, not rotation/scroll. */
    int ret = zmk_input_processor_runtime_get_config(mouse, NULL, &normal);
    if (ret < 0) {
        return ret;
    }
    uint32_t multiplier = normal.scale_multiplier, divisor = normal.scale_divisor;
    if (!multiplier || !divisor) {
        return -EINVAL;
    }
    if (slow) {
        /* Reduce before multiplying the denominator to avoid overflow. */
        uint32_t cancel = multiplier % 4 == 0 ? 4 : (multiplier % 2 == 0 ? 2 : 1);
        multiplier /= cancel;
        if (divisor > UINT32_MAX / (4 / cancel)) {
            return -ERANGE;
        }
        divisor *= 4 / cancel;
    }
    return zmk_input_processor_runtime_set_scaling(
        mouse, multiplier, divisor, ZMK_INPUT_PROCESSOR_RUNTIME_WRITE_MODE_TEMPORARY);
}

static int precision_pressed(struct zmk_behavior_binding *binding,
                             struct zmk_behavior_binding_event event) {
    const struct device *dev = zmk_behavior_get_binding(binding->behavior_dev);
    struct precision_data *data = dev->data;
    if (event.position >= 64) {
        return -EINVAL;
    }
    uint64_t bit = UINT64_C(1) << event.position;
    if (!data->held_positions) {
        int ret = precision_apply(dev, true);
        if (ret < 0) {
            return ret;
        }
    }
    data->held_positions |= bit;
    return ZMK_BEHAVIOR_OPAQUE;
}

static int precision_released(struct zmk_behavior_binding *binding,
                              struct zmk_behavior_binding_event event) {
    const struct device *dev = zmk_behavior_get_binding(binding->behavior_dev);
    struct precision_data *data = dev->data;
    if (event.position >= 64) {
        return -EINVAL;
    }
    uint64_t bit = UINT64_C(1) << event.position;
    if (!(data->held_positions & bit)) {
        return ZMK_BEHAVIOR_OPAQUE;
    }
    if (data->held_positions == bit) {
        int ret = precision_apply(dev, false);
        if (ret < 0) {
            return ret;
        }
    }
    data->held_positions &= ~bit;
    return ZMK_BEHAVIOR_OPAQUE;
}

#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
static const struct behavior_parameter_metadata metadata = {.sets_len = 0, .sets = NULL};
#endif
static const struct behavior_driver_api precision_api = {
    .binding_pressed = precision_pressed, .binding_released = precision_released,
#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
    .parameter_metadata = &metadata,
#endif
};
#define PRECISION_INST(n)                                                                           \
    static struct precision_data precision_data_##n;                                               \
    static const struct precision_config precision_config_##n = {                                 \
        .processor_name = DT_INST_PROP(n, processor_name)};                                        \
    BEHAVIOR_DT_INST_DEFINE(n, NULL, NULL, &precision_data_##n, &precision_config_##n,               \
                            POST_KERNEL, CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &precision_api);
DT_INST_FOREACH_STATUS_OKAY(PRECISION_INST)
