// SPDX-License-Identifier: MIT
#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include "paw3222_batch.h"

struct recorder {
    int calls, fail_on, frames;
    bool fail_all;
    int64_t x, y;
};

static int record(void *ctx, bool y_axis, int16_t value) {
    struct recorder *r = ctx;
    if (++r->calls == r->fail_on || r->fail_all) return -EAGAIN;
    if (y_axis) { r->y += value; r->frames++; }
    else r->x += value;
    return 0;
}

int main(void) {
    struct paw3222_batch b = {0};
    struct recorder r = {0};
    /* A 1 kHz producer must not become a 1 kHz BLE report stream. Preserve
     * total travel, including the final sample after the sensor goes idle. */
    for (int t = 0; t < 1000; t++) {
        paw3222_batch_add(&b, 1, -2);
        paw3222_batch_flush(&b, t, 8, record, &r);
    }
    assert(r.frames == 125 && paw3222_batch_pending(&b));
    assert(paw3222_batch_delay(&b, 999, 8) == 1);
    assert(paw3222_batch_flush(&b, 1000, 8, record, &r) == 1);
    assert(r.x == 1000 && r.y == -2000 && !paw3222_batch_pending(&b));
    int frames = r.frames;
    for (int t = 1001; t < 4000; t++)
        assert(paw3222_batch_flush(&b, t, 8, record, &r) == 0);
    assert(r.frames == frames);
    paw3222_batch_add(&b, -3, 4);
    assert(paw3222_batch_flush(&b, 5000, 8, record, &r) == 1);
    assert(r.x == 997 && r.y == -1996); /* no delay on first motion after idle */

    /* USB bypasses pacing, even immediately after a BLE report. */
    for (int i = 0; i < 100; i++) {
        paw3222_batch_add(&b, 1, 1);
        assert(paw3222_batch_flush(&b, 5000, 0, record, &r) == 1);
    }
    assert(r.x == 1097 && r.y == -1896);

    /* Input queue backpressure must neither duplicate X nor lose the Y sync.
     * New samples received between the two accepted axes stay for next frame. */
    b = (struct paw3222_batch){0}; r = (struct recorder){.fail_on = 2};
    paw3222_batch_add(&b, 5, -6);
    assert(paw3222_batch_flush(&b, 0, 8, record, &r) == -EAGAIN);
    assert(r.x == 5 && r.y == 0 && r.calls == 2);
    paw3222_batch_add(&b, 7, 8);
    assert(paw3222_batch_flush(&b, 1, 8, record, &r) == 0);
    assert(paw3222_batch_flush(&b, 2, 8, record, &r) == 1);
    assert(r.x == 5 && r.y == -6 && r.calls == 3);
    assert(paw3222_batch_flush(&b, 10, 8, record, &r) == 1);
    assert(r.x == 12 && r.y == 2 && !paw3222_batch_pending(&b));

    b = (struct paw3222_batch){0}; r = (struct recorder){.fail_on = 1};
    paw3222_batch_add(&b, -128, 128);
    assert(paw3222_batch_flush(&b, 0, 8, record, &r) == -EAGAIN);
    assert(r.x == 0 && r.y == 0);
    assert(paw3222_batch_flush(&b, 1, 8, record, &r) == 0);
    assert(paw3222_batch_flush(&b, 2, 8, record, &r) == 1);
    assert(r.x == -128 && r.y == 128);

    /* Large backlog is split into valid int16 frames without losing travel. */
    b = (struct paw3222_batch){0}; r = (struct recorder){0};
    for (int i = 0; i < 600; i++) paw3222_batch_add(&b, 128, -128);
    for (int t = 0; paw3222_batch_pending(&b); t += 8)
        assert(paw3222_batch_flush(&b, t, 8, record, &r) == 1);
    assert(r.x == 76800 && r.y == -76800 && r.frames == 3);
    b = (struct paw3222_batch){0}; r = (struct recorder){0};
    paw3222_batch_add(&b, 127, -128);
    paw3222_batch_add(&b, -127, 128);
    assert(!paw3222_batch_pending(&b));
    assert(paw3222_batch_flush(&b, 0, 8, record, &r) == 0 && r.calls == 0);
    assert(paw3222_batch_bound((int64_t)INT32_MAX + 1) == INT32_MAX);
    assert(paw3222_batch_bound((int64_t)INT32_MIN - 1) == INT32_MIN);

    /* Continuous producer calls must also honor retry backoff, rather than
     * bypass it between report-timer retries and spin at the sensor IRQ rate. */
    b = (struct paw3222_batch){0}; r = (struct recorder){.fail_all = true};
    for (int t = 0; t < 100; t++) {
        paw3222_batch_add(&b, 1, -1);
        paw3222_batch_flush(&b, t, 0, record, &r);
    }
    assert(r.calls <= 8 && r.frames == 0 && paw3222_batch_pending(&b));
    assert(paw3222_batch_delay(&b, 100, 0) <= 32);
    r.fail_all = false;
    for (int t = 100; t < 150 && paw3222_batch_pending(&b); t++)
        paw3222_batch_flush(&b, t, 0, record, &r);
    assert(!paw3222_batch_pending(&b) && r.x == 100 && r.y == -100);
    assert(b.failures == 0 && b.retry_after_ms == 0);
    puts("BLE batching: pacing, travel, tail, USB, bounded retry and recovery passed");
    return 0;
}
