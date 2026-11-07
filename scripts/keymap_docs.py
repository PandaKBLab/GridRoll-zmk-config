#!/usr/bin/env python3
"""Render the eight source-default layers; --check rejects stale GitHub diagrams."""
import argparse
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["base", "mouse", "symbol", "nav", "function", "scroll", "wireless", "system"]
PURPOSE = ["Typing / 基础输入", "Mouse buttons / 鼠标按键", "Symbols / 符号",
           "Navigation and numbers / 导航与数字", "Function and shortcuts / 功能与快捷键",
           "Trackball scrolling / 轨迹球滚动", "Bluetooth profiles / 蓝牙槽位", "Output and recovery / 输出与恢复"]
ACCESS = ["Power-on default", "Hold left outer middle-row key", "Hold bottom-row Tab or Backspace",
          "Hold right outer middle-row key", "Hold bottom-row Space", "Hold Enter or Minus",
          "Hold bottom-row ]", "Hold top-left Tab"]
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
           "TAB": "Tab", "LEFT_ARROW": "Left", "RIGHT_ARROW": "Right", "UP_ARROW": "Up",
           "DOWN_ARROW": "Down", "PAGE_DOWN": "PgDn", "PAGE_UP": "PgUp", "HOME": "Home",
           "END": "End", "DEL": "Delete", "INS": "Insert", "SLASH": "/", "FSLH": "/",
           "BACKSLASH": "\\", "BSLH": "\\", "COMMA": ",", "DOT": ".", "SQT": "'", "APOS": "'",
           "MINUS": "-", "EQUAL": "=", "EXCLAMATION": "!", "AT": "@", "HASH": "#", "DOLLAR": "$",
           "PERCENT": "%", "CARET": "^", "AMPERSAND": "&", "ASTERISK": "*", "UNDER": "_",
           "LEFT_PARENTHESIS": "(", "QUESTION": "?", "LBKT": "[", "RIGHT_BRACKET": "]",
           "SEMICOLON": ";", "GRAVE": "`", "C_MUTE": "Mute"}


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
        return ["TRANSPARENT"]
    if behavior == "&bt":
        return ["BT " + args[1] if args[0] == "BT_SEL" else "Clear profile"]
    if behavior == "&out":
        return [{"OUT_USB": "USB", "OUT_BLE": "BLE", "OUT_TOG": "Toggle output"}[args[0]]]
    if behavior == "&mkp":
        return [{"MB1": "Left click", "MB2": "Right click", "MB3": "Middle click",
                 "MB4": "Mouse 4", "MB5": "Mouse 5"}.get(args[0], args[0])]
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
                size = 10 if len(line) > 12 else 13
                svg.append(f'<text x="{x+38}" y="{y+26+line_index*17}" font-size="{size}">{escape(line)}</text>')
            svg.append(f'<text x="{x+9}" y="{y+55}" font-size="8" fill="#79879b">{position}</text></g>')
            position += 1
    cw, ccw = CW_CCW[sensor]
    svg += [f'<text x="550" y="365" font-size="14">Encoder CW: {cw} · CCW: {ccw} | hold = momentary; TRANSPARENT = lower active layer</text>',
            '</g></svg>\n']
    return "\n".join(svg)


def outputs():
    result = {}
    all_layers = layers()
    doc = ["# Eight-layer default keymap / 八层默认键位", "",
           "These are firmware source defaults, not a readback of a Studio-saved layout. Normal updates preserve saved keymaps. Export your layout before using Studio's restore-defaults operation if you want these defaults; a settings-reset flash is unnecessary and also clears pairing.", "",
           "这是源码默认键位，普通更新不会覆盖 Studio 已保存的布局。需要采用本页八层时，先导出旧布局，再使用 Studio 恢复默认；无需刷 reset 清除配对。", "",
           "Reference: [LiNEA40's seven-layer keymap](https://github.com/keyfreaks/zmk-config-LiNEA40/blob/6953ccb2e2d6256ed57887fde692bcb1959f9052/config/LiNEA40.keymap). Its inner 5+5 columns and bottom eleven bindings are adapted to GridRoll's existing 47 positions. Six outer keys provide Tab/System, Mouse, Shift, Backspace, Navigation and Enter. L7 is GridRoll's additional System layer. The original Japanese-keycode symbols are retained; emitted characters depend on the computer's keyboard layout. The original auto mouse layer, hardware driver and wheel acceleration are not imported.", "",
           "Tap-hold keys: tap sends the displayed key; hold activates the indicated layer/modifier. `&trans` resolves to a lower active layer. Every layer is enabled and editable in both Studios. The trackball scrolls in L5; the encoder uses DYA runtime sensor rotation on all eight layers. Encoder press is position 39 (bottom-left half, column 3), default Insert.", "",
           "| Layer | Purpose | Access from Base | Encoder CW / CCW |", "|---|---|---|---|"]
    for index, (name, bindings, sensor) in enumerate(all_layers):
        doc.append(f"| L{index} {name.title()} | {PURPOSE[index]} | {ACCESS[index]} | {' / '.join(CW_CCW[sensor])} |")
    doc += ["", "Right USB enumerated by a computer selects USB automatically, including after loading a saved BLE preference. A charge-only cable does not force USB. You can manually choose BLE while plugged in: hold top-left Tab (L7), press top-row U; Y selects USB and I toggles output. A new USB connection prefers USB again. Unplugging falls back to BLE when a host is connected.", ""]
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
    doc += ["## Base-layer combos / 首层组合键", "",
            "LiNEA40 combos are remapped to GridRoll positions and limited to L0, with a 30 ms chord window:", "",
            "| Keys | Action |", "|---|---|", "| S + D | Grave / backtick |", "| I + O | Delete |",
            "| U + I | Insert |", "| J + K | Middle click |", "| K + L | Right click |",
            "| Comma + Period | Mouse button 4 |", "| M + Comma | Mouse button 5 |", "",
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
