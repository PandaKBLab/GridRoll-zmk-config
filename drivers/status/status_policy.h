/* SPDX-License-Identifier: MIT */
#pragma once
#include <stdbool.h>
#include <stdint.h>
#include <string.h>

#define GR_WAIT_MS 30000
#define GR_WAIT_PERIOD_MS 2000
#define GR_PULSE_MS 100
#define GR_CONNECTED_MS 2000
#define GR_LOW_PERIOD_MS 30000
#define GR_SAMPLE_FRESH_MS 180000 /* max(3 * 60-second sampling, 120 seconds) */

struct gr_status {
    bool central, active, usb, bt_mode, connected, valid, low;
    uint8_t profile;
    int64_t sample_at, wait_end, wait_next, wait_on_end;
    int64_t confirm_end, low_next, low_on_end;
};
struct gr_render { bool on; int64_t next; }; /* next=-1 means no LED work */

static inline void gr_status_init(struct gr_status *s, bool central) {
    memset(s, 0, sizeof(*s));
    s->central = central;
    s->profile = UINT8_MAX;
}
static inline void gr_wait_start(struct gr_status *s, int64_t now) {
    s->wait_end = now + GR_WAIT_MS;
    s->wait_next = now;
    s->wait_on_end = 0;
}
static inline void gr_status_activity(struct gr_status *s, bool active, int64_t now) {
    if (s->active == active) return;
    s->active = active;
    s->valid = false; /* wake waits for a new successful sample */
    s->wait_end = s->wait_on_end = s->confirm_end = s->low_on_end = 0;
    s->low_next = 0;
    if (active && s->central && s->bt_mode) {
        if (s->connected) s->confirm_end = now + GR_CONNECTED_MS;
        else gr_wait_start(s, now);
    }
}
static inline void gr_status_link(struct gr_status *s, bool bt_mode, bool connected,
                                  uint8_t profile, int64_t now) {
    bool changed = bt_mode != s->bt_mode || connected != s->connected || profile != s->profile;
    s->bt_mode = bt_mode;
    s->connected = connected;
    s->profile = profile;
    if (!s->active || !s->central || !bt_mode) {
        s->wait_end = s->wait_on_end = s->confirm_end = 0;
        return;
    }
    if (!changed) return; /* sampling/events never restart a spent window */
    if (connected) {
        s->confirm_end = now + GR_CONNECTED_MS;
        s->wait_end = s->wait_on_end = 0;
    } else {
        s->confirm_end = 0;
        gr_wait_start(s, now);
    }
}
static inline void gr_status_sample(struct gr_status *s, int err, uint8_t percent,
                                    int64_t now) {
    if (!s->active || err || percent > 100) {
        s->valid = false;
        s->low_on_end = 0;
        return;
    }
    s->valid = true;
    s->sample_at = now; /* only a real successful fetch refreshes this */
    if (percent <= 15 && !s->low) {
        s->low = true;
        s->low_next = now;
    } else if (percent >= 20) {
        s->low = false;
        s->low_on_end = 0;
    }
}
static inline int64_t gr_min(int64_t a, int64_t b) { return a < b ? a : b; }
static inline struct gr_render gr_status_render(struct gr_status *s, int64_t now) {
    struct gr_render r = {.on = false, .next = -1};
    if (!s->active) return r;
    /* The short successful-connection indication is not swallowed by low battery. */
    if (s->central && s->bt_mode && s->connected && now < s->confirm_end) {
        r.on = true; r.next = s->confirm_end; return r;
    }
    bool fresh = s->valid && now >= s->sample_at &&
                 now - s->sample_at < GR_SAMPLE_FRESH_MS;
    if (!s->usb && fresh && s->low) {
        if (now >= s->low_on_end && now >= s->low_next) {
            s->low_on_end = now + GR_PULSE_MS;
            s->low_next = now + GR_LOW_PERIOD_MS;
        }
        r.on = now < s->low_on_end;
        r.next = gr_min(r.on ? s->low_on_end : s->low_next,
                        s->sample_at + GR_SAMPLE_FRESH_MS);
        return r; /* low-battery pattern suppresses waiting flashes */
    }
    if (s->central && s->bt_mode && !s->connected && now < s->wait_end) {
        if (now >= s->wait_on_end && now >= s->wait_next) {
            s->wait_on_end = now + GR_PULSE_MS;
            s->wait_next = now + GR_WAIT_PERIOD_MS;
        }
        r.on = now < s->wait_on_end;
        r.next = gr_min(r.on ? s->wait_on_end : s->wait_next, s->wait_end);
    }
    return r;
}
