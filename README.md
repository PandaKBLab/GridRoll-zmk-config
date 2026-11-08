# GridRoll

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Deutsch](README.de.md)

ZMK firmware for PandaKB GridRoll: 47 keys, a left encoder, a right PAW3222 trackball, USB/Bluetooth, ZMK Studio and DYA Studio. The **right half connects to the computer**, the left connects to it wirelessly. Keyboard, USB and Bluetooth name: **GridRoll**.

This repository distributes firmware and user documentation. It does not distribute PCB projects, schematics, routing, netlists or internal circuit documents.

## Download and update

Open a successful [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) run and download the single **GridRoll-firmware** ZIP. It contains exactly:

- **GridRoll-left.uf2**

- **GridRoll-right.uf2**

- **GridRoll-settings-reset.uf2**

Flash each application to its matching half. **Do not flash settings-reset for a normal update**: it clears settings and pairing. First installation uses the separate [bootloader procedure](docs/first-flash.md). Artifacts remain available for 30 days. A build pass is software validation, not a physical device test.

## Four functional layers

| Layer | Purpose / access | Encoder CW / CCW |
|---|---|---|
| L0 Base | QWERTY; ordinary left Space and right Enter | Wheel up / down |
| L1 Mouse | Automatic on ball motion; or Fn+B, Esc to leave | Wheel up / down |
| L2 Symbols | Hold Symbols, immediately left of left Space | Wheel up / down |
| L3 Function | Hold Fn, immediately right of right Enter; also ball scrolling | Volume up / down |
| L4–L7 | Empty editable slots: no key or encoder action | None |

Base bottom row: Ctrl, Alt, GUI, encoder middle-click, Symbols, **Space** | **Enter**, Fn, trackball opening, Left, Down, Right. Space/Enter are ordinary keys; the former third-row Enter is now right Shift. See [all 376 exact bindings and all layer diagrams](docs/keymap.md).

**Saved layouts override source defaults.** To adopt this four-layer arrangement, export your old layout, use **ZMK Studio's keymap Restore Stock Settings**, and save. This does not require a pairing reset. DYA encoder overrides are separate: set L0–L2 to wheel up/down, L3 to volume up/down, L4–L7 to no action. Preserve your other DYA parameters.

### L0 Base

![L0 Base](docs/keymap/layer-0.svg)

### L1 Mouse

![L1 Mouse](docs/keymap/layer-1.svg)

### L2 Symbols

![L2 Symbols](docs/keymap/layer-2.svg)

### L3 Function

![L3 Function](docs/keymap/layer-3.svg)

### Empty slots L4–L7

![L4 empty](docs/keymap/layer-4.svg)
![L5 empty](docs/keymap/layer-5.svg)
![L6 empty](docs/keymap/layer-6.svg)
![L7 empty](docs/keymap/layer-7.svg)

## Trackball and mouse controls

Native **798 CPI, about 800 DPI**, is the closest 38-CPI sensor step approved for this keyboard; no extra correction is applied. With DYA mouse scaling 1/1, holding **L1 left row 4 / column 6 (left Space position)** gives one quarter speed, about **200 effective DPI**; release restores normal speed. DYA speed settings remain effective.

Mouse: **J left, K right, H middle click; L Back, semicolon Forward; U/I wheel up/down, O/P horizontal wheel**. Hold **M** in Mouse, or hold Fn from Base, for ball scrolling through the separate DYA scroll processor. Base letters remain letters.

First valid ball movement enables Mouse outside a **200 ms typing guard**. Mouse exits **1200 ms** after the last pointer/wheel/button activity; held mouse/modifier/precision keys protect dragging. Ordinary transparent typing exits; Esc returns to Base. Fn+B enters a manual Mouse layer which Esc leaves. No idle polling is added. Keep DYA mouse Temp-layer enabled / target 1 / guard 200 / expiry 1200 when adopting these defaults.

## USB, Bluetooth and both Studios

Pair the computer with **GridRoll on the right half**. Fn+A/S/D/F/G select host profiles 0–4. Fn+Z clears only the selected profile when a new pairing is wanted. Normal updates keep bonds.

New computer USB enumeration prefers USB automatically; a charge-only cable does not force it. **Fn+X selects USB, Fn+C selects BLE**. Manual BLE remains selected until the next USB connection; unplugging falls back to a connected host.

**ZMK Studio and DYA Studio remain unlocked**: no edit-unlock key, idle relocking or disconnect relocking. Browser connection authorization is still selected by the user. For wired settings, connect right USB, select USB output and its serial port; close other pages using the same port.

For **wireless DYA/Studio** on the currently paired computer: select BLE output (**Fn+C**), press **Fn+V**, then rescan/connect in DYA's Bluetooth picker. The discovery window lasts at most **60 seconds**, and closes earlier on keyboard idle, USB output or disconnection. A new BLE host connection or selection from USB also opens a window. Ordinary input does not endlessly renew it. Closing the advertising window does not deliberately disconnect an established settings session. This key opens discovery; it does not unlock editing.

The previous firmware stopped advertising once the host connected, which can hide a working keyboard from the browser picker. The update adds bounded connected-host discovery plus the Studio service UUID in scan response, while retaining normal keyboard/battery/name discovery. Actual Windows/browser GATT connection and saved-setting behavior still require device verification. See [wireless settings steps and limits](docs/studio-wireless.md).

DYA supports mouse/scroll and per-layer encoder settings. CI checks three pinned extension protocols and compiled unlocked transports; unimplemented sensor imaging features are not implied.

## LEDs, power and wake

Right red: waiting 100 ms/2 s for at most 30 s; connected on 2 s, then off. Each half's own estimated battery ≤15% gives 100 ms/30 s, clearing at ≥20%; USB suppresses it. Idle/sleep turns red off. Blue remains a hardware charging-cycle indication and does not uniquely prove full charge. See [LED policy](docs/led-status.md).

Battery sampling uses the native single sampler every 60 s while active, stops in idle, and refreshes after wake. After **30 s** without input the keyboard idles; after **15 min** on battery it deep-sleeps. Press a key on each sleeping half to wake; ball/encoder motion is not a promised deep-sleep wake source. USB-powered halves remain awake. Save wireless Studio edits before timed battery sleep.

The discovery window creates no artificial activity to defeat sleep. Normal connected use is not permanently advertising for Studio. Existing motion interrupts, 8 ms BLE motion batching, USB immediate output and the requested 7.5 ms host interval remain; the host negotiates actual radio timing. Current and wake reliability need physical testing.

[Maintenance](docs/maintenance.md) · [Firmware compatibility](docs/hardware.md) · [Validation](docs/validation.md). Dependencies stay pinned. Original code is MIT; see [third-party notices](THIRD_PARTY_NOTICES.md).
