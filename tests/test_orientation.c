// SPDX-License-Identifier: MIT
#include <assert.h>
#include <stdio.h>
#include "paw3222_orientation.h"

int main(void) {
    /* Raw vectors reproduce the four physical directions reported on the board.
     * HID screen coordinates are +X right and +Y down. */
    const struct {
        int8_t raw_x, raw_y;
        int16_t screen_x, screen_y;
    } cases[] = {
        {-20, 0, 0, -20},   /* up */
        {20, 0, 0, 20},     /* down */
        {0, 20, -20, 0},    /* left */
        {0, -20, 20, 0},    /* right */
        {-11, -7, 7, -11},  /* diagonal */
        {0, 0, 0, 0},
        {-128, -128, 128, -128},
        {127, 127, -127, 127},
    };
    for (unsigned int i = 0; i < sizeof(cases) / sizeof(cases[0]); i++) {
        const struct paw3222_motion motion =
            paw3222_board_motion(cases[i].raw_x, cases[i].raw_y);
        assert(motion.x == cases[i].screen_x);
        assert(motion.y == cases[i].screen_y);
    }
    puts("PAW3222 board orientation: all directions and signed limits passed");
    return 0;
}
