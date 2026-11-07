#!/usr/bin/env python3
"""Compile the actual precision behavior functions against a runtime API harness."""
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


parser = argparse.ArgumentParser()
parser.add_argument("--emit-only", action="store_true")
args = parser.parse_args()
source = (ROOT / "drivers/input/precision.c").read_text()
parts = [block(source, rf"struct {name} \{{") + ";" for name in ["precision_config", "precision_data"]]
parts += [block(source, rf"static int {name}\(") for name in [
    "precision_apply", "precision_pressed", "precision_released"]]
if args.emit_only:
    print("Actual quarter-speed precision behavior functions extracted")
else:
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        (folder / "precision_functions.inc").write_text("\n\n".join(parts))
        executable = folder / "test-precision"
        subprocess.run(["cc", "-Wall", "-Wextra", "-Werror", "-std=c11", "-I" + str(folder),
                        str(ROOT / "tests/test_precision.c"), "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True)
