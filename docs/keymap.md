# Eight-layer default keymap / 八层默认键位

These are firmware source defaults, not a readback of a Studio-saved layout. Normal updates preserve saved keymaps. Export your layout before using Studio's restore-defaults operation if you want these defaults; a settings-reset flash is unnecessary and also clears pairing.

这是源码默认键位，普通更新不会覆盖 Studio 已保存的布局。需要采用本页八层时，先导出旧布局，再使用 Studio 恢复默认；无需刷 reset 清除配对。

Reference: [LiNEA40's seven-layer keymap](https://github.com/keyfreaks/zmk-config-LiNEA40/blob/6953ccb2e2d6256ed57887fde692bcb1959f9052/config/LiNEA40.keymap). Its inner 5+5 columns and bottom eleven bindings are adapted to GridRoll's existing 47 positions. Six outer keys provide Tab/System, Mouse, Shift, Backspace, Navigation and Enter. L7 is GridRoll's additional System layer. The original Japanese-keycode symbols are retained; emitted characters depend on the computer's keyboard layout. The original auto mouse layer, hardware driver and wheel acceleration are not imported.

Tap-hold keys: tap sends the displayed key; hold activates the indicated layer/modifier. `&trans` resolves to a lower active layer. Every layer is enabled and editable in both Studios. The trackball scrolls in L5; the encoder uses DYA runtime sensor rotation on all eight layers. Encoder press is position 39 (bottom-left half, column 3), default Insert.

| Layer | Purpose | Access from Base | Encoder CW / CCW |
|---|---|---|---|
| L0 Base | Typing / 基础输入 | Power-on default | Wheel down / Wheel up |
| L1 Mouse | Mouse buttons / 鼠标按键 | Hold left outer middle-row key | Wheel down / Wheel up |
| L2 Symbol | Symbols / 符号 | Hold bottom-row Tab or Backspace | Volume up / Volume down |
| L3 Nav | Navigation and numbers / 导航与数字 | Hold right outer middle-row key | Wheel down / Wheel up |
| L4 Function | Function and shortcuts / 功能与快捷键 | Hold bottom-row Space | Wheel down / Wheel up |
| L5 Scroll | Trackball scrolling / 轨迹球滚动 | Hold Enter or Minus | Down arrow / Up arrow |
| L6 Wireless | Bluetooth profiles / 蓝牙槽位 | Hold bottom-row ] | Right arrow / Left arrow |
| L7 System | Output and recovery / 输出与恢复 | Hold top-left Tab | Volume up / Volume down |

Right USB enumerated by a computer selects USB automatically, including after loading a saved BLE preference. A charge-only cable does not force USB. You can manually choose BLE while plugged in: hold top-left Tab (L7), press top-row U; Y selects USB and I toggles output. A new USB connection prefers USB again. Unplugging falls back to BLE when a host is connected.

## L0 Base

