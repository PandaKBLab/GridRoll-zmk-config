# Validation status

## Current update — hold for precision movement (2026-11-08)

L1 Mouse left 41 is left row 4 / column 1 (one-based), global position 36 / RC(3,0), the Base Ctrl position. Only that source binding changes. The new zero-parameter Studio behavior temporarily uses one quarter of the mouse processor's normal DYA scaling; release restores the current normal RAM baseline, including memory-only settings. It changes scaling only, preserves rotation/scroll settings and writes no settings. Multiple assignments do not compound the reduction and restore only after the last key is released. The key creates no work timers or periodic polling. Existing automatic-layer lifetime handling keeps L1 active while it is held and resumes the normal 1200 ms timeout on release. Base Ctrl, matrix/GPIO order, eight layers, LED policy, radio, sleep/wake, dependencies and both unlocked Studios are preserved.

Source and generated keymap checks pass locally. The actual behavior functions have a host regression harness for relative quarter speed, restoration, DYA baseline edits, multiple/duplicate key events, direction preservation and error handling; actual patched-layer lifetime tests also cover the precision hold. Full Actions build and hardware tests are pending for this update. Normal updates preserve saved Studio keymaps: if a previous layout overrides L1 left 41, assign **Precision 0.25x (hold)** to just that position and save, without clearing settings or pairing.

## Previous battery and status LED update (2026-11-08)

This update enables each half's existing switched battery sensing through the native ZMK sampler, once per 60 seconds while active, and the agreed red-LED policy. Right waiting flashes last at most 30 seconds; selected host connection lights for 2 seconds; local low battery uses 15%/20% hysteresis and 100 ms per 30 seconds. Real sample callbacks distinguish genuine/unchanged 0% from an uninitialized cache, errors and stale data. Idle/sleep cancels LED work synchronously; LED activity does not wake or keep the keyboard awake. The left retains its peripheral role and no USB data stack. Both halves recognize hardware VBUS for charging suppression and USB-powered sleep policy. Blue charging is unchanged and no software full-charge indication is inferred.

[Actions run 42392079162](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42392079162) passed the LED policy tests, actual patched battery-callback/hardware-USB tests, existing input/motion/USB regressions, all three DYA protocol checks, four application builds, compiled configuration assertions, address checks and the separate bootloader regression. The production left image links 193,984 bytes of FLASH (23.92%) / 39,672 bytes of RAM (15.13%); the right links 359,164 bytes of FLASH (44.29%) / 120,928 bytes of RAM (46.13%). These are static allocations, not measured peak stack or hardware current. The single downloaded ZIP passed integrity, three-file-only inventory, nRF52840 UF2 and application-address checks. Both Studio interfaces remain unlocked; keymap, DYA parameters, bonds, radio settings and battery sleep/key-wake defaults are preserved. Both application images need updating. Hardware battery calibration, visible flashes, current, cable/host handling and sleep/wake remain untested.

## Previous Planck/automatic Mouse update

The current source replaces LiNEA40 defaults with conventional Planck-style QWERTY/Lower/Raise and eight enabled layers. J/K in Mouse are left/right click. Mouse activates on the first valid ball event outside a 200 ms typing guard; idle expiry is 1200 ms after pointer/wheel/button activity, with held mouse/modifier protection and immediate ordinary-typing exit. A scoped patch to the pinned runtime processor arms expiry after even a single frame and handles release/multiple-button activity without idle polling. Base encoder defaults use discrete input wheel events instead of 20 ms timed scrolling. [Actions run 42384855102](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42384855102) passed all application and bootloader builds, GPIO/layout and generated-diagram checks, USB/motion regressions, three DYA protocol checks, and actual patched-function lifetime/wheel tests. The latter cover a single motion frame, typing guard, stale expiry, held/multiple buttons, modifier dragging, ordinary-typing exit, manual-layer ownership, explicit exit/re-entry, wheel renewal, and 1001 discrete downward steps with release producing no extra event. The production right image links 355,460 bytes of FLASH (43.83%) and 120,528 bytes of RAM (45.98% of 256 KiB); static allocations are not measured peak stack use. Device auto-layer, drag, wheel, Studio save/reconnect and power tests remain pending. Saved keymap, processor and encoder overrides are separate and intentionally preserved.

## Previous encoder/USB update

