#!/usr/bin/env python3
"""Build and validate all application artifacts with the locked west workspace."""
import argparse, os, shutil, subprocess, sys
import yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS={entry["artifact-name"].removeprefix("GridRoll-"): entry
         for entry in yaml.safe_load((ROOT/"build.yaml").read_text())["include"]}
p=argparse.ArgumentParser()
p.add_argument("--workspace",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
p.add_argument("--only",choices=TARGETS)
a=p.parse_args(); workspace=a.workspace.resolve(); out=a.out.resolve(); out.mkdir(parents=True,exist_ok=True)
for name,entry in TARGETS.items():
    if a.only and a.only!=name: continue
    shield=entry["shield"]; snippets=entry.get("snippet", "").split(); stem=entry["artifact-name"]
    build=workspace/"build"/name
    command=["west","build","-p","-s",str(workspace/"zmk/app"),"-d",str(build),
             "-b",entry["board"]]
    if snippets: command += ["-S"," ".join(snippets)]
    command += ["--",f"-DZephyr_DIR={workspace}/zephyr/share/zephyr-package/cmake",
                f"-DZMK_CONFIG={ROOT}/config",f"-DZMK_EXTRA_MODULES={ROOT}",f"-DSHIELD={shield}"]
    log=out/f"{stem}.log"
    print(f"Building {stem}; log: {log}",flush=True)
    with log.open("w") as f:
        rc=subprocess.run(command,cwd=workspace,stdout=f,stderr=subprocess.STDOUT).returncode
    if rc:
        print(log.read_text()[-6000:]); sys.exit(rc)
    for line in log.read_text().splitlines():
        if line.strip().startswith(("Memory region", "FLASH:", "RAM:")):
            print(f"{stem}: {line.strip()}", flush=True)
    config=(build/"zephyr/.config").read_text()
    if name in ("left", "right", "right-diagnostics"):
        for flag in ['CONFIG_ZMK_KEYBOARD_NAME="GridRoll"',
                     'CONFIG_BT_DEVICE_NAME="GridRoll"',
                     "CONFIG_ZMK_BLE=y", "CONFIG_ZMK_SPLIT=y",
                     "CONFIG_ZMK_SLEEP=y", "CONFIG_ZMK_IDLE_TIMEOUT=30000",
                     "CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000",
                     "CONFIG_GRIDROLL_STATUS_LED=y", "CONFIG_ZMK_BATTERY_REPORTING=y",
                     "CONFIG_ZMK_BATTERY_REPORT_INTERVAL=60",
                     "CONFIG_ZMK_BATTERY_REPORTING_FETCH_MODE_STATE_OF_CHARGE=y",
                     "CONFIG_ZMK_BATTERY_VOLTAGE_DIVIDER=y", "CONFIG_ADC_NRFX_SAADC=y",
                     "CONFIG_BT_GATT_SERVICE_CHANGED=y"]:
            assert flag in config.splitlines(), f"{name}: missing {flag}"
    if name in ("right","right-diagnostics"):
        dts=(build/"zephyr/zephyr.dts").read_text()
        for layer in ["Base", "Mouse", "Lower", "Navigation", "Raise", "Scroll", "Wireless", "System"]:
            assert f'display-name = "{layer}";' in dts, f"{name}: missing compiled layer {layer}"
        assert 'compatible = "zmk,behavior-runtime-sensor-rotate";' in dts
        assert 'compatible = "gridroll,behavior-precision";' in dts
        for flag in ["CONFIG_ZMK_SPLIT_ROLE_CENTRAL=y","CONFIG_ZMK_STUDIO=y",
                     "# CONFIG_ZMK_STUDIO_LOCKING is not set",
                     "CONFIG_ZMK_STUDIO_RPC=y", "CONFIG_ZMK_STUDIO_TRANSPORT_UART=y",
                     "CONFIG_ZMK_STUDIO_TRANSPORT_BLE=y",
                     "CONFIG_ZMK_CUSTOM_SETTINGS=y", "CONFIG_ZMK_CUSTOM_SETTINGS_STUDIO_RPC=y",
                     "CONFIG_ZMK_RUNTIME_SENSOR_ROTATE=y",
                     "CONFIG_ZMK_RUNTIME_SENSOR_ROTATE_STUDIO_RPC=y",
                     "CONFIG_GRIDROLL_USB_AUTO_OUTPUT=y",
                     "CONFIG_GRIDROLL_WHEEL_STEP=y",
                     "CONFIG_GRIDROLL_PRECISION=y",
                     "CONFIG_ZMK_LOW_PRIORITY_THREAD_STACK_SIZE=4096",
                     "CONFIG_ZMK_STUDIO_RPC_THREAD_STACK_SIZE=6144",
                     "CONFIG_SYSTEM_WORKQUEUE_STACK_SIZE=4096",
                     "CONFIG_GRIDROLL_PAW3222=y","CONFIG_ZMK_RUNTIME_INPUT_PROCESSOR_STUDIO_RPC=y",
                     "CONFIG_ZMK_USB=y", 'CONFIG_USB_DEVICE_PRODUCT="GridRoll"',
                     "# CONFIG_BT_CTLR_PHY_2M is not set",
                     "CONFIG_BT_PERIPHERAL_PREF_MIN_INT=6",
                     "CONFIG_BT_PERIPHERAL_PREF_MAX_INT=6",
                     "CONFIG_BT_PERIPHERAL_PREF_LATENCY=0",
                     "CONFIG_ZMK_STUDIO_TRANSPORT_BLE_PREF_LATENCY=0",
                     "CONFIG_GRIDROLL_PAW3222_BLE_REPORT_INTERVAL_MS=8"]:
            assert flag in config.splitlines(), f"{name}: missing {flag}"
        for flag in ["CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y",
                     "CONFIG_ZMK_STUDIO_LOCK_BLE_DIRECT_ADVERTISING_ON_UNLOCK=y"]:
            assert flag not in config.splitlines(), f"{name}: unwanted {flag}"
        assert not any(line.startswith("CONFIG_ZMK_STUDIO_LOCK_IDLE_TIMEOUT_SEC=")
                       for line in config.splitlines()), f"{name}: Studio idle locking enabled"
    if name=="left":
        assert "CONFIG_GRIDROLL_PRECISION=y" not in config.splitlines()
        assert "CONFIG_ZMK_LOW_PRIORITY_THREAD_STACK_SIZE=2048" in config.splitlines()
        assert "CONFIG_ZMK_USB=y" not in config.splitlines()
        assert "CONFIG_ZMK_SPLIT_ROLE_CENTRAL=y" not in config
        assert "CONFIG_ZMK_STUDIO=y" not in config
        assert "CONFIG_GRIDROLL_PAW3222=y" not in config
    if name=="settings-reset":
        assert "CONFIG_GRIDROLL_STATUS_LED=y" not in config.splitlines()
        assert "CONFIG_ZMK_BLE=y" not in config
        assert "CONFIG_ZMK_SETTINGS_RESET_ON_START=y" in config
    for ext in ["uf2","hex"]: shutil.copyfile(build/f"zephyr/zmk.{ext}",out/f"{stem}.{ext}")
    shutil.copyfile(build/"zephyr/.config",out/f"{stem}.config")
    shutil.copyfile(build/"zephyr/zephyr.dts",out/f"{stem}.dts")
    subprocess.run([sys.executable,str(ROOT/"scripts/check_addresses.py"),str(out/f"{stem}.hex"),
                    "--uf2",str(out/f"{stem}.uf2")],check=True)
