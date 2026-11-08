# Four-layer default keymap / 四层默认键位

Four functional layers (L0–L3) and four empty editable slots (L4–L7). All 47 physical positions and their matrix order are preserved. This page is generated from firmware source, not a readback of a Studio-saved layout.

四个常用层 L0～L3，L4～L7 为空的可编辑预留层。基础层左手右下角是普通空格，右手左下角是普通回车；原第三行右侧回车位置改为右 Shift。左右最下排的层键分别是 Symbols 和 Function。

Base bottom row, viewed while typing: Ctrl, Alt, GUI, encoder middle-click, Symbols, Space | Enter, Function, trackball opening, Left, Down, Right. Base Space/Enter are ordinary key presses, not tap-hold keys.

Default native resolution is 798 CPI (about 800 DPI), the closest allowed 38-CPI step approved by the user. With DYA mouse scaling 1/1, precision is 199.5 effective CPI (about 200). The sensor remains 798 CPI; the precision behavior temporarily scales motion to one quarter of the current normal DYA speed.

Auto Mouse: the first nonzero movement outside the 200 ms typing guard enables L1. Exit is 1200 ms after the last pointer/wheel/button activity; held mouse/modifier/precision keys prevent timeout. Ordinary transparent typing exits automatically; Esc returns to Base. Function+B enters Mouse manually and Esc leaves it. No idle polling is added.

自动鼠标层：拨球进入 L1，打字保护 200ms；停止鼠标操作 1200ms 后退出，按住拖拽或精细键不会超时。J 左键、K 右键、H 中键、L 后退、分号前进；U/I 上下滚轮，O/P 横向滚轮。L1 左手第 4 行第 6 列（左空格位置，位置 41）按住为正常速度的 1/4，松开恢复。按住 M 进入 Function 并让轨迹球滚动；鼠标按键仍可使用。

Symbols (L2): numbers 1–0 on the home row, common shifted symbols on the top row and brackets/operators below. Function (L3): F1–F12 on the top row; A/S/D/F/G select Bluetooth profiles 0–4; X selects USB, C selects BLE, V opens Studio discovery, B enters manual Mouse, Z clears only the selected host profile. The right home row retains mouse buttons, and its lower row provides navigation. The encoder scrolls CW up/CCW down in L0–L2, controls volume in L3, and does nothing in L4–L7.

无线设置：先与当前电脑配对并使用蓝牙输出；Fn+C 选择 BLE，Fn+V 开放最长 60s 的 Studio 发现窗口，再点 DYA 的蓝牙连接并扫描。主机重新连接或从 USB 选择 BLE 也会短暂开放。空闲、USB 输出、断连或到期后关闭额外广播；普通鼠标活动不会反复续期，关闭广播不主动断开已有 GATT 连接。这不是解锁键，两种 Studio 始终免解锁。

BLE discovery does not promise a physical Windows/browser connection result. The pinned firmware previously stopped advertising after the host connected. The fix uses a bounded window and advertises the Studio service in scan response while retaining HID/Battery/name in the primary packet. Normal pairing/reconnect remains available after the window. Keep BLE output selected for wireless Studio; use USB output for wired Studio. No artificial activity is generated to defeat sleep.

Updates intentionally preserve pairing and saved Studio/DYA values. To adopt this full four-layer layout, first export the old layout, then use ZMK Studio's keymap Restore Stock Settings action and save. Do not flash settings-reset. Review DYA encoder assignments separately: L0–L2 wheel up/down, L3 volume up/down, L4–L7 no action; old encoder overrides survive a keymap restore. Keep mouse Temp-layer target 1 / guard 200 / expiry 1200 and normal scale 1/1 for about 800 DPI.

采用新配列时先导出旧布局，再在 ZMK Studio 恢复默认键位并保存；不要刷 reset。DYA 旋钮参数独立保存：L0～L2 为 CW 上滚、CCW 下滚，L3 为音量加减，L4～L7 为无动作。旧参数需单独更新。电池 30s 空闲、15min 深睡与按键唤醒保留；BLE 设置期间也应及时保存，不用灯效或广播伪造活动阻止休眠。

| Layer | Purpose | Access from Base | Encoder CW / CCW |
|---|---|---|---|
| L0 Base | QWERTY / 基础输入 | Power-on default | Wheel up / Wheel down |
| L1 Mouse | Mouse and precision / 鼠标与精细移动 | Move ball; or Function + B | Wheel up / Wheel down |
| L2 Symbols | Numbers and symbols / 数字符号 | Hold Symbols, left of left Space | Wheel up / Wheel down |
| L3 Function | Function, wireless and ball scroll / 功能与滚动 | Hold Fn, right of right Enter; or Mouse + M | Volume up / Volume down |
| L4 Empty4 | Empty / 空层 | Studio custom use only | No action / No action |
| L5 Empty5 | Empty / 空层 | Studio custom use only | No action / No action |
| L6 Empty6 | Empty / 空层 | Studio custom use only | No action / No action |
| L7 Empty7 | Empty / 空层 | Studio custom use only | No action / No action |