This update enables cormoran_rsr runtime encoder rotation, eight fully populated LiNEA40-inspired layers, Base wheel scrolling, and automatic USB preference after HID enumeration / settings load. Manual BLE, charge-only use, sleep/wake and unlocked Studio remain available. Generated diagrams and all 376 bindings pass local consistency checks. A third DYA schema and encoder read/write samples are added to CI. [Actions run 42381214356](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42381214356) passed: USB policy regression, generated diagrams, all three DYA extension schemas, encoder sensor/eight-layer read/write cross-decoding, four firmware builds, compiled flags/layers, address checks and bootloader regressions. Runtime sensor rotation adds 14 messages / 30 checked fields. The production right image links 356,496 bytes of FLASH (43.96%) and 121,064 bytes of RAM (46.18% of 256 KiB). Physical DYA edits/save/reconnect, clockwise direction, automatic USB switching and sleep/wake tests remain pending. Static allocations do not measure peak stack use.

## Previous stability update — 2026-11-07

This stability update disables Studio locking by default for all Studio-enabled GridRoll builds. Compiled checks require unlocked startup, no idle/disconnect relocking, USB serial and BLE Studio transports, standard Studio RPC, and DYA runtime-input/custom-settings RPC support. The existing unlock behavior remains available for saved-layout compatibility; pressing it is unnecessary. AGENTS.md records the default for future firmware work.

Input-queue backpressure now uses 2–32 ms bounded retries, including when fresh sensor samples arrive. Accepted X events are not duplicated, and staged Y/tail motion is retained. Motion IRQ scheduling respects an already-pending sample/recovery deadline. Right-side Studio/low-priority/system-work-queue stacks are 6144/4096/4096 bytes; CI reports linked RAM/FLASH usage. Sleep timeouts, key wake, GPIOs and pinned firmware dependencies are unchanged.

CI checks both DYA extension schemas against frontend source snapshot **3a0259938c8a7a3c1abcf1e7e52e783f34f23e6f**: protobuf numeric fields/types and nested messages are compared despite package/name changes, and processor write/read messages are cross-decoded. This is a source/wire compatibility test. Physical ZMK Studio/DYA connections, save/reconnect and long-session stability still require device tests.

The successful build checked 65 messages / 156 fields for runtime-input processing and 32 messages / 96 fields for custom settings; both schemas and processor read/write cross-decoding passed. Compiled configuration assertions confirmed disabled Studio locking, no idle/disconnect relocking, both transports and the required RPC extensions. The production right image links 336,576 bytes of FLASH (41.50% of the application region) and 119,416 bytes of RAM (45.55% of 256 KiB). These are static link allocations, not measured peak stack usage or a device stress test.

The firmware uses GridRoll for its keyboard, BLE and USB name, corrects the reported PAW3222 mounting orientation before DYA processing, and enables 30-second idle / 15-minute battery deep sleep. The right half retains ZMK Studio and the USB RPC transport. Both halves retain matrix-key wake.

Software checks cover firmware-required GPIO reservations and keymap structure, SDIO error recovery, all four trackball directions and signed limits, compiled names and roles, BLE/Studio flags, sleep timeouts, and HEX/UF2 address consistency.

The user subsequently confirmed that a computer can connect with the right half on battery, then reported continuous trackball stutter and trailing motion over BLE while USB movement feels responsive. This update batches relative motion into BLE input frames at least 8 ms apart, retaining displacement and flushing the final movement after the sensor becomes idle. USB bypasses pacing. Input-queue retry handling retains a partially queued X/Y frame without duplicating an accepted X event. No periodic report timer runs when there is no pending motion.

The right half retains its requested 7.5 ms host connection interval with peripheral latency 0; the Studio BLE latency preference is also 0. These are requested parameters, not measured host-negotiated values. Left split-link parameters, 1M PHY, radio transmit power, GPIOs, mounting correction and sleep/wake configuration are unchanged by this stability update. Studio locking is intentionally disabled. Connected-idle current may increase and must be measured. The unit tests simulate a 1 kHz input stream, final-tail delivery, idle, USB bypass, signed limits and queue backpressure; physical latency and current are still pending.

## Download package

Each successful Actions run publishes exactly one **GridRoll-firmware** ZIP. It contains only:

- GridRoll-left.uf2
- GridRoll-right.uf2
- GridRoll-settings-reset.uf2

Diagnostic images, bootloader images, HEX files, logs, device trees and build configurations are not uploaded in the standard package. The upload runs only after all application builds and package-content checks succeed. Build diagnostics remain in the Actions job logs.

Verified [push-triggered Actions run 42392079162](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42392079162), built from commit **047857c9b36432b712726d7901aac30c8c6fdb3f**, completed successfully. All motion/SDIO/GPIO unit tests, DYA protocol and cross-decoding checks, four application builds, compiled-configuration assertions, application address checks and the separate bootloader regression job passed. It created exactly one artifact: [GridRoll-firmware.zip](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/runs/42392079162/artifacts/13581603822).

