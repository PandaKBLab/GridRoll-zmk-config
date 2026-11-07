#!/usr/bin/env python3
"""Exercise the real patched sampler callback against LED freshness policy."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--source", type=Path, required=True)
p.add_argument("--activity", type=Path, required=True)
a = p.parse_args()
source = a.source.read_text()
match = re.search(r"static void zmk_battery_work\(struct k_work \*work\) \{", source)
assert match
start = source.index("{", match.start())
depth, end = 1, start + 1
while depth:
    depth += (source[end] == "{") - (source[end] == "}")
    end += 1
with tempfile.TemporaryDirectory() as temp:
    temp = Path(temp)
    (temp / "battery_work.inc").write_text(source[match.start():end])
    power = a.activity.read_text()
    part = re.search(r'bool is_usb_power_present\(void\) \{.*?\n\}', power, re.S).group(0)
    (temp / "usb_power.inc").write_text(part)
    exe = temp / "test-battery-hook"
    subprocess.run(["cc", "-Wall", "-Wextra", "-Werror", "-Wno-unused-parameter", "-std=c11",
                    "-I" + str(temp), "-I" + str(ROOT / "drivers/status"),
                    str(ROOT / "tests/test_battery_status_hook.c"), "-o", str(exe)], check=True)
    subprocess.run([str(exe)], check=True)