Right USB enumerated by a computer selects USB automatically. A charge-only cable does not force USB. Fn+C selects BLE while plugged in; Fn+X selects USB. A new USB connection prefers USB again; unplugging falls back to a connected BLE host.

## L0 Base

![L0 base keymap](keymap/layer-0.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&kp TAB` | `&kp Q` | `&kp W` | `&kp E` | `&kp R` | `&kp T` | `&kp Y` | `&kp U` | `&kp I` | `&kp O` | `&kp P` | `&kp BSPC` |
| 1 | `&kp ESC` | `&kp A` | `&kp S` | `&kp D` | `&kp F` | `&kp G` | `&kp H` | `&kp J` | `&kp K` | `&kp L` | `&kp SEMI` | `&kp SQT` |
| 2 | `&kp LSHFT` | `&kp Z` | `&kp X` | `&kp C` | `&kp V` | `&kp B` | `&kp N` | `&kp M` | `&kp COMMA` | `&kp DOT` | `&kp FSLH` | `&kp RSHFT` |
| 3 | `&kp LCTRL` | `&kp LALT` | `&kp LGUI` | `&mkp MCLK` | `&mo SYMBOLS` | `&kp SPACE` | `&kp RET` | `&mo FUNCTION` | — | `&kp LEFT` | `&kp DOWN` | `&kp RIGHT` |

## L1 Mouse

![L1 mouse keymap](keymap/layer-1.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&wheel_up` | `&wheel_down` | `&wheel_left` | `&wheel_right` | `&trans` |
| 1 | `&to BASE` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&mkp MCLK` | `&mkp LCLK` | `&mkp RCLK` | `&mkp MB4` | `&mkp MB5` | `&trans` |
| 2 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&mo FUNCTION` | `&trans` | `&trans` | `&trans` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&precision_quarter` | `&trans` | `&trans` | — | `&trans` | `&trans` | `&trans` |

## L2 Symbols

![L2 symbols keymap](keymap/layer-2.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&kp TILDE` | `&kp EXCL` | `&kp AT` | `&kp HASH` | `&kp DOLLAR` | `&kp PRCNT` | `&kp CARET` | `&kp AMPS` | `&kp ASTRK` | `&kp LPAR` | `&kp RPAR` | `&trans` |
| 1 | `&kp DEL` | `&kp N1` | `&kp N2` | `&kp N3` | `&kp N4` | `&kp N5` | `&kp N6` | `&kp N7` | `&kp N8` | `&kp N9` | `&kp N0` | `&kp GRAVE` |
| 2 | `&trans` | `&kp LBKT` | `&kp RBKT` | `&kp LBRC` | `&kp RBRC` | `&kp PIPE` | `&kp MINUS` | `&kp EQUAL` | `&kp PLUS` | `&kp UNDER` | `&kp BSLH` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&trans` | `&trans` | `&trans` |

## L3 Function

![L3 function keymap](keymap/layer-3.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&kp F1` | `&kp F2` | `&kp F3` | `&kp F4` | `&kp F5` | `&kp F6` | `&kp F7` | `&kp F8` | `&kp F9` | `&kp F10` | `&kp F11` | `&kp F12` |
| 1 | `&to BASE` | `&bt BT_SEL 0` | `&bt BT_SEL 1` | `&bt BT_SEL 2` | `&bt BT_SEL 3` | `&bt BT_SEL 4` | `&mkp MCLK` | `&mkp LCLK` | `&mkp RCLK` | `&mkp MB4` | `&mkp MB5` | `&kp DEL` |
| 2 | `&trans` | `&bt BT_CLR` | `&out OUT_USB` | `&out OUT_BLE` | `&studio_ble` | `&to MOUSE` | `&kp HOME` | `&kp LEFT` | `&kp DOWN` | `&kp UP` | `&kp RIGHT` | `&kp END` |
| 3 | `&trans` | `&trans` | `&trans` | `&kp C_MUTE` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&kp C_PREV` | `&kp C_VOL_DN` | `&kp C_VOL_UP` |

## L4 Empty4

![L4 empty4 keymap](keymap/layer-4.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 1 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 2 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 3 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | — | `&none` | `&none` | `&none` |

## L5 Empty5

![L5 empty5 keymap](keymap/layer-5.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 1 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 2 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 3 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | — | `&none` | `&none` | `&none` |

## L6 Empty6

![L6 empty6 keymap](keymap/layer-6.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 1 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 2 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 3 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | — | `&none` | `&none` | `&none` |

## L7 Empty7

![L7 empty7 keymap](keymap/layer-7.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 1 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 2 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` |
| 3 | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | `&none` | — | `&none` | `&none` | `&none` |

## Layer and settings notes

The stock layout has no typing combos. J/K are letters on Base and mouse buttons on Mouse/Function. L4–L7 contain only &none bindings and no-action encoder defaults, not transparent copies of Base. No stock key activates these empty slots.

Studio can edit all eight slots, but automatic Mouse targets compiled layer 1 and the trackball scroll override targets compiled layer 3. Keep those indices stable. Saved settings, physical motion, wireless Studio, sleep/wake and host-layout characters require device verification.
