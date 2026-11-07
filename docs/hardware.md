# Firmware compatibility

This firmware targets GridRoll E73/nRF52840 keyboards with 47 keys, a left encoder and a right PAW3222 trackball. The right half is the computer-facing central; the left is its wireless peripheral.

Features include USB/BLE keyboard and pointer output, ZMK Studio over the right USB connection, DYA runtime mouse/scroll and per-layer encoder settings, eight enabled layers adapted from LiNEA40, automatic USB preference on computer connection, idle power management and timed deep sleep with matrix-key wake.

Firmware-required GPIO and layout definitions are maintained in boards/. Do not flash this image onto another keyboard solely because it uses the same controller or sensor.

PCB projects, schematics, routing, netlists, module-pad maps and internal circuit documentation are not distributed here. For service or assembly, use the product's separately supplied instructions.

See [first flash](first-flash.md), [maintenance](maintenance.md) and [validation](validation.md). Software checks do not replace physical radio, power and wake tests.
