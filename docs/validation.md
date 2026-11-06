# Validation status

## Current update — 2026-11-06

The firmware uses GridRoll for its keyboard, BLE and USB name, corrects the reported PAW3222 mounting orientation before DYA processing, and enables 30-second idle / 15-minute battery deep sleep. The right half retains ZMK Studio and the USB RPC transport. Both halves retain matrix-key wake.

Software checks cover firmware-required GPIO reservations and keymap structure, SDIO error recovery, all four trackball directions and signed limits, compiled names and roles, BLE/Studio flags, sleep timeouts, and HEX/UF2 address consistency.

## Download package

Each successful Actions run publishes exactly one **GridRoll-firmware** ZIP. It contains only:

- GridRoll-left.uf2
- GridRoll-right.uf2
- GridRoll-settings-reset.uf2

Diagnostic images, bootloader images, HEX files, logs, device trees and build configurations are not uploaded in the standard package. The upload runs only after all application builds and package-content checks succeed. Build diagnostics remain in the Actions job logs.

Verified [push-triggered Actions run 42164852588](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42164852588), built from commit **62dc635d95d07206c657722b84618848c94f72fe**, completed successfully. It created exactly one artifact: [GridRoll-firmware.zip](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42164852588/artifacts/13477908401).

The ZIP was downloaded and inspected: exactly the three files listed above, no directories or extra files; ZIP integrity, nRF52840 UF2 headers, block counts and application address bounds passed. Its SHA-256 matches GitHub's artifact digest: **c0819f372d20370198c4621a25c6b4c291966c14e94276be1aeb758ebd893f21**. The left and right image hashes match the previous successful software build, so this update changes packaging and documentation only.

| File | UF2 SHA-256 |
|---|---|
| GridRoll-left.uf2 | 83988b091d57b19b6f2f23f48b8696a3b45eeb76d29611a64e6629397ec0bdbd |
| GridRoll-right.uf2 | dfbe164607a4e915c8b672e54108cafac174283d4f2bb8f9e5f3064d0fe0ebf8 |
| GridRoll-settings-reset.uf2 | 57fdc42869a3c7a2dead79a461b1134f7c1bdf2ec981c08fb2593c5459c3e575 |

Internal circuit and module-pad tables have been removed from current documentation. Existing Git history has not been rewritten.

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
