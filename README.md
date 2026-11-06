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

With the stock keymap, hold **Fn + Mouse** to enter System: top-row **Q** selects profile 0, **Backspace** clears that profile, and **U** selects BLE output. Studio-saved layouts may differ.

For [ZMK Studio](https://zmk.studio/) or [DYA Studio](https://studio.dya.cormoran.works/), connect the **right half by USB**, select USB output, then use System's top-left key to unlock editing. Close other pages using the same serial port and save your changes. Updates preserve Studio/DYA settings. If you previously compensated the trackball rotation in DYA, remove that extra compensation: mounting correction now runs before both pointer and scroll processing.

## Power and wake

- **30 seconds** without input: idle, with Bluetooth available.
- **15 minutes** without input on battery: deep sleep. Press a key on each sleeping half to wake it; allow time for Bluetooth reconnection. Trackball or encoder motion is not a promised deep-sleep wake source.
- USB-powered halves stay awake for USB/Studio use. Save Studio changes before battery sleep; unsaved RAM changes are lost.
- The trackball uses motion interrupts and its existing sensor sleep configuration. Current draw and wake reliability still require physical testing.

See [maintenance](docs/maintenance.md), [firmware compatibility](docs/hardware.md) and [validation](docs/validation.md). Dependencies are pinned in config/west.yml. Original code is MIT; see [third-party notices](THIRD_PARTY_NOTICES.md) for dependency licenses.
