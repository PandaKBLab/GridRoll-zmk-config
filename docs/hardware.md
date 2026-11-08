# Firmware compatibility

This firmware targets GridRoll E73/nRF52840 keyboards with 47 keys, a left encoder and a right PAW3222 trackball. The right half is the computer-facing central; the left is its wireless peripheral.

Features include USB/BLE keyboard and pointer output, unlocked ZMK Studio and DYA runtime mouse/scroll/encoder settings, four populated layers plus four empty editable slots, automatic Mouse (200 ms typing guard / 1200 ms exit), native 798 CPI (about 800 DPI), and discrete encoder wheel steps. Base has ordinary left Space/right Enter. Bounded BLE Studio discovery complements the existing USB transport. Automatic USB preference, local switched battery sensing, bounded red indications, idle management and timed battery sleep with matrix-key wake remain. Blue charging stays hardware controlled; no definitive software charge-complete indication is inferred. Browser/device wireless Studio still needs physical validation.

Firmware-required GPIO and layout definitions are maintained in boards/. Do not flash this image onto another keyboard solely because it uses the same controller or sensor.

PCB projects, schematics, routing, netlists, module-pad maps and internal circuit documentation are not distributed here. For service or assembly, use the product's separately supplied instructions.

See [first flash](first-flash.md), [maintenance](maintenance.md) and [validation](validation.md). Software checks do not replace physical radio, power and wake tests.
