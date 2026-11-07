# Third-party notices

- ZMK: MIT, https://github.com/cormoran/zmk (fork of zmkfirmware/zmk).
- Zephyr: Apache-2.0, https://github.com/zmkfirmware/zephyr.
- Runtime input processor / custom settings: MIT, https://github.com/cormoran.
- Runtime sensor rotate: MIT, https://github.com/cormoran/zmk-behavior-runtime-sensor-rotate.
- Default layer assignments reference keyfreaks/zmk-config-LiNEA40,
  config/LiNEA40.keymap at 6953ccb2e2d6256ed57887fde692bcb1959f9052;
  adapted to GridRoll's 47 positions with an additional System layer.
- Adafruit nRF52 Bootloader: MIT; its dependencies retain their respective licenses.
- Nordic S140 6.1.1 / MBR: retain the Nordic license supplied with upstream binaries.
- PAW3222 register names and initialization were informed by sekigon-gonnoc/zmk-driver-paw3222,
  itself derived from Zephyr input_paw32xx.c (Copyright 2024 Google LLC;
  modifications Copyright 2025 sekigon-gonnoc, Apache-2.0).
  GridRoll's GPIO transport and sensor adapter are new implementations under MIT.

Original upstream license files are included with first-flash build artifacts.
The private repository visibility does not change these license obligations.
