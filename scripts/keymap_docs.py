#!/usr/bin/env python3
"""Render four functional layers and four empty editable slots from source."""
import argparse
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["base", "mouse", "symbols", "function", "empty4", "empty5", "empty6", "empty7"]
PURPOSE = ["QWERTY / 基础输入", "Mouse and precision / 鼠标与精细移动",
           "Numbers and symbols / 数字符号", "Function, wireless and ball scroll / 功能与滚动"] + ["Empty / 空层"] * 4
ACCESS = ["Power-on default", "Move ball; or Function + B", "Hold Symbols, left of left Space",
          "Hold Fn, right of right Enter; or Mouse + M"] + ["Studio custom use only"] * 4
CW_CCW = {"encoder_scroll": ("Wheel up", "Wheel down"),
          "encoder_volume": ("Volume up", "Volume down"),
          "encoder_none": ("No action", "No action"),
          "encoder_arrows": ("Down arrow", "Up arrow"),
          "encoder_horizontal": ("Right arrow", "Left arrow")}


def layers():
    source = (ROOT / "config/gridroll.keymap").read_text()
    body = source.split('compatible = "zmk,keymap";', 1)[1].split("    behaviors {", 1)[0]
    result = []
    for name, block in re.findall(r"\n        (\w+) \{(.*?)\n        \};", body, re.S):
        raw = re.search(r"\bbindings\s*=\s*<(.*?)>;", block, re.S).group(1)
        bindings = [re.sub(r"\s+", " ", "&" + b + p).strip()
                    for b, p in re.findall(r"&(\w+)([^&]*)", raw)]
        assert len(bindings) == 47, name
        sensor = re.search(r"sensor-bindings = <&(\w+)>;", block).group(1)
        result.append((name, bindings, sensor))
    assert [x[0] for x in result] == EXPECTED
    return result


ALIASES = {"BACKSPACE": "Bksp", "BSPC": "Bksp", "RIGHT_SHIFT": "RShift",
           "LSHFT": "LShift", "RSHFT": "RShift", "LEFT_SHIFT": "LShift", "LCTRL": "Ctrl", "LEFT_ALT": "Alt",
           "LEFT_WIN": "Win", "ESC": "Esc", "SPACE": "Space", "ENTER": "Enter", "RET": "Enter",
           "TAB": "Tab", "LEFT_ARROW": "←", "RIGHT_ARROW": "→", "UP_ARROW": "↑",
           "DOWN_ARROW": "↓", "PAGE_DOWN": "PgDn", "PAGE_UP": "PgUp", "HOME": "Home",
           "END": "End", "DEL": "Delete", "INS": "Insert", "SLASH": "/", "FSLH": "/",
           "BACKSLASH": "\\", "BSLH": "\\", "COMMA": ",", "DOT": ".", "SQT": "'", "APOS": "'",
           "MINUS": "-", "EQUAL": "=", "EXCLAMATION": "!", "AT": "@", "HASH": "#", "DOLLAR": "$",
           "PERCENT": "%", "CARET": "^", "AMPERSAND": "&", "ASTERISK": "*", "UNDER": "_",
           "LEFT_PARENTHESIS": "(", "QUESTION": "?", "LBKT": "[", "RIGHT_BRACKET": "]",
           "SEMICOLON": ";", "GRAVE": "`", "C_MUTE": "Mute", "DELETE": "Del",
           "ESCAPE": "Esc", "PRINTSCREEN": "PrtSc", "KP_MULTIPLY": "Num *",
           "KP_SLASH": "Num /", "KP_PLUS": "Num +", "KP_MINUS": "Num -", "KP_EQUAL": "Num ="}


def code_label(code):
    modifiers = []
    while re.match(r"^(LC|LS|LA|LG)\(", code):
        prefix = code[:2]
        modifiers.append({"LC": "Ctrl", "LS": "Shift", "LA": "Alt", "LG": "Win"}[prefix])
        code = code[3:-1]
    code = re.sub(r"^(?:KP_NUMBER_|NUMBER_|N)(\d)$", r"\1", code)
    return "+".join(modifiers + [ALIASES.get(code, code)])


