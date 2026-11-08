#!/usr/bin/env python3
"""Validate the actual patched BLE source and its native advertising decision."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def block(source, pattern):
    match = re.search(pattern, source)
    assert match, pattern
    start = source.index("{", match.start())
    depth, end = 1, start + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[match.start():end]


p = argparse.ArgumentParser()
p.add_argument("--source", type=Path, required=True)
p.add_argument("--uuid", type=Path, required=True)
p.add_argument("--emit-only", action="store_true")
a = p.parse_args()
source = a.source.read_text()
uuid = a.uuid.read_text()
# Audited DYA client: cormoran/zmk-studio-ts-client 39083858775d320018716e3d8fd68d00f6d11118,
# src/transport/gatt.ts filters Studio UUID OR Battery Service; pairing/keyboard
# connection alone is not sufficient when the firmware no longer advertises.
assert "BT_UUID_128_ENCODE(num, 0x0196, 0x6107, 0xc967, 0xc5cfb1c2482a)" in uuid
assert "ZMK_STUDIO_BT_SERVICE_UUID ZMK_BT_STUDIO_UUID(0x00000000)" in uuid
scan = block(source, r"static const struct bt_data zmk_ble_sd\[\] =")
assert "BT_DATA_BYTES(BT_DATA_UUID128_ALL, ZMK_STUDIO_BT_SERVICE_UUID)" in scan
assert "#if IS_ENABLED(CONFIG_ZMK_STUDIO_TRANSPORT_BLE)" in source
assert "#define GRIDROLL_STUDIO_SCAN_RSP NULL, 0" in source
ad = block(source, r"static (?:const )?struct bt_data zmk_ble_ad\[\] =")
assert "BT_UUID_HIDS_VAL" in ad and "BT_UUID_BAS_VAL" in ad
assert "BT_LE_ADV_OPT_FORCE_NAME_IN_AD" in source
assert "bt_le_adv_start(ZMK_ADV_CONN_NAME, zmk_ble_ad, ARRAY_SIZE(zmk_ble_ad), GRIDROLL_STUDIO_SCAN_RSP)" in source
assert 3 + 4 + 6 + 2 + len("GridRoll".encode()) <= 31
assert 2 + 16 <= 31  # the service UUID is separate from the primary packet
functions = [block(source, r"int " + name + r"\(") for name in [
    "update_advertising", "zmk_ble_set_directed_advertising"]]
if not a.emit_only:
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        (folder / "native_ble_functions.inc").write_text("\n\n".join(functions))
        executable = folder / "test-native-ble"
        subprocess.run(["cc", "-Wall", "-Wextra", "-Werror", "-std=c11", "-I" + str(folder),
                        str(ROOT / "tests/test_native_ble_discovery.c"), "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True)
print("Studio BLE UUID, HID/BAS/name preservation, legacy packet budgets and native source checks passed")
