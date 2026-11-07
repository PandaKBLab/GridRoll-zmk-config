/* SPDX-License-Identifier: MIT */
#include <errno.h>
#include <zephyr/init.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <hal/nrf_power.h>
#include <zmk/activity.h>
#include <zmk/event_manager.h>
#include <zmk/events/activity_state_changed.h>
#if IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
#include <zmk/ble.h>
#include <zmk/endpoints.h>
#include <zmk/usb.h>
#include <zmk/events/ble_active_profile_changed.h>
#include <zmk/events/endpoint_changed.h>
#include <zmk/events/usb_conn_state_changed.h>
#endif
#include "status_policy.h"

static const struct gpio_dt_spec red = GPIO_DT_SPEC_GET(DT_NODELABEL(lowbat_led), gpios);
static struct gr_status status;
static bool ready, pending_sample;
static int pending_error;
static uint8_t pending_percent;
static int64_t pending_at;
K_MUTEX_DEFINE(status_lock);

static void status_work_cb(struct k_work *work);
K_WORK_DELAYABLE_DEFINE(status_work, status_work_cb);

static void refresh_locked(int64_t now) {
    gr_status_activity(&status, zmk_activity_get_state() == ZMK_ACTIVITY_ACTIVE, now);
    /* Read hardware VBUS even on the USB-disabled left peripheral. This does
     * not enable a USB stack or introduce polling while idle. */
    status.usb = nrf_power_usbregstatus_vbusdet_get(NRF_POWER);
#if IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
    bool bt_mode = !zmk_usb_is_hid_ready() ||
                   zmk_endpoint_get_preferred_transport() == ZMK_TRANSPORT_BLE;
    gr_status_link(&status, bt_mode, zmk_ble_active_profile_is_connected(),
                   zmk_ble_active_profile_index(), now);
#endif
}

static void render_locked(int64_t now) {
    struct gr_render r = gr_status_render(&status, now);
    gpio_pin_set_dt(&red, r.on);
    if (r.next < 0) k_work_cancel_delayable(&status_work);
    else k_work_reschedule(&status_work, K_MSEC(MAX(INT64_C(1), r.next - now)));
}
static void status_work_cb(struct k_work *work) {
    k_mutex_lock(&status_lock, K_FOREVER);
    if (ready) {
        int64_t now = k_uptime_get();
        refresh_locked(now);
        render_locked(now);
    }
    k_mutex_unlock(&status_lock);
}

/* Called by the existing ZMK battery fetch, including unchanged/zero SOC and
 * failures. No second ADC reader or cached-SOC freshness timer is created. */
void gridroll_battery_sample_report(int err, uint8_t percent) {
    k_mutex_lock(&status_lock, K_FOREVER);
    int64_t now = k_uptime_get();
    if (!ready) {
        pending_sample = true; pending_error = err; pending_percent = percent; pending_at = now;
    } else {
        refresh_locked(now);
        gr_status_sample(&status, err, percent, now);
        render_locked(now);
    }
    k_mutex_unlock(&status_lock);
}

static int status_event(const zmk_event_t *event) {
    k_mutex_lock(&status_lock, K_FOREVER);
    if (ready) {
        int64_t now = k_uptime_get();
        refresh_locked(now);
        /* Idle/sleep switches the GPIO off synchronously before poweroff. */
        render_locked(now);
    }
    k_mutex_unlock(&status_lock);
    return ZMK_EV_EVENT_BUBBLE;
}
ZMK_LISTENER(gridroll_status, status_event);
ZMK_SUBSCRIPTION(gridroll_status, zmk_activity_state_changed);
#if IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)
ZMK_SUBSCRIPTION(gridroll_status, zmk_ble_active_profile_changed);
ZMK_SUBSCRIPTION(gridroll_status, zmk_endpoint_changed);
ZMK_SUBSCRIPTION(gridroll_status, zmk_usb_conn_state_changed);
#endif

static int status_init(void) {
    if (!device_is_ready(red.port)) return -ENODEV;
    int err = gpio_pin_configure_dt(&red, GPIO_OUTPUT_INACTIVE);
    if (err) return err;
    k_mutex_lock(&status_lock, K_FOREVER);
    gr_status_init(&status, IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL));
    ready = true;
    int64_t now = k_uptime_get();
    refresh_locked(now);
    if (pending_sample) gr_status_sample(&status, pending_error, pending_percent, pending_at);
    render_locked(now);
    k_mutex_unlock(&status_lock);
    return 0;
}
SYS_INIT(status_init, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);
