#!/usr/bin/env python3
"""Render the eight source-default layers; --check rejects stale GitHub diagrams."""
import argparse
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["base", "mouse", "lower", "nav", "raise", "scroll", "wireless", "system"]
PURPOSE = ["Planck-style QWERTY / 基础输入", "Automatic mouse buttons / 自动鼠标层", "Symbols and F keys / 符号与功能键",
           "Navigation / 导航", "Numbers and F keys / 数字与功能键",
           "Trackball scrolling / 轨迹球滚动", "Bluetooth profiles / 蓝牙槽位", "Output and recovery / 输出与恢复"]
ACCESS = ["Power-on default", "Move ball; or hold right Space", "Hold Lower (left of left Space)",
          "Lower + bottom-left Ctrl position", "Hold Raise (right of right Space)", "Mouse + M; or Lower + right Space",
          "Raise + left Shift position", "Hold Lower + Raise"]
CW_CCW = {"encoder_scroll": ("Wheel down", "Wheel up"),
          "encoder_volume": ("Volume up", "Volume down"),
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
           "LSHFT": "LShift", "LEFT_SHIFT": "LShift", "LCTRL": "Ctrl", "LEFT_ALT": "Alt",
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
    doc = ["# Eight-layer default keymap / 八层默认键位", "",
           "These are firmware source defaults, not a readback of a Studio-saved layout. Normal updates preserve saved keymaps. Export your layout before using Studio's restore-defaults operation if you want these defaults; a settings-reset flash is unnecessary and also clears pairing.", "",
           "这是源码默认键位，普通更新不会覆盖 Studio 已保存的布局。需要采用本页八层时，先导出旧布局，再使用 Studio 恢复默认；无需刷 reset 清除配对。", "",
           "The conventional Planck QWERTY/Lower/Raise arrangement is adapted to GridRoll's existing 47 positions. No QMK implementation code is imported. Tab, Esc, Shift, punctuation and Enter are ordinary keys. Bottom row: Ctrl, Alt, GUI, encoder middle-click, Lower, Space, Space/Mouse, Raise, trackball opening, Left, Down, Right. Up is available on the navigation layers. Lower + Raise opens System. Previous LiNEA40 combos and Japanese-specific symbols are removed.", "",
           "Tap-hold keys: right Space taps Space and holds Mouse. `&trans` resolves to a lower active layer. Every layer is enabled and editable in both Studios. The trackball scrolls only in L5. Encoder press is position 39 (bottom-left half, column 3), default middle click. Rotation in Base uses discrete wheel events, one step per sensor trigger; it does not use a short timed mouse-scroll hold.", "",
           "Auto Mouse defaults: the first nonzero ball movement activates L1 immediately if no key was pressed during the last 200 ms. This 200 ms is a typing guard, not a required movement duration. The owned automatic layer exits 1200 ms after the last movement, wheel step or mouse/modifier release. Holding one or several mouse buttons/modifiers prevents timeout during dragging. A normal transparent typing key exits immediately; Esc also returns to Base. A manually held Mouse layer is not timed out by the automatic controller. There is no periodic idle polling.", "",
           "默认自动鼠标层：有效拨球立即进入 L1；最近 200ms 内按过键时暂不触发，避免打字误碰。停止拨球、滚轮及鼠标操作 1200ms 后退出；拖拽按住不退出。普通打字键立即退出，Esc 回基础层。J=左键、K=右键、H=中键、L=后退、分号=前进；U/I=滚轮上/下，O/P=横向左/右；按住 M 把轨迹球转为滚动。", "",
           "L1 Mouse left 41 means left row 4 / column 1 (one-based), the bottom-left Ctrl position, global position 36 / RC(3,0). Hold it for one quarter of the mouse processor's normal DYA speed; release restores normal speed. Base Ctrl is unchanged. Only mouse scaling changes: direction, scrolling, saved settings and sleep policy remain intact. The key adds no timer or flash writes; holding it protects the automatic Mouse layer from timeout.", "",
           "L1 左手 41（第 4 行第 1 列，最下排最左、基础层 Ctrl 位置）：按住为正常速度的 1/4，松开恢复；基础层仍是 Ctrl。已有 Studio 布局不会被刷机覆盖：在 L1 的这个位置选择 `Precision 0.25x (hold)` 并保存即可，无需恢复整套布局或刷 reset。", "",
           "Saved DYA values override firmware defaults independently of the saved keymap. For this update, set mouse Temp-layer enabled / layer 1 / activation guard 200 / deactivation 1200, and set Base encoder CW to wheel down and CCW to wheel up if older bindings remain. Save each change. Restoring only the Studio keymap does not reset DYA processor or encoder settings. Keep your speed/rotation settings and Bluetooth pairing.", "",
           "| Layer | Purpose | Access from Base | Encoder CW / CCW |", "|---|---|---|---|"]
    for index, (name, bindings, sensor) in enumerate(all_layers):
        doc.append(f"| L{index} {name.title()} | {PURPOSE[index]} | {ACCESS[index]} | {' / '.join(CW_CCW[sensor])} |")
    doc += ["", "Right USB enumerated by a computer selects USB automatically. A charge-only cable does not force USB. You can manually choose BLE while plugged in: hold Lower + Raise (L7), press top-row U; Y selects USB and I toggles output. A new USB connection prefers USB again. Unplugging falls back to BLE when a host is connected.", ""]
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
            "The stock layout has no typing combos. J and K remain ordinary letters on Base; they become mouse buttons only in Mouse/Scroll. Saved layouts and DYA settings remain user-controlled across updates.", "",
            "Studio can change layer names/bindings, but the trackball scroll override still targets compiled layer 5. Keep layer indices stable when using that override. Actual encoder direction, DYA save/reconnect, USB switching, sleep/wake and host-layout characters require device verification.", ""]
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
    print("Eight enabled layers: diagrams and all 376 key bindings match source")


if __name__ == "__main__":
    main()
