/* SPDX-License-Identifier: MIT */
#define DT_DRV_COMPAT gridroll_behavior_studio_ble
#include <zephyr/device.h>
#include <zephyr/kernel.h>
#include <zephyr/sys/atomic.h>
#include <zephyr/logging/log.h>
#include <drivers/behavior.h>
#include <zmk/behavior.h>
#include <zmk/activity.h>
#include <zmk/ble.h>
#include <zmk/endpoints.h>
#include <zmk/usb.h>
#include <zmk/event_manager.h>
#include <zmk/events/activity_state_changed.h>
#include <zmk/events/ble_active_profile_changed.h>
#include <zmk/events/endpoint_changed.h>
#include "discovery_policy.h"

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);
static struct discovery_state state;
static atomic_t generation, manual_requested;
static bool last_requested, retry_pending;
static unsigned int retries;
static void update_window(struct k_work *work);
static K_WORK_DELAYABLE_DEFINE(window_work, update_window);

static void request_update(void) {
    atomic_inc(&generation);
    k_work_reschedule(&window_work, K_NO_WAIT);
}

static void update_window(struct k_work *work) {
    atomic_val_t observed = atomic_get(&generation);
    int64_t now = k_uptime_get();
    bool ble = !zmk_usb_is_hid_ready() ||
               zmk_endpoint_get_preferred_transport() == ZMK_TRANSPORT_BLE;
    struct discovery_result result = discovery_update(
        &state, zmk_activity_get_state() == ZMK_ACTIVITY_ACTIVE,
        zmk_ble_active_profile_is_connected(), ble, zmk_ble_active_profile_index(),
        atomic_set(&manual_requested, 0) != 0, now);
    int64_t next = result.next;
    if (result.advertise != last_requested || retry_pending) {
        if (result.advertise != last_requested) {
            retries = 0;
        }
        /* The native API changes its flag before updating advertising, even
         * if that update fails. Remember the request so expiry always closes it. */
        last_requested = result.advertise;
        int ret = zmk_ble_set_directed_advertising(result.advertise);
        retry_pending = false;
        if (ret < 0) {
            LOG_WRN("Studio discovery update failed: %d", ret);
            /* Bounded retry only; never create an idle polling loop. */
            retry_pending = retries++ < 3;
            if (retry_pending && (next < 0 || next > now + 250)) {
                next = now + 250;
            }
        } else {
            retries = 0;
        }
    }
    if (next >= 0) {
        k_work_reschedule(&window_work, K_MSEC(next > now ? next - now : 0));
    } else {
        k_work_cancel_delayable(&window_work);
    }
    /* An event arriving during the native BLE call must win over the deadline. */
    if (atomic_get(&generation) != observed) {
        k_work_reschedule(&window_work, K_NO_WAIT);
    }
}

static int discovery_listener(const zmk_event_t *event) {
    request_update();
    return ZMK_EV_EVENT_BUBBLE;
}
ZMK_LISTENER(gridroll_studio_discovery, discovery_listener);
ZMK_SUBSCRIPTION(gridroll_studio_discovery, zmk_activity_state_changed);
ZMK_SUBSCRIPTION(gridroll_studio_discovery, zmk_ble_active_profile_changed);
ZMK_SUBSCRIPTION(gridroll_studio_discovery, zmk_endpoint_changed);

static int pressed(struct zmk_behavior_binding *binding,
                   struct zmk_behavior_binding_event event) {
    atomic_set(&manual_requested, 1);
    request_update();
    return ZMK_BEHAVIOR_OPAQUE;
}
static int released(struct zmk_behavior_binding *binding,
                    struct zmk_behavior_binding_event event) {
    return ZMK_BEHAVIOR_OPAQUE;
}
#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
static const struct behavior_parameter_metadata metadata = {.sets_len = 0, .sets = NULL};
#endif
static const struct behavior_driver_api api = {
    .binding_pressed = pressed, .binding_released = released,
#if IS_ENABLED(CONFIG_ZMK_BEHAVIOR_METADATA)
    .parameter_metadata = &metadata,
#endif
};
#define DISCOVERY_INST(n)                                                                           \
    BEHAVIOR_DT_INST_DEFINE(n, NULL, NULL, NULL, NULL, POST_KERNEL,                                \
                            CONFIG_KERNEL_INIT_PRIORITY_DEFAULT, &api);
DT_INST_FOREACH_STATUS_OKAY(DISCOVERY_INST)
