/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdio.h>
#include "status_policy.h"
#define CONFIG_GRIDROLL_STATUS_LED 1
#define CONFIG_USB_DEVICE_STACK 0
#define IS_ENABLED(x) (x)
#define LOG_DBG(...) ((void)0)
#define ZMK_ACTIVITY_ACTIVE 0
struct k_work { int unused; };
struct device { int unused; };
static const struct device sensor;
static const struct device *battery=&sensor;
static uint8_t last_state_of_charge, next_charge;
static int state, fetches, next_error, reports;
static int64_t now;
static struct gr_status status;
static bool usb_present;
#define NRF_POWER NULL
static bool nrf_power_usbregstatus_vbusdet_get(const void *reg) { return usb_present; }
#include "usb_power.inc"
static int zmk_activity_get_state(void) { return state; }
static int zmk_battery_update(const struct device *dev) {
    assert(dev==battery); fetches++;
    if (!next_error) last_state_of_charge=next_charge;
    return next_error;
}
void gridroll_battery_sample_report(int err, uint8_t percent) {
    reports++; gr_status_sample(&status,err,percent,now);
}
#include "battery_work.inc"
int main(void) {
    assert(!is_usb_power_present());
    usb_present=true; assert(is_usb_power_present()); /* no left USB stack needed */
    struct k_work work={0};
    gr_status_init(&status,false); gr_status_activity(&status,true,0);
    assert(!status.valid && !gr_status_render(&status,0).on);
    now=100; next_charge=0; zmk_battery_work(&work);
    assert(fetches==1 && reports==1 && status.valid && gr_status_render(&status,100).on);
    now=60100; zmk_battery_work(&work);
    assert(reports==2 && status.sample_at==60100); /* unchanged real 0 remains fresh */
    now=120100; next_error=-5; zmk_battery_work(&work);
    assert(reports==3 && !status.valid && !gr_status_render(&status,now).on);
    next_error=0; next_charge=50; now=180100; zmk_battery_work(&work);
    assert(status.valid && !status.low && status.sample_at==now);
    state=1; now=240100; zmk_battery_work(&work);
    assert(fetches==4 && reports==4); /* queued work cannot start a sample in idle */
    puts("Actual battery callback and hardware USB detection: zero/unchanged SOC, failures, recovery and idle passed");
    return 0;
}