def label(binding):
    parts = binding.split()
    behavior, args = parts[0], parts[1:]
    if behavior == "&kp":
        return [code_label(args[0])]
    if behavior in ("&lt", "&mt"):
        return [code_label(args[1]), "hold " + ("L" + str(EXPECTED.index(args[0].lower()))
                if behavior == "&lt" else code_label(args[0]))]
    if behavior in ("&mo", "&to"):
        return [("Hold " if behavior == "&mo" else "Go ") + "L" + str(EXPECTED.index(args[0].lower()))]
    if behavior == "&trans":
        return ["TRNS"]
    if behavior == "&none":
        return ["—"]
    if behavior == "&bt":
        return ["BT " + args[1] if args[0] == "BT_SEL" else "Clear profile"]
    if behavior == "&out":
        return [{"OUT_USB": "USB", "OUT_BLE": "BLE", "OUT_TOG": "Toggle output"}[args[0]]]
    if behavior == "&mkp":
        return [{"MB1": "Left click", "MB2": "Right click", "MB3": "Middle click",
                 "LCLK": "Left click", "RCLK": "Right click", "MCLK": "Middle click",
                 "MB4": "Mouse 4", "MB5": "Mouse 5"}.get(args[0], args[0])]
    if behavior.startswith("&wheel_"):
        return [behavior[1:].replace("_", " ").title()]
    if behavior == "&precision_quarter":
        return ["Precision", "hold 0.25x"]
    if behavior == "&studio_ble":
        return ["Studio BLE", "discover 60s"]
    return [{"&bootloader": "Bootloader", "&sys_reset": "Reboot"}.get(behavior, binding)]


def diagram(index, name, bindings, sensor):
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="392" viewBox="0 0 1100 392">',
           '<rect width="1100" height="392" rx="12" fill="#f0f3f7"/>',
           f'<text x="24" y="31" font-family="sans-serif" font-size="21" fill="#15243b">L{index} · {name.title()}</text>',
           '<g font-family="sans-serif" fill="#15243b" text-anchor="middle">']
    position = 0
    for row in range(4):
        for col in range(12):
            x, y = 24 + col * 84 + (36 if col >= 6 else 0), 49 + row * 73
            if (row, col) == (3, 8):
                svg.append(f'<circle cx="{x+38}" cy="{y+31}" r="28" fill="#d8e1ed"/><text x="{x+38}" y="{y+35}" font-size="10">TRACKBALL</text>')
                continue
            binding = bindings[position]
            svg.append(f'<g><title>{escape(str(position)+": "+binding)}</title><rect x="{x}" y="{y}" width="77" height="63" rx="6" fill="white" stroke="#acb9cc"/>')
            for line_index, line in enumerate(label(binding)):
                size = round(min(13, 66 / max(1, len(line)) / 0.68), 1)
                svg.append(f'<text x="{x+38}" y="{y+26+line_index*17}" font-size="{size}">{escape(line)}</text>')
            svg.append(f'<text x="{x+9}" y="{y+55}" font-size="8" fill="#79879b">{position}</text></g>')
            position += 1
    cw, ccw = CW_CCW[sensor]
    svg += [f'<text x="550" y="365" font-size="14">Encoder CW: {cw} · CCW: {ccw} | hold = momentary; TRNS = lower active layer</text>',
            '</g></svg>\n']
    return "\n".join(svg)


