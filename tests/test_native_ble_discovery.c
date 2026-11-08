/* SPDX-License-Identifier: MIT */
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#define LOG_DBG(...) ((void)0)
typedef int bt_addr_le_t;
struct bt_conn { int dummy; };
static bool open_profile, connected_profile, directed_advertising_enabled;
static int starts, stops;
enum advertising_type { ZMK_ADV_NONE, ZMK_ADV_DIR, ZMK_ADV_CONN } advertising_status;
#define CURR_ADV(adv) ((adv) << 4)
static bool zmk_ble_active_profile_is_open(void) { return open_profile; }
static bool zmk_ble_active_profile_is_connected(void) { return connected_profile; }
#define CHECKED_ADV_STOP() do { err = 0; if (err) return err; stops++; advertising_status = ZMK_ADV_NONE; } while (0)
#define CHECKED_DIR_ADV() do { addr = NULL; conn = NULL; (void)addr; (void)conn; \
    assert(!"directed mode must not replace normal scannable discovery"); } while (0)
#define CHECKED_OPEN_ADV() do { err = 0; if (err) return err; starts++; advertising_status = ZMK_ADV_CONN; } while (0)
#include "native_ble_functions.inc"

int main(void) {
    connected_profile = true;
    assert(!update_advertising());
    assert(!starts && advertising_status == ZMK_ADV_NONE); /* previous failure */
    assert(!zmk_ble_set_directed_advertising(true));
    assert(starts == 1 && advertising_status == ZMK_ADV_CONN);
    assert(!update_advertising() && starts == 1); /* does not restart per event */
    assert(!zmk_ble_set_directed_advertising(false));
    assert(stops == 1 && advertising_status == ZMK_ADV_NONE);
    connected_profile = false;
    assert(!update_advertising() && starts == 2);
    assert(!zmk_ble_set_directed_advertising(false));
    assert(advertising_status == ZMK_ADV_CONN); /* normal reconnect stays available */
    open_profile = true;
    assert(!update_advertising() && starts == 2); /* ordinary pairing unchanged */
    puts("Actual native BLE advertising: connected-host window and ordinary pairing/reconnect passed");
    return 0;
}
