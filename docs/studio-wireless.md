# Wireless Studio discovery

GridRoll keeps **ZMK Studio and DYA Studio unlocked**. A discovery window makes
the device visible to the browser; it is not an edit-unlock operation and does
not bypass Bluetooth pairing.

## Using this update

1. Flash the right application firmware. For a previously Studio-saved layout,
   connect right USB first, export the old layout, restore the stock **keymap**
   in ZMK Studio, and save. No settings-reset flash is needed.
2. Use the Bluetooth profile paired to this computer. In the four-layer default
   layout, Fn+A/S/D/F/G select profiles 0–4. Select BLE output with **Fn+C**.
3. Press **Fn+V**, open DYA's Bluetooth connection picker, and rescan. Select
   **GridRoll** and authorize the connection. On an older saved layout, the same
   zero-parameter behavior is named **Studio BLE discover (60s)**.
4. Make changes and save. Close other Studio sessions using the same device.
   If using wired Studio instead, select USB output with Fn+X.

The window lasts at most 60 seconds. Idle, USB output or host disconnection
closes the extra connected-host advertising early. Normal input does not keep
renewing it; press Fn+V again if necessary. A fresh BLE host connection or
selection of BLE after USB opens a window automatically while active. Routine
movement after idle does not reopen it. Window expiry does not deliberately
disconnect an already established GATT session, and normal pairing/reconnect
advertising remains available when the selected host is disconnected.

This feature does not fake keyboard activity or prevent battery sleep. Save
wireless edits before the existing 15-minute battery sleep timeout; key wake and
30-second idle behavior remain. Actual host behavior needs testing.

## Why the working keyboard could be missing

The user reported that USB DYA settings and normal wireless keyboard input work,
but GridRoll is absent from the Web Bluetooth picker. That observation alone
does not establish a hardware or browser-specific cause.

The pinned firmware's [advertising decision](https://github.com/cormoran/zmk/blob/1fc72aaff7a42bd533c1f4c9b3f23c5317c745f4/app/src/ble.c)
stops advertising when the selected host is connected, unless its separate
advertising flag is enabled. The old configuration disables the Studio lock and
therefore has no unlock event to open that advertising window. The audited
[DYA client](https://github.com/cormoran/zmk-studio-ts-client/blob/39083858775d320018716e3d8fd68d00f6d11118/src/transport/gatt.ts)
filters its device picker by the Studio service **or** Battery Service. A usable
HID connection does not guarantee browser discovery of a device that no longer
advertises.

The firmware now controls a bounded advertising flag independently of the edit
lock. A scoped patch also places the standard Studio service UUID
`00000000-0196-6107-c967-c5cfb1c2482a` in scan response. The primary packet keeps
HID, Battery Service, appearance, flags and the GridRoll name; both legacy
packets stay within 31 bytes. The left split peripheral does not gain a host
Studio service or advertising window. GATT encryption, profile ownership and
stored bonds are unchanged.

## Verification boundary

CI checks the actual patched native advertising decision, Studio UUID, packet
budgets and window policy, plus compiled BLE/USB transports and disabled
Studio locking. It does **not** prove that the user's Windows Bluetooth stack,
browser cache or DYA build will complete a GATT connection. Official
[ZMK Studio documentation](https://zmk.dev/docs/features/studio) describes
platform-dependent BLE support. Physical discovery, edits/save, pointer latency,
current and sleep/wake remain device acceptance tests.

If an update still fails, report whether GridRoll appears within the Fn+V
window, the browser/OS, output/profile, and exact error. Keep USB Studio available;
do not clear every bond or flash settings-reset merely because a picker is empty.
