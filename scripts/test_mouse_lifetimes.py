#!/usr/bin/env python3
"""Compile the actual patched lifetime and wheel functions against a host harness."""
import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def block(source, pattern):
    match = re.search(pattern, source)
    assert match, pattern
    start = source.index("{", match.start())
    depth = 1
    end = start + 1
    while depth:
        depth += (source[end] == "{") - (source[end] == "}")
        end += 1
    return source[match.start():end]


parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, required=True)
parser.add_argument("--emit-only", action="store_true")
args = parser.parse_args()
source = args.source.read_text()
functions = [block(source, rf"(?:static )?(?:int|void) {name}\(") for name in [
    "zmk_input_processor_runtime_note_activity", "temp_layer_activation_work_handler",
    "temp_layer_deactivation_work_handler", "position_state_changed_listener",
    "runtime_processor_layer_state_changed_listener"]]
motion = block(source, r"if \(data->temp_layer_enabled && event->value != 0\)")
renew = block(source, r"if \(data->temp_layer_enabled && data->temp_layer_layer_active &&")
functions.append("static void motion(struct input_event *event) {\n"
                 "struct runtime_processor_data *data = &data0;\n" + motion + "\n" + renew + "\n}")
wheel = (ROOT / "drivers/input/wheel_step.c").read_text()
functions += [block(wheel, rf"static int {name}\(") for name in ["pressed", "released"]]
if args.emit_only:
    print("Actual mouse lifetime, activation guard and wheel functions extracted")
    sys.exit(0)
with tempfile.TemporaryDirectory() as folder:
    folder = Path(folder)
    (folder / "runtime_functions.inc").write_text("\n\n".join(functions))
    if not args.emit_only:
        executable = folder / "test-mouse"
        subprocess.run(["cc", "-Wall", "-Wextra", "-Werror", "-Wno-unused-parameter", "-std=c11",
                        "-I" + str(folder), str(ROOT / "tests/test_mouse_lifetimes.c"),
                        "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True)
print("Actual mouse lifetime and wheel functions extracted" if args.emit_only else
      "Single-frame expiry, typing guard, held/multiple buttons, wheel renewal and manual layer tests passed")
