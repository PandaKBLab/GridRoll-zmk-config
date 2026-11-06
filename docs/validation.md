# Validation status

## Current update — 2026-11-06

The firmware uses GridRoll for its keyboard, BLE and USB name, corrects the reported PAW3222 mounting orientation before DYA processing, and enables 30-second idle / 15-minute battery deep sleep. The right half retains ZMK Studio and the USB RPC transport. Both halves retain matrix-key wake.

Software checks cover firmware-required GPIO reservations and keymap structure, SDIO error recovery, all four trackball directions and signed limits, compiled names and roles, BLE/Studio flags, sleep timeouts, and HEX/UF2 address consistency.

The inherited fork workflow was backed up, removed and re-registered through the GitHub API. A subsequent **push** automatically started [run 42160071055](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42160071055), which completed successfully for both the firmware and bootloader jobs. The firmware source commit is **5cb5d0e5ae8b94204a9ccdfae394eb3443c62c4c**. No browser automation or new login credentials were used for this recovery.

The hardware/keymap guard, SDIO failure-recovery tests, physical-direction regression test, all four application builds, first-flash builds and HEX/UF2 address checks passed. Downloaded ZIP checksums matched GitHub's artifact digests. The individual left/right UF2 files also matched the full bundle byte for byte.

| Firmware | Download | UF2 SHA-256 |
|---|---|---|
| Left | [GridRoll-left ZIP](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42160071055/artifacts/13476481914) | 83988b091d57b19b6f2f23f48b8696a3b45eeb76d29611a64e6629397ec0bdbd |
| Right | [GridRoll-right ZIP](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42160071055/artifacts/13476736347) | dfbe164607a4e915c8b672e54108cafac174283d4f2bb8f9e5f3064d0fe0ebf8 |

Final compiled configurations were independently read from the downloaded bundle: both sides use the GridRoll name, BLE, 30-second idle and 15-minute battery sleep; the right is central and includes ZMK Studio RPC, its USB serial transport, DYA runtime RPC and 1M PHY compatibility. Both device trees retain matrix-key wake. Artifacts expire on 2026-12-06.

All 58 files in the tested source tree matched the reviewed local files. The current tree contains firmware, tools and documentation, with English/Chinese/Japanese/German README files and no PCB, schematic or routing files. Internal circuit and module-pad tables were removed from current documents; existing Git history was not rewritten.

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
