/* SPDX-License-Identifier: MIT */
#define DT_DRV_COMPAT gridroll_behavior_wheel_step
#include <zephyr/device.h>
#include <zephyr/input/input.h>
#include <drivers/behavior.h>
#include <zmk/behavior.h>
#include <zmk/pointing/input_processor_runtime.h>

struct wheel_config { uint16_t code; int32_t step; };

static int pressed(struct zmk_behavior_binding *binding,
                   struct zmk_behavior_binding_event event) {
    const struct device *dev = zmk_behavior_get_binding(binding->behavior_dev);
    const struct wheel_config *cfg = dev->config;
    const struct device *mouse = zmk_input_processor_runtime_find_by_name("mouse");
    if (mouse) {
        zmk_input_processor_runtime_note_activity(mouse);
    }
    return input_report_rel(dev, cfg->code, cfg->step, true, K_NO_WAIT);
}

static int released(struct zmk_behavior_binding *binding,
                    struct zmk_behavior_binding_event event) {
    return ZMK_BEHAVIOR_OPAQUE;
}

#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
static const struct behavior_parameter_metadata metadata = {.sets_len = 0, .sets = NULL};
#endif
static const struct behavior_driver_api wheel_api = {
    .binding_pressed = pressed, .binding_released = released,
#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
    .parameter_metadata = &metadata,
#endif
};
#define WHEEL_INST(n)                                                                               \
    static const struct wheel_config wheel_config_##n = {                                          \
        .code = DT_INST_PROP(n, input_code), .step = (int32_t)DT_INST_PROP(n, step)};                \
    BEHAVIOR_DT_INST_DEFINE(n, NULL, NULL, NULL, &wheel_config_##n, POST_KERNEL,                    \
                            CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &wheel_api);
DT_INST_FOREACH_STATUS_OKAY(WHEEL_INST)
