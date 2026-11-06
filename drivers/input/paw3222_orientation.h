// SPDX-License-Identifier: MIT
#ifndef GRIDROLL_PAW3222_ORIENTATION_H
#define GRIDROLL_PAW3222_ORIENTATION_H

#include <stdint.h>

struct paw3222_motion {
    int16_t x;
    int16_t y;
};

/* GridRoll's installed sensor reports up/left/down/right as -X/+Y/+X/-Y.
 * Correct the mounting before both DYA mouse and scroll processing.
 * Widen before negating so a raw -128 can correctly become +128. */
static inline struct paw3222_motion paw3222_board_motion(int8_t raw_x, int8_t raw_y) {
    return (struct paw3222_motion){.x = -(int16_t)raw_y, .y = (int16_t)raw_x};
}

#endif
