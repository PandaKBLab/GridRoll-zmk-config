# Validation status

## Current update — 2026-11-07

The firmware uses GridRoll for its keyboard, BLE and USB name, corrects the reported PAW3222 mounting orientation before DYA processing, and enables 30-second idle / 15-minute battery deep sleep. The right half retains ZMK Studio and the USB RPC transport. Both halves retain matrix-key wake.

Software checks cover firmware-required GPIO reservations and keymap structure, SDIO error recovery, all four trackball directions and signed limits, compiled names and roles, BLE/Studio flags, sleep timeouts, and HEX/UF2 address consistency.

The user subsequently confirmed that a computer can connect with the right half on battery, then reported continuous trackball stutter and trailing motion over BLE while USB movement feels responsive. This update batches relative motion into BLE input frames at least 8 ms apart, retaining displacement and flushing the final movement after the sensor becomes idle. USB bypasses pacing. Input-queue retry handling retains a partially queued X/Y frame without duplicating an accepted X event. No periodic report timer runs when there is no pending motion.

The right half now requests a 7.5 ms host connection interval with peripheral latency 0; the Studio BLE latency preference is also 0. These are requested parameters, not measured host-negotiated values. Left split-link parameters, 1M PHY, radio transmit power, GPIOs, mounting correction, Studio/DYA and sleep/wake configuration are unchanged. Connected-idle current may increase and must be measured. The unit tests simulate a 1 kHz input stream, final-tail delivery, idle, USB bypass, signed limits and queue backpressure; physical latency and current are still pending.

## Download package

Each successful Actions run publishes exactly one **GridRoll-firmware** ZIP. It contains only:

- GridRoll-left.uf2
- GridRoll-right.uf2
- GridRoll-settings-reset.uf2

Diagnostic images, bootloader images, HEX files, logs, device trees and build configurations are not uploaded in the standard package. The upload runs only after all application builds and package-content checks succeed. Build diagnostics remain in the Actions job logs.

Verified [push-triggered Actions run 42352410024](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42352410024), built from commit **da512166c82086f4e31c96ca10fb22dd27ddd6a2**, completed successfully. All motion/SDIO/GPIO unit tests, four application builds, compiled-configuration assertions, application address checks and the separate bootloader regression job passed. It created exactly one artifact: [GridRoll-firmware.zip](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42352410024/artifacts/13566097870).

The ZIP was downloaded and inspected: exactly the three files listed above, no directories or extra files; ZIP integrity, nRF52840 UF2 headers, block counts and application address bounds passed. Its SHA-256 matches GitHub's artifact digest: **010772eba7a2377d17462c738ec4e9d73b64c660e7cba357d7bbe9e946a55790**. The left and settings-reset image hashes match the previous successful build; the right image changed. Existing users can flash only GridRoll-right.uf2 without clearing settings. These checks validate the software and package, not physical BLE smoothness or current draw.

| File | UF2 SHA-256 |
|---|---|
| GridRoll-left.uf2 | 83988b091d57b19b6f2f23f48b8696a3b45eeb76d29611a64e6629397ec0bdbd |
| GridRoll-right.uf2 | 3a123b0853b02c196556e51fe5de4304abb12c8ee560831375ad0032c4c42565 |
| GridRoll-settings-reset.uf2 | 57fdc42869a3c7a2dead79a461b1134f7c1bdf2ec981c08fb2593c5459c3e575 |

Internal circuit and module-pad tables have been removed from current documentation. Existing Git history has not been rewritten.

## Physical verification

On 2026-11-06, the user confirmed that both halves' keys and the right trackball work with right USB connected and the left half on battery. This verifies basic split input over BLE and right USB input; encoder behavior and corrected trackball orientation have not been rechecked separately.

During host-discovery troubleshooting, the user powered off the left half and reset the USB-powered right half: a phone could then discover **GridRoll**. With the right half left running, switching the left half back on did not prevent discovery. These observations show that host advertising can work alongside the split link. The original failure has not been reproduced or assigned a confirmed cause. No firmware code, configuration or dependency changes were made during that discovery diagnostic sequence. The user later confirmed a computer connection without right USB; a complete both-halves battery input test remains pending.

| Check | Required observation | Status |
|---|---|---|
| Keys | Input on both halves, right USB and left battery | User-reported working; duplicate-press test pending |
| Encoder | Correct rotation and press behavior | Pending |
| Trackball | Up/down/left/right match physical movement | USB input user-reported working; direction test pending |
| Mouse layer | Consistent horizontal and vertical scrolling | Pending |
| Bluetooth discovery | Phone discovers the right half as GridRoll, with the left off and on | User-reported working after right reset |
| Bluetooth host input | Pair a computer and use both halves on battery | Battery-powered host connection user-reported; complete input test pending |
| BLE trackball latency | Compare continuous motion, stop response and scrolling with USB | Previous build stutter user-reported; new software checks passed, flash/physical test pending |
| Split | Both halves reconnect after power cycling and sleep | Basic split input user-reported working; cycle/sleep tests pending |
| ZMK Studio | Right USB connects; unlock, edit, save and reconnect work | Pending |
| DYA | Pointer and scroll parameters persist after power cycling | Pending |
| Power | Measure active, idle and battery deep-sleep current | Pending |
| Wake | Press keys on each sleeping half; verify reconnect and input | Pending |
| USB | USB-powered half stays awake during Studio use | Pending |
| Recovery | Correct-side UF2 update and settings-reset recovery | Pending |

Record the firmware commit and run number when reporting results. This repository contains firmware validation only; PCB design, circuit checks and manufacturing approval are outside its scope.
