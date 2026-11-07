# GridRoll

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Deutsch](README.de.md)

ZMK firmware for the PandaKB GridRoll split keyboard: 47 keys, a left encoder, a right PAW3222 trackball, USB/Bluetooth, ZMK Studio and DYA Studio.

The **right half is the central** and connects to your computer; the left half connects wirelessly to it. The keyboard, Bluetooth and USB product name is **GridRoll**.

This repository contains firmware, build tools and user documentation. It does not distribute PCB projects, schematics, routing, netlists or internal circuit documents. Firmware-required GPIO definitions remain in the board source.

## Download and flash

1. Open [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) and select a successful run.
2. Download the single **GridRoll-firmware** ZIP. It contains exactly three files: **GridRoll-left.uf2**, **GridRoll-right.uf2** and **GridRoll-settings-reset.uf2**.
3. Enter each half's bootloader and copy GridRoll-left.uf2 to the left, GridRoll-right.uf2 to the right. A settings-reset image is not normal keyboard firmware.
4. Controllers without the GridRoll bootloader first need the [first-flash procedure](docs/first-flash.md). Bootloader packages are built separately and are not included in this download.

Artifacts are retained for 30 days. A successful build is software validation, not a hardware test.

## Bluetooth and Studio

Pair your computer with **GridRoll on the right half**. If it is invisible, select an unused Bluetooth profile or clear the selected profile and forget the old pairing on your computer. Normal updates preserve saved bonds.

With the stock keymap, hold the **top-left Tab** key to enter System: top-row **Q** selects profile 0, **Backspace** clears it, **Y** selects USB and **U** selects BLE. A newly enumerated right USB connection automatically selects USB, even with a saved BLE preference. Charge-only connections do not force USB; unplugging falls back to a connected BLE host. You can manually select BLE until the next USB connection. Saved layouts may differ.

For [ZMK Studio](https://zmk.studio/) or [DYA Studio](https://studio.dya.cormoran.works/), connect the **right half by USB**, select USB output and choose its serial port. **Studio editing is unlocked by default: no unlock key is required, and idle or disconnect does not relock it.** Close other pages using the same serial port and save your changes. Updates preserve Studio/DYA settings. If you previously compensated the trackball rotation in DYA, remove that extra compensation: mounting correction runs before both pointer and scroll processing.

Both interfaces support keymap editing; DYA also exposes mouse/scroll settings and **per-layer encoder clockwise/counter-clockwise bindings** through `cormoran_rsr`. Base rotation defaults to mouse-wheel scrolling: clockwise down, counter-clockwise up. CI checks all three pinned DYA extension protocols and the compiled unlocked configuration. Sensor imaging and other unimplemented hardware features are not included.

## Eight default layers

Seven layers are adapted from the [LiNEA40 reference](https://github.com/keyfreaks/zmk-config-LiNEA40/blob/6953ccb2e2d6256ed57887fde692bcb1959f9052/config/LiNEA40.keymap), plus GridRoll's System layer. All eight are enabled. See [every exact binding, layer access, encoder defaults and combos](docs/keymap.md). Diagrams are generated from source and checked by CI.

**Normal updates preserve Studio-saved layouts.** To adopt these defaults, export your old layout and use Studio's restore-defaults operation; do not flash settings-reset just to change keymaps. Japanese-layout symbol codes from the reference are retained; actual characters depend on the computer's keyboard layout.

### L0 Base

![L0 Base](docs/keymap/layer-0.svg)

### L1 Mouse

![L1 Mouse](docs/keymap/layer-1.svg)

### L2 Symbol

![L2 Symbol](docs/keymap/layer-2.svg)

### L3 Navigation

![L3 Navigation](docs/keymap/layer-3.svg)

### L4 Function

![L4 Function](docs/keymap/layer-4.svg)

### L5 Scroll

![L5 Scroll](docs/keymap/layer-5.svg)

### L6 Wireless

![L6 Wireless](docs/keymap/layer-6.svg)

### L7 System

![L7 System](docs/keymap/layer-7.svg)

## Power and wake

- **30 seconds** without input: idle, with Bluetooth available.
- **15 minutes** without input on battery: deep sleep. Press a key on each sleeping half to wake it; allow time for Bluetooth reconnection. Trackball or encoder motion is not a promised deep-sleep wake source.
- USB-powered halves stay awake for USB/Studio use. Save Studio changes before battery sleep; unsaved RAM changes are lost.
- The trackball uses motion interrupts and its existing sensor sleep configuration. Current draw and wake reliability still require physical testing.
- BLE trackball motion is combined into reports at least **8 ms** apart, retaining total displacement; USB output remains immediate. The right half requests a **7.5 ms** host connection interval with zero peripheral latency. The host decides the actual interval, and connected-idle battery consumption may increase. This change still needs a physical smoothness and power test.

See [maintenance](docs/maintenance.md), [firmware compatibility](docs/hardware.md) and [validation](docs/validation.md). Dependencies are pinned in config/west.yml. Original code is MIT; see [third-party notices](THIRD_PARTY_NOTICES.md) for dependency licenses.