The ZIP was downloaded and inspected: exactly the three files listed above, no directories or extra files; ZIP integrity, nRF52840 UF2 headers, block counts and application address bounds passed. Its SHA-256 matches GitHub's artifact digest: **4a46bed787b9703adf58358906f6b3c60b4a796074f3c8908c477c9dd7f4c970**. Both left and right images changed compared with the previous successful build (f0d20d3afeb08ef753f64df610ec4d7e32f6e2c0); settings-reset is unchanged. Flash GridRoll-left.uf2 and GridRoll-right.uf2 to their corresponding halves without clearing settings or flashing settings-reset. Normal updates preserve saved layouts: export an existing Studio layout before using Studio's restore-defaults operation to adopt the new eight-layer mapping; do not use settings-reset just to change keymaps. These checks validate the software and package, not physical BLE smoothness or current draw.

| File | UF2 SHA-256 |
|---|---|
| GridRoll-left.uf2 | b2e3d0e51c5875e2379e9d87c1d8e4b67af95d9d050afb5a7fb78e7072527537 |
| GridRoll-right.uf2 | 5bd261a4fef777c770bd730dd97efff5886b3f16488fa3fcd980ff3b2643b617 |
| GridRoll-settings-reset.uf2 | 57fdc42869a3c7a2dead79a461b1134f7c1bdf2ec981c08fb2593c5459c3e575 |

Internal circuit and module-pad tables have been removed from current documentation. Existing Git history has not been rewritten.

## Physical verification

On 2026-11-06, the user confirmed that both halves' keys and the right trackball work with right USB connected and the left half on battery. This verifies basic split input over BLE and right USB input; encoder behavior and corrected trackball orientation have not been rechecked separately.

During host-discovery troubleshooting, the user powered off the left half and reset the USB-powered right half: a phone could then discover **GridRoll**. With the right half left running, switching the left half back on did not prevent discovery. These observations show that host advertising can work alongside the split link. The original failure has not been reproduced or assigned a confirmed cause. No firmware code, configuration or dependency changes were made during that discovery diagnostic sequence. The user later confirmed a computer connection without right USB; a complete both-halves battery input test remains pending.

| Check | Required observation | Status |
|---|---|---|
| Keys | Input on both halves, right USB and left battery | User-reported working; duplicate-press test pending |
| Encoder | Base wheel down/up is one step per trigger; middle press works | Actual wheel function regression and compiled listener wiring passed; physical test pending |
| Automatic Mouse | First motion outside 200 ms typing guard enables Mouse; J/K click; idle 1200 ms exits; held/multiple mouse keys do not time out | Actual patched-function regression passed; physical movement/drag/save test pending |
| Trackball | Up/down/left/right match physical movement | USB input user-reported working; direction test pending |
| Scroll layer (L5) | Consistent horizontal and vertical trackball scrolling | Pending |
| Encoder runtime RPC | DYA lists the encoder, reads eight layers and saves both directions | Compiled RPC, sensor enumeration/eight-layer wire samples passed; physical edit/save test pending |
| USB default output | USB overrides saved BLE; charger retains BLE; manual BLE survives resume | Battery/charger/startup/manual-BLE/resume/reconnect policy tests and compiled configuration passed; physical test pending |
| Bluetooth discovery | Phone discovers the right half as GridRoll, with the left off and on | User-reported working after right reset |
| Bluetooth host input | Pair a computer and use both halves on battery | Battery-powered host connection user-reported; complete input test pending |
| BLE trackball latency | Compare continuous motion, stop response and scrolling with USB | Previous build stutter user-reported; new software checks passed, flash/physical test pending |
| Split | Both halves reconnect after power cycling and sleep | Basic split input user-reported working; cycle/sleep tests pending |
| ZMK Studio | Right USB connects; edit/save without unlock and reconnect without relocking | Compiled unlocked policy, transports and RPC checks passed; physical test pending |
| DYA | Keymap, mouse/scroll and encoder RPC work without unlock; saved values survive restart | Extension schema, read/write cross-decoding and compiled RPC checks passed; physical test pending |
| LED policy | Right host waiting/connection; local 15%/20% low battery; USB suppression; no idle flashes | Software policy/compiled flags passed; physical visibility/timing pending |
| Battery sampling | Compare local voltage/percentage with instruments, verify gate turns off and both sides report | Native callback and compiled bindings passed; calibration/current tests pending |
| Power | Measure active, idle and battery deep-sleep current | Pending |
| Wake | Press keys on each sleeping half; verify reconnect and input | Pending |
| USB | USB-powered half stays awake during Studio use | Pending |
| Recovery | Correct-side UF2 update and settings-reset recovery | Pending |

Record the firmware commit and run number when reporting results. This repository contains firmware validation only; PCB design, circuit checks and manufacturing approval are outside its scope.
