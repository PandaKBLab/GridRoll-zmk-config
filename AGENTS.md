# Firmware maintenance

- Default ZMK Studio to `CONFIG_ZMK_STUDIO_LOCKING=n`. Do not require a Studio
  unlock key, idle relocking or relocking after disconnect unless the user
  explicitly requests locking. Keep this policy in compiled-config checks.
- Preserve both standard ZMK Studio keymap editing and DYA Studio mouse/scroll
  settings plus runtime encoder rotation. Keep eight enabled default layers and
  automatic USB preference on a new enumerated connection; allow manual BLE.
  Default to Planck-style QWERTY/Lower/Raise, Mouse J=left/K=right, a 200 ms
  typing guard and 1200 ms auto-Mouse inactivity timeout. Protect held drags;
  use discrete encoder wheel events. Preserve saved settings; document overrides.
  Generate keymap diagrams/tables from source and keep them checked in CI.
  Verify extension wire compatibility against pinned source snapshots;
  do not claim every DYA-specific hardware feature is implemented.
- Use GitHub Actions for full firmware builds. Publish exactly one
  `GridRoll-firmware` artifact containing only `GridRoll-left.uf2`,
  `GridRoll-right.uf2`, and `GridRoll-settings-reset.uf2`.
- Preserve GPIOs, matrix order, saved settings and battery sleep/key wake unless
  the user requests a change. Keep dependencies pinned and review RAM usage.
- This repository is firmware only. Do not add PCB projects, schematics,
  routing, netlists or internal circuit documents. Never claim hardware tests
  were performed from a successful build or protocol test alone.
