/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdio.h>
#include "discovery_policy.h"

int main(void) {
    struct discovery_state s = {0};
    struct discovery_result r;
    /* Existing host connection can be discovered, without an unlock event. */
    r = discovery_update(&s, true, true, true, 0, false, 1000);
    assert(r.advertise && r.next == 61000);
    r = discovery_update(&s, true, true, true, 0, false, 60000);
    assert(r.advertise && r.next == 61000); /* input/events do not extend it */
    r = discovery_update(&s, true, true, true, 0, false, 61000);
    assert(!r.advertise && r.next == -1);
    r = discovery_update(&s, true, true, true, 0, false, 70000);
    assert(!r.advertise && r.next == -1); /* no idle polling/reopen loop */
    r = discovery_update(&s, true, true, true, 0, true, 80000);
    assert(r.advertise && r.next == 140000); /* explicit discover key */
    r = discovery_update(&s, false, true, true, 0, false, 81000);
    assert(!r.advertise && r.next == -1); /* idle closes immediately */
    r = discovery_update(&s, true, true, true, 0, false, 82000);
    assert(!r.advertise); /* routine movement after idle does not advertise */
    r = discovery_update(&s, true, true, false, 0, true, 83000);
    assert(!r.advertise); /* USB output cannot start a background BLE window */
    r = discovery_update(&s, true, true, true, 0, false, 84000);
    assert(r.advertise && r.next == 144000); /* deliberate output selection */
    r = discovery_update(&s, true, false, true, 0, false, 85000);
    assert(!r.advertise && r.next == -1);
    r = discovery_update(&s, true, true, true, 0, false, 86000);
    assert(r.advertise && r.next == 146000); /* host reconnect */
    r = discovery_update(&s, true, true, true, 1, false, 87000);
    assert(r.advertise && r.next == 147000); /* another selected host */
    r = discovery_update(&s, false, true, true, 1, true, 88000);
    assert(!r.advertise && r.next == -1); /* manual request cannot fake activity */
    puts("Studio discovery: bounded connected-host window, manual renewal, USB/idle/expiry and no idle reopen passed");
    return 0;
}