![L0 base keymap](keymap/layer-0.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&lt SYSTEM TAB` | `&kp Q` | `&kp W` | `&kp E` | `&kp R` | `&kp T` | `&kp Y` | `&kp U` | `&kp I` | `&kp O` | `&kp P` | `&kp BSPC` |
| 1 | `&mo MOUSE` | `&kp A` | `&kp S` | `&kp D` | `&kp F` | `&kp G` | `&kp H` | `&kp J` | `&kp K` | `&kp L` | `&lt SCROLL MINUS` | `&mo NAV` |
| 2 | `&kp LSHFT` | `&kp Z` | `&kp X` | `&kp C` | `&kp V` | `&kp B` | `&kp N` | `&kp M` | `&kp COMMA` | `&kp DOT` | `&mt RIGHT_SHIFT BACKSPACE` | `&kp RET` |
| 3 | `&mt LCTRL ESC` | `&kp LEFT_WIN` | `&mt LEFT_ALT GRAVE` | `&kp INS` | `&lt SCROLL ENTER` | `&lt SYMBOL TAB` | `&lt SYMBOL BACKSPACE` | `&lt FUNCTION SPACE` | — | `&lt WIRELESS RIGHT_BRACKET` | `&kp BACKSLASH` | `&mt RIGHT_SHIFT SLASH` |

## L1 Mouse

![L1 mouse keymap](keymap/layer-1.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` |
| 1 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&mkp MB1` | `&trans` | `&trans` | `&trans` | `&trans` |
| 2 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&trans` | `&trans` | `&trans` |

## L2 Symbol

![L2 symbol keymap](keymap/layer-2.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&kp EXCLAMATION` | `&kp AT` | `&kp HASH` | `&kp DOLLAR` | `&kp PERCENT` | `&kp CARET` | `&kp AMPERSAND` | `&kp ASTERISK` | `&kp LEFT_PARENTHESIS` | `&kp LBKT` | `&trans` |
| 1 | `&trans` | `&kp SLASH` | `&kp KP_NUMBER_4` | `&kp KP_NUMBER_5` | `&kp SEMICOLON` | `&kp SEMICOLON` | `&kp C_MUTE` | `&kp LS(LBKT)` | `&kp RIGHT_BRACKET` | `&kp BACKSLASH` | `&kp EQUAL` | `&trans` |
| 2 | `&trans` | `&mt LEFT_SHIFT KP_NUMBER_0` | `&kp KP_NUMBER_1` | `&kp KP_NUMBER_2` | `&kp APOS` | `&kp SQT` | `&kp KP_EQUAL` | `&kp INT3` | `&kp LS(RIGHT_BRACKET)` | `&kp LS(BACKSLASH)` | `&kp LS(INT1)` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&kp ASTERISK` | `&kp LEFT_PARENTHESIS` | `&kp LS(QUESTION)` |

## L3 Nav

![L3 nav keymap](keymap/layer-3.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&trans` | `&kp LC(LG(LEFT_ARROW))` | `&kp UP_ARROW` | `&kp LC(LG(RIGHT_ARROW))` | `&trans` | `&kp KP_MULTIPLY` | `&kp NUMBER_7` | `&kp NUMBER_8` | `&kp NUMBER_9` | `&kp KP_PLUS` | `&trans` |
| 1 | `&trans` | `&trans` | `&kp LEFT_ARROW` | `&kp DOWN` | `&kp RIGHT_ARROW` | `&trans` | `&kp KP_SLASH` | `&kp NUMBER_4` | `&kp NUMBER_5` | `&kp NUMBER_6` | `&kp KP_MINUS` | `&trans` |
| 2 | `&trans` | `&kp HOME` | `&kp PAGE_DOWN` | `&kp END` | `&kp PAGE_UP` | `&trans` | `&kp UNDER` | `&kp NUMBER_1` | `&kp NUMBER_2` | `&kp NUMBER_3` | `&kp ENTER` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&kp ENTER` | `&kp NUMBER_0` | — | `&kp DOT` | `&kp ENTER` | `&kp QUESTION` |

## L4 Function

![L4 function keymap](keymap/layer-4.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&kp F1` | `&kp F2` | `&kp F3` | `&kp F4` | `&kp F5` | `&trans` | `&trans` | `&kp LA(PRINTSCREEN)` | `&trans` | `&kp LC(LA(DELETE))` | `&trans` |
| 1 | `&trans` | `&kp F6` | `&kp F7` | `&kp F8` | `&kp F9` | `&kp F10` | `&trans` | `&trans` | `&kp LS(LG(S))` | `&trans` | `&kp LC(LS(ESCAPE))` | `&trans` |
| 2 | `&trans` | `&trans` | `&trans` | `&trans` | `&kp F11` | `&kp F12` | `&kp C_MUTE` | `&trans` | `&trans` | `&trans` | `&kp LC(LA(INS))` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&trans` | `&trans` | `&trans` |

## L5 Scroll

![L5 scroll keymap](keymap/layer-5.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&trans` | `&kp LC(LG(LEFT_ARROW))` | `&kp UP_ARROW` | `&kp LC(LG(RIGHT_ARROW))` | `&trans` | `&kp KP_MULTIPLY` | `&kp NUMBER_7` | `&kp NUMBER_8` | `&kp NUMBER_9` | `&kp KP_PLUS` | `&trans` |
| 1 | `&trans` | `&trans` | `&kp LEFT_ARROW` | `&kp DOWN` | `&kp RIGHT_ARROW` | `&trans` | `&kp KP_SLASH` | `&kp NUMBER_4` | `&kp NUMBER_5` | `&kp NUMBER_6` | `&kp KP_MINUS` | `&trans` |
| 2 | `&trans` | `&kp HOME` | `&kp PAGE_DOWN` | `&kp END` | `&kp PAGE_UP` | `&trans` | `&kp UNDER` | `&kp NUMBER_1` | `&kp NUMBER_2` | `&kp NUMBER_3` | `&kp ENTER` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&kp NUMBER_0` | — | `&kp NUMBER_0` | `&kp DOT` | `&kp QUESTION` |

## L6 Wireless

![L6 wireless keymap](keymap/layer-6.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&trans` | `&bt BT_SEL 0` | `&bt BT_SEL 1` | `&bt BT_SEL 2` | `&bt BT_SEL 3` | `&bt BT_SEL 4` | `&bt BT_SEL 0` | `&bt BT_SEL 1` | `&bt BT_SEL 2` | `&bt BT_SEL 3` | `&bt BT_SEL 4` | `&trans` |
| 1 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` |
| 2 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&bt BT_CLR` | `&trans` |
| 3 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&bootloader` | `&studio_unlock` | — | `&trans` | `&trans` | `&bt BT_CLR_ALL` |

## L7 System

![L7 system keymap](keymap/layer-7.svg)

Exact source bindings, viewed from the typing side; `—` is the trackball opening.

| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | `&to BASE` | `&bt BT_SEL 0` | `&bt BT_SEL 1` | `&bt BT_SEL 2` | `&bt BT_SEL 3` | `&bt BT_SEL 4` | `&out OUT_USB` | `&out OUT_BLE` | `&out OUT_TOG` | `&trans` | `&trans` | `&bt BT_CLR` |
| 1 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` |
| 2 | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` | `&trans` |
| 3 | `&bootloader` | `&sys_reset` | `&trans` | `&kp C_MUTE` | `&trans` | `&trans` | `&trans` | `&trans` | — | `&trans` | `&sys_reset` | `&bootloader` |

## Base-layer combos / 首层组合键

LiNEA40 combos are remapped to GridRoll positions and limited to L0, with a 30 ms chord window:

| Keys | Action |
|---|---|
| S + D | Grave / backtick |
| I + O | Delete |
| U + I | Insert |
| J + K | Middle click |
| K + L | Right click |
| Comma + Period | Mouse button 4 |
| M + Comma | Mouse button 5 |

Studio can change layer names/bindings, but the trackball scroll override still targets compiled layer 5. Keep layer indices stable when using that override. Actual encoder direction, DYA save/reconnect, USB switching, sleep/wake and host-layout characters require device verification.
