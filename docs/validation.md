# Validation status

## Current update — 2026-11-06

The firmware uses GridRoll for its keyboard, BLE and USB name, corrects the reported PAW3222 mounting orientation before DYA processing, and enables 30-second idle / 15-minute battery deep sleep. The right half retains ZMK Studio and the USB RPC transport. Both halves retain matrix-key wake.

Software checks cover firmware-required GPIO reservations and keymap structure, SDIO error recovery, all four trackball directions and signed limits, compiled names and roles, BLE/Studio flags, sleep timeouts, and HEX/UF2 address consistency.

The latest successful GitHub Actions run and its exact commit are the source of truth for downloadable firmware. Do not infer a successful build from a commit or a queued run. Current checks are being rerun for the PandaKBLab repository.

## Physical verification

The user reported that Bluetooth was not discoverable and that trackball directions were rotated. Software changes have not yet been physically verified.

| Check | Required observation | Status |
|---|---|---|
| Keys and encoder | Correct input on both halves and no duplicate presses | Pending |
| Trackball | Up/down/left/right match physical movement | Pending |
| Mouse layer | Consistent horizontal and vertical scrolling | Pending |
| Bluetooth | Right half is discoverable as GridRoll on an open profile and pairs | Pending |
| Split | Both halves reconnect after power cycling and sleep | Pending |
| ZMK Studio | Right USB connects; unlock, edit, save and reconnect work | Pending |
| DYA | Pointer and scroll parameters persist after power cycling | Pending |
| Power | Measure active, idle and battery deep-sleep current | Pending |
| Wake | Press keys on each sleeping half; verify reconnect and input | Pending |
| USB | USB-powered half stays awake during Studio use | Pending |
| Recovery | Correct-side UF2 update and settings-reset recovery | Pending |

Record the firmware commit and run number when reporting results. This repository contains firmware validation only; PCB design, circuit checks and manufacturing approval are outside its scope.