def outputs():
    result = {}
    all_layers = layers()
    doc = [
        "# Four-layer default keymap / 四层默认键位",
        "",
        "Four functional layers (L0–L3) and four empty editable slots (L4–L7). All 47 physical positions and their matrix order are preserved. This page is generated from firmware source, not a readback of a Studio-saved layout.",
        "",
        "四个常用层 L0～L3，L4～L7 为空的可编辑预留层。基础层左手右下角是普通空格，右手左下角是普通回车；原第三行右侧回车位置改为右 Shift。左右最下排的层键分别是 Symbols 和 Function。",
        "",
        "Base bottom row, viewed while typing: Ctrl, Alt, GUI, encoder middle-click, Symbols, Space | Enter, Function, trackball opening, Left, Down, Right. Base Space/Enter are ordinary key presses, not tap-hold keys.",
        "",
        "Default native resolution is 798 CPI (about 800 DPI), the closest allowed 38-CPI step approved by the user. With DYA mouse scaling 1/1, precision is 199.5 effective CPI (about 200). The sensor remains 798 CPI; the precision behavior temporarily scales motion to one quarter of the current normal DYA speed.",
        "",
        "Auto Mouse: the first nonzero movement outside the 200 ms typing guard enables L1. Exit is 1200 ms after the last pointer/wheel/button activity; held mouse/modifier/precision keys prevent timeout. Ordinary transparent typing exits automatically; Esc returns to Base. Function+B enters Mouse manually and Esc leaves it. No idle polling is added.",
        "",
        "自动鼠标层：拨球进入 L1，打字保护 200ms；停止鼠标操作 1200ms 后退出，按住拖拽或精细键不会超时。J 左键、K 右键、H 中键、L 后退、分号前进；U/I 上下滚轮，O/P 横向滚轮。L1 左手第 4 行第 6 列（左空格位置，位置 41）按住为正常速度的 1/4，松开恢复。按住 M 进入 Function 并让轨迹球滚动；鼠标按键仍可使用。",
        "",
        "Symbols (L2): numbers 1–0 on the home row, common shifted symbols on the top row and brackets/operators below. Function (L3): F1–F12 on the top row; A/S/D/F/G select Bluetooth profiles 0–4; X selects USB, C selects BLE, V opens Studio discovery, B enters manual Mouse, Z clears only the selected host profile. The right home row retains mouse buttons, and its lower row provides navigation. The encoder scrolls CW up/CCW down in L0–L2, controls volume in L3, and does nothing in L4–L7.",
        "",
        "无线设置：先与当前电脑配对并使用蓝牙输出；Fn+C 选择 BLE，Fn+V 开放最长 60s 的 Studio 发现窗口，再点 DYA 的蓝牙连接并扫描。主机重新连接或从 USB 选择 BLE 也会短暂开放。空闲、USB 输出、断连或到期后关闭额外广播；普通鼠标活动不会反复续期，关闭广播不主动断开已有 GATT 连接。这不是解锁键，两种 Studio 始终免解锁。",
        "",
        "BLE discovery does not promise a physical Windows/browser connection result. The pinned firmware previously stopped advertising after the host connected. The fix uses a bounded window and advertises the Studio service in scan response while retaining HID/Battery/name in the primary packet. Normal pairing/reconnect remains available after the window. Keep BLE output selected for wireless Studio; use USB output for wired Studio. No artificial activity is generated to defeat sleep.",
        "",
        "Updates intentionally preserve pairing and saved Studio/DYA values. To adopt this full four-layer layout, first export the old layout, then use ZMK Studio's keymap Restore Stock Settings action and save. Do not flash settings-reset. Review DYA encoder assignments separately: L0–L2 wheel up/down, L3 volume up/down, L4–L7 no action; old encoder overrides survive a keymap restore. Keep mouse Temp-layer target 1 / guard 200 / expiry 1200 and normal scale 1/1 for about 800 DPI.",
        "",
        "采用新配列时先导出旧布局，再在 ZMK Studio 恢复默认键位并保存；不要刷 reset。DYA 旋钮参数独立保存：L0～L2 为 CW 上滚、CCW 下滚，L3 为音量加减，L4～L7 为无动作。旧参数需单独更新。电池 30s 空闲、15min 深睡与按键唤醒保留；BLE 设置期间也应及时保存，不用灯效或广播伪造活动阻止休眠。",
        "",
        "| Layer | Purpose | Access from Base | Encoder CW / CCW |",
        "|---|---|---|---|"
    ]
    for index, (name, bindings, sensor) in enumerate(all_layers):
        doc.append(f"| L{index} {name.title()} | {PURPOSE[index]} | {ACCESS[index]} | {' / '.join(CW_CCW[sensor])} |")
    doc += ["", "Right USB enumerated by a computer selects USB automatically. A charge-only cable does not force USB. Fn+C selects BLE while plugged in; Fn+X selects USB. A new USB connection prefers USB again; unplugging falls back to a connected BLE host.", ""]
    for index, (name, bindings, sensor) in enumerate(all_layers):
        path = f"docs/keymap/layer-{index}.svg"
        result[path] = diagram(index, name, bindings, sensor)
        doc += [f"## L{index} {name.title()}", "", f"![L{index} {name} keymap](keymap/layer-{index}.svg)", "",
                "Exact source bindings, viewed from the typing side; `—` is the trackball opening.", "",
                "| Row | Left 0 | Left 1 | Left 2 | Left 3 | Left 4 | Left 5 | Right 0 | Right 1 | Right 2 | Right 3 | Right 4 | Right 5 |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        pos = 0
        for row in range(4):
            cells = []
            for col in range(12):
                if (row, col) == (3, 8):
                    cells.append("—")
                else:
                    cells.append("`" + bindings[pos] + "`")
                    pos += 1
            doc.append("| " + str(row) + " | " + " | ".join(cells) + " |")
        doc.append("")
    doc += ["## Layer and settings notes", "",
            "The stock layout has no typing combos. J/K are letters on Base and mouse buttons on Mouse/Function. L4–L7 contain only &none bindings and no-action encoder defaults, not transparent copies of Base. No stock key activates these empty slots.", "",
            "Studio can edit all eight slots, but automatic Mouse targets compiled layer 1 and the trackball scroll override targets compiled layer 3. Keep those indices stable. Saved settings, physical motion, wireless Studio, sleep/wake and host-layout characters require device verification.", ""]
    result["docs/keymap.md"] = "\n".join(doc)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for relative, content in outputs().items():
        path = ROOT / relative
        if args.check:
            assert path.exists() and path.read_text() == content, f"Stale diagram/table: {relative}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    print("Four functional + four empty layers: diagrams and all 376 bindings match source")


if __name__ == "__main__":
    main()
