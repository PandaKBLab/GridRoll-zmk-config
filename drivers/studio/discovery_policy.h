/* SPDX-License-Identifier: MIT */
#pragma once
#include <stdbool.h>
#include <stdint.h>

struct discovery_state {
    bool connected, ble;
    uint8_t profile;
    int64_t until;
};
struct discovery_result { bool advertise; int64_t next; };

static inline struct discovery_result discovery_update(
    struct discovery_state *s, bool active, bool connected, bool ble, uint8_t profile,
    bool manual, int64_t now) {
    bool fresh = connected && (!s->connected || profile != s->profile || (ble && !s->ble));
    s->connected = connected;
    s->ble = ble;
    s->profile = profile;
    if (!active || !connected || !ble) {
        s->until = 0;
    } else if (fresh || manual) {
        s->until = now + 60000;
    }
    bool advertise = active && connected && ble && now < s->until;
    if (!advertise) {
        s->until = 0;
    }
    return (struct discovery_result){advertise, advertise ? s->until : -1};
}
