/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

#define ZMK_BEHAVIOR_OPAQUE 0
#define ZMK_INPUT_PROCESSOR_RUNTIME_WRITE_MODE_TEMPORARY 2
struct device { const void *config; void *data; };
struct zmk_behavior_binding { const char *behavior_dev; };
struct zmk_behavior_binding_event { uint32_t position; };
struct zmk_input_processor_runtime_config {
    uint32_t scale_multiplier, scale_divisor;
    int32_t rotation_degrees;
    bool xy_swap_enabled, x_invert, y_invert;
};
static struct device behavior, mouse;
static struct zmk_input_processor_runtime_config normal, live;
static bool missing;
static int set_calls, set_error, get_error;
static const struct device *zmk_behavior_get_binding(const char *name) {
    assert(!strcmp(name, "precision")); return &behavior;
}
static const struct device *zmk_input_processor_runtime_find_by_name(const char *name) {
    assert(!strcmp(name, "mouse")); return missing ? NULL : &mouse;
}
static int zmk_input_processor_runtime_get_config(
    const struct device *dev, const char **name, struct zmk_input_processor_runtime_config *out) {
    assert(dev == &mouse && name == NULL);
    if (get_error) return get_error;
    *out = normal; return 0;
}
static int zmk_input_processor_runtime_set_scaling(
    const struct device *dev, uint32_t multiplier, uint32_t divisor, int mode) {
    /* Temporary calls must not alter normal settings or commit flash writes. */
    assert(dev == &mouse && mode == ZMK_INPUT_PROCESSOR_RUNTIME_WRITE_MODE_TEMPORARY);
    if (set_error) return set_error;
    live.scale_multiplier = multiplier; live.scale_divisor = divisor; set_calls++;
    return 0;
}

#include "precision_functions.inc"

static const struct precision_config config = {.processor_name = "mouse"};
static struct precision_data data;
static struct zmk_behavior_binding binding = {"precision"};
static struct zmk_behavior_binding_event event = {.position = 41};
static void reset(uint32_t multiplier, uint32_t divisor) {
    data.held_positions = 0; behavior.config = &config; behavior.data = &data;
    normal = (struct zmk_input_processor_runtime_config){multiplier, divisor, 37, true, true, false};
    live = normal; missing = false; set_calls = set_error = get_error = 0; event.position = 41;
}
static int press(void) { return precision_pressed(&binding, event); }
static int release(void) { return precision_released(&binding, event); }
static void unchanged_direction(void) {
    assert(live.rotation_degrees == 37 && live.xy_swap_enabled && live.x_invert && !live.y_invert);
}
int main(void) {
    reset(1, 1); assert(!press()); assert(live.scale_multiplier == 1 && live.scale_divisor == 4);
    assert(normal.scale_multiplier == 1 && normal.scale_divisor == 1); unchanged_direction();
    assert(!release()); assert(live.scale_multiplier == 1 && live.scale_divisor == 1);
    assert(!data.held_positions && set_calls == 2); unchanged_direction();

    /* Relative to normal DYA speed, not a fixed absolute override. */
    reset(3, 2); assert(!press()); assert(live.scale_multiplier == 3 && live.scale_divisor == 8);
    assert(!release()); assert(live.scale_multiplier == 3 && live.scale_divisor == 2);
    reset(8, 3); assert(!press()); assert(live.scale_multiplier == 2 && live.scale_divisor == 3);
    assert(!release()); assert(live.scale_multiplier == 8 && live.scale_divisor == 3);

    /* Memory-only or saved DYA baseline edits during the hold survive release. */
    reset(1, 1); assert(!press()); normal.scale_multiplier = 5; normal.scale_divisor = 3;
    assert(!release()); assert(live.scale_multiplier == 5 && live.scale_divisor == 3);
    unchanged_direction();

    /* Duplicate events and a second Studio-assigned key do not divide twice. */
    reset(1, 1); assert(!press()); assert(!press()); assert(set_calls == 1);
    event.position = 37; assert(!press()); assert(set_calls == 1);
    event.position = 41; assert(!release()); assert(set_calls == 1);
    event.position = 37; assert(!release()); assert(set_calls == 2);
    assert(!release()); assert(set_calls == 2 && !data.held_positions);

    /* Invalid state fails before claiming a held key or changing live scaling. */
    reset(1, 1); event.position = 64; assert(press() == -EINVAL && release() == -EINVAL);
    reset(1, 1); missing = true; assert(press() == -ENODEV && !data.held_positions);
    reset(0, 1); assert(press() == -EINVAL && !data.held_positions);
    reset(1, UINT32_MAX); assert(press() == -ERANGE && !data.held_positions);
    reset(1, 1); get_error = -EIO; assert(press() == -EIO && !data.held_positions);
    reset(1, 1); set_error = -EIO; assert(press() == -EIO && !data.held_positions);
    reset(4, UINT32_MAX); assert(!press()); assert(live.scale_divisor == UINT32_MAX);
    assert(!release()); /* reduction avoids a needless denominator overflow */
    puts("Precision: relative quarter speed, release, DYA baseline, direction, multiple keys and errors passed");
    return 0;
}
