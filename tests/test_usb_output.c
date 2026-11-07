/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdio.h>
#include "usb_output_policy.h"

int main(void) {
    bool was_ready = false;
    assert(!gridroll_usb_should_select(&was_ready, false, false)); /* battery */
    assert(!gridroll_usb_should_select(&was_ready, false, true));  /* charger */
    assert(gridroll_usb_should_select(&was_ready, true, false));   /* enumerate */
    assert(gridroll_usb_should_select(&was_ready, true, true));    /* saved BLE at boot */
    /* A manual BLE selection must survive repeated configured/resume events. */
    for (int i = 0; i < 100; ++i) {
        assert(!gridroll_usb_should_select(&was_ready, true, false));
    }
    assert(!gridroll_usb_should_select(&was_ready, false, false)); /* unplug */
    assert(!gridroll_usb_should_select(&was_ready, false, false)); /* charger only */
    assert(gridroll_usb_should_select(&was_ready, true, false));   /* reconnect */
    puts("USB output: battery, charger, saved preference, manual BLE, resume and reconnect passed");
    return 0;
}
