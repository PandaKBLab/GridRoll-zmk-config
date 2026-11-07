# LED and battery status / 指示灯与电量

Blue indicates the local charging cycle. Red indicates connection or low battery.
Normal connected use has no steady status light. The two halves have independent
batteries and blue charging indicators.

| State | Blue | Red |
|---|---|---|
| Normal first charging cycle | On, hardware controlled | Connection indication may run on the right |
| Normal first charge ends | Changes from on to off | No software full-charge indication |
| Waiting for the selected Bluetooth host | Charging hardware decides | Right: 100 ms on every 2 s, for at most 30 s |
| Selected host connects | Charging hardware decides | Right: on for 2 s, then off |
| Unexpected host disconnect | Charging hardware decides | Right: restarts the bounded waiting window |
| Local battery estimate at or below 15% | Off without USB | Each half: 100 ms on every 30 s; clears at 20% |
| USB output preferred and ready | Charging hardware decides | No waiting-for-Bluetooth flashes |
| Idle or deep sleep | Charging hardware decides | Off; LED work cancelled |

The **right red LED describes the computer-facing Bluetooth connection**, not
the left-to-right split link. The left red LED indicates only its own low battery.
Waiting begins at boot, wake, profile selection or an unexpected disconnect.
The waiting window ending does not stop Bluetooth advertising. Normal wired use
does not flash for an unused background Bluetooth profile; explicitly selecting
BLE while USB-powered enables connection indication again.

Low battery suppresses waiting flashes. A successful connection still receives
its short 2-second confirmation, then returns to the low-battery pattern.
Physical USB power suppresses low-battery warning on that half, including when
the cable only supplies power. Idle/sleep always switches red off and prevents
status events from waking the keyboard.

Battery levels use the existing ZMK sampler once per 60 seconds while active.
The measurement circuit is powered only during its sample, with the native
settling delay retained. Idle stops sampling, and wake starts the native sampler
again. A queued fetch is skipped if the keyboard has already entered idle.
No second ADC polling task is used for LEDs. A result hook records successful
fetches even if the percentage stays unchanged or is genuinely 0%; errors and
samples older than 180 seconds suppress the low-battery light. Wake waits for
a new valid sample rather than treating the initial cached 0% as a measurement.

USB power is detected from the MCU's existing hardware VBUS status on both
halves. The left retains its peripheral role and does not enable a USB data
stack. USB-powered halves avoid timed deep sleep; on battery, the existing
30-second idle / 15-minute deep sleep and matrix-key wake remain unchanged.
LED work never reports fake key, encoder or pointing input to keep the keyboard
awake. Normal connected red-off operation has no periodic LED work; the existing
ZMK activity timer and native battery schedule remain in use.

## Full charge is a hardware boundary

Blue going off **after a normal first charging cycle** is a useful everyday
reference. Blue also stays off during subsequent refresh charging and several
other conditions. It does not uniquely prove full charge. The existing hardware
does not provide the controller a charging-complete/current measurement, so the
firmware does not turn a voltage estimate of 100% into a definitive full-charge
signal. No full-charge red flash or steady red light is generated.
See [TI status definitions](https://www.ti.com/lit/ds/symlink/bq24075.pdf#page=28).

Battery percentages are voltage estimates, affected by charge, load and rest.
There is no independent battery-presence detector; a missing battery can produce
a plausible voltage reading. No battery temperature monitoring is added.

## 中文使用说明

- 蓝灯为本侧充电周期指示，正常首轮充电结束后由亮转灭；蓝灯灭不单独等于已充满。
- 右侧红灯慢闪表示等待电脑蓝牙连接，亮 2 秒后灭表示连接成功；正常连接后不常亮。
- 两侧红灯各自偶尔短闪表示本侧电池估算电量低。插 USB、空闲、休眠时关闭低电提醒。
- 等待慢闪最多持续 30 秒；灯灭后仍可以连接。开机、唤醒、切换蓝牙槽或意外断连时重新提示。
- 低电阈值为 ≤15%，恢复到 ≥20% 解除。没有有效采样时不把默认 0% 当低电。
- 普通更新保留配对、Studio 键位和 DYA 参数。本次两侧均加入电池和灯功能，应分别刷入左右固件；无需刷 reset。

Software regression and compiled configuration checks do not establish physical
visibility, calibrated battery accuracy, current consumption, sleep/wake or radio
reliability. Those require device tests. Both Studio interfaces remain unlocked.
