/* SPDX-License-Identifier: MIT */
#include <zephyr/settings/settings.h>
#include <zmk/endpoints.h>
#include <zmk/event_manager.h>
#include <zmk/events/usb_conn_state_changed.h>
#include <zmk/usb.h>
#include "usb_output_policy.h"

static bool was_hid_ready;

static int apply_usb_preference(bool settings_commit) {
    if (gridroll_usb_should_select(&was_hid_ready, zmk_usb_is_hid_ready(),
                                  settings_commit)) {
        return zmk_endpoint_set_preferred_transport(ZMK_TRANSPORT_USB);
    }
    return 0;
}

static int usb_output_listener(const zmk_event_t *event) {
    apply_usb_preference(false);
    return ZMK_EV_EVENT_BUBBLE;
}

ZMK_LISTENER(gridroll_usb_output, usb_output_listener);
ZMK_SUBSCRIPTION(gridroll_usb_output, zmk_usb_conn_state_changed);

#if IS_ENABLED(CONFIG_SETTINGS)
/* ZMK loads settings in main(), after SYS_INIT. Run after all stored values
 * have been read, rather than racing that load with a boot-time timer. */
static int usb_output_settings_commit(void) {
    return apply_usb_preference(true);
}
SETTINGS_STATIC_HANDLER_DEFINE(gridroll_usb_output, "gridroll_usb_output", NULL, NULL,
                               usb_output_settings_commit, NULL);
#endif
