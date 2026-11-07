// SPDX-License-Identifier: MIT
#ifndef GRIDROLL_PAW3222_BATCH_H
#define GRIDROLL_PAW3222_BATCH_H

#include <stdbool.h>
#include <stdint.h>
#include <limits.h>

/* Keep displacement while limiting BLE report production. Sensor reads and USB
 * reports remain immediate. An accepted X event must not be queued twice if the
 * synchronized Y event temporarily fails to enter Zephyr's input queue. */
struct paw3222_batch {
    int32_t x, y;
    int16_t frame_x, frame_y;
    int64_t last_report_ms;
    int64_t retry_after_ms;
    unsigned int failures;
    bool sent, staged, x_queued;
};

typedef int (*paw3222_batch_sink)(void *ctx, bool y_axis, int16_t value);

static inline int32_t paw3222_batch_bound(int64_t value) {
    return value > INT32_MAX ? INT32_MAX : value < INT32_MIN ? INT32_MIN : (int32_t)value;
}

static inline int16_t paw3222_batch_axis(int32_t value) {
    return value > INT16_MAX ? INT16_MAX : value < INT16_MIN ? INT16_MIN : (int16_t)value;
}

static inline void paw3222_batch_add(struct paw3222_batch *batch, int16_t x, int16_t y) {
    batch->x = paw3222_batch_bound((int64_t)batch->x + x);
    batch->y = paw3222_batch_bound((int64_t)batch->y + y);
}

static inline bool paw3222_batch_pending(const struct paw3222_batch *batch) {
    return batch->staged || batch->x != 0 || batch->y != 0;
}

static inline unsigned int paw3222_batch_delay(const struct paw3222_batch *batch,
                                              int64_t now_ms, unsigned int interval_ms) {
    int64_t remaining = batch->sent && interval_ms
                            ? interval_ms - (now_ms - batch->last_report_ms) : 0;
    int64_t retry = batch->retry_after_ms - now_ms;
    if (retry > remaining) remaining = retry;
    return remaining > 0 ? (unsigned int)remaining : 0;
}

static inline int paw3222_batch_retry(struct paw3222_batch *batch, int64_t now_ms, int rc) {
    if (batch->failures < 5) batch->failures++;
    batch->retry_after_ms = now_ms + (1U << batch->failures); /* 2..32 ms */
    return rc;
}

/* Returns 1 for one completed frame, 0 if nothing is due, or the sink error.
 * The first frame after inactivity is immediate; no empty reports are emitted. */
static inline int paw3222_batch_flush(struct paw3222_batch *batch, int64_t now_ms,
                                     unsigned int interval_ms, paw3222_batch_sink sink,
                                     void *ctx) {
    if (!paw3222_batch_pending(batch) || paw3222_batch_delay(batch, now_ms, interval_ms))
        return 0;
    if (!batch->staged) {
        batch->frame_x = paw3222_batch_axis(batch->x);
        batch->frame_y = paw3222_batch_axis(batch->y);
        batch->staged = true;
    }
    if (!batch->x_queued) {
        int rc = sink(ctx, false, batch->frame_x);
        if (rc < 0) return paw3222_batch_retry(batch, now_ms, rc);
        batch->x_queued = true;
    }
    int rc = sink(ctx, true, batch->frame_y);
    if (rc < 0) return paw3222_batch_retry(batch, now_ms, rc);
    batch->x = paw3222_batch_bound((int64_t)batch->x - batch->frame_x);
    batch->y = paw3222_batch_bound((int64_t)batch->y - batch->frame_y);
    batch->staged = batch->x_queued = false;
    batch->sent = true;
    batch->failures = 0;
    batch->retry_after_ms = 0;
    batch->last_report_ms = now_ms;
    return 1;
}

#endif
