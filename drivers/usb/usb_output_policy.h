/* SPDX-License-Identifier: MIT */
#pragma once
#include <stdbool.h>

/* A USB resume must not undo a manual BLE choice during the same connection.
 * Settings commit is special: a saved BLE preference may have just replaced
 * the startup USB preference, even if USB enumerated before settings loaded. */
static inline bool gridroll_usb_should_select(bool *was_ready, bool ready,
                                              bool settings_commit) {
    bool select = ready && (settings_commit || !*was_ready);
    *was_ready = ready;
    return select;
}
