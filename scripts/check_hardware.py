#!/usr/bin/env python3
"""Guard the wiring contract and row-major 47-key layout."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "left": {"row": [(0,29),(0,31),(1,6),(0,26)],
             "col": [(1,11),(1,10),(0,3),(0,28),(1,13),(0,30)]},
    "right": {"row": [(1,4),(0,30),(0,29),(0,31)],
              "col": [(0,24),(1,6),(0,3),(1,11),(1,10),(0,28)]},
}
for side, pins in EXPECTED.items():
    text=(ROOT/f"boards/shields/gridroll/gridroll_{side}.overlay").read_text()
    all_pins=[]
    for kind, expected in pins.items():
        section=re.search(rf"{kind}-gpios\s*=\s*(.*?);",text,re.S).group(1)
        found=[(int(p),int(n)) for p,n in re.findall(r"&gpio([01])\s+(\d+)",section)]
        assert found==expected, (side,kind,found)
        assert section.count("GPIO_ACTIVE_HIGH")==len(expected)
        assert section.count("GPIO_PULL_DOWN")== (4 if kind=="row" else 0)
        all_pins+=found
    extras=[(0,13),(0,24)] if side=="left" else [(0,12),(1,9),(0,13),(0,15)]
    assert len(set(all_pins+extras))==len(all_pins+extras), f"{side}: pin conflict"
    assert not set(all_pins+extras)&{(0,9),(0,10),(0,4),(0,5),(0,8)}, "reserved pin used"
    assert f"col-offset = <{0 if side=='left' else 6}>" in text
layout=(ROOT/"boards/shields/gridroll/gridroll-layouts.dtsi").read_text()
mapping=[(int(r),int(c)) for r,c in re.findall(r"RC\((\d+),\s*(\d+)\)",layout)]
assert mapping==[(r,c) for r in range(4) for c in range(12) if (r,c)!=(3,8)]
assert mapping.count((3,3))==1
assert len(re.findall(r"&key_physical_attrs",layout))==47
keymap=(ROOT/"config/gridroll.keymap").read_text()
layers=keymap.split('compatible = "zmk,keymap";',1)[1]
for layer in ["base","mouse","lower","nav","raise","scroll","wireless","system"]:
    content=re.search(rf"\b{layer}\s*\{{(.*?)\n\s*\}};",layers,re.S).group(1)
    bindings=re.search(r"\bbindings\s*=\s*<(.*?)>;",content,re.S).group(1)
    assert len(re.findall(r"&\w+",bindings))==47, layer
assert 'status = "reserved"' not in keymap
assert len(re.findall(r'sensor-bindings = <&encoder_',keymap))==8
assert 'layers = <SCROLL>;' in keymap
assert 'cw-binding = <&wheel_down>;' in keymap
assert 'ccw-binding = <&wheel_up>;' in keymap
assert 'temp-layer-enabled;' in keymap and 'temp-layer = <MOUSE>;' in keymap
assert 'temp-layer-activation-delay-ms = <200>;' in keymap
assert 'temp-layer-deactivation-delay-ms = <1200>;' in keymap
assert 'if-layers = <LOWER RAISE>;' in keymap and 'then-layer = <SYSTEM>;' in keymap
assert '&lt MOUSE SPACE' in keymap
assert all(f'&mo {layer}' in keymap for layer in ['LOWER','RAISE','NAV','SCROLL','WIRELESS'])
assert 'combos {' not in keymap
mouse=re.search(r'\bmouse\s*\{(.*?)\n\s*\};',layers,re.S).group(1)
mouse_bindings=re.search(r'\bbindings\s*=\s*<(.*?)>;',mouse,re.S).group(1)
mouse_items=[re.sub(r'\s+',' ', '&'+b+p).strip() for b,p in re.findall(r'&(\w+)([^&]*)',mouse_bindings)]
assert mouse_items[19]=='&mkp LCLK' and mouse_items[20]=='&mkp RCLK'
right_overlay=(ROOT/'boards/shields/gridroll/gridroll_right.overlay').read_text()
for wheel in ['wheel_down','wheel_up','wheel_left','wheel_right']:
    assert f'device = <&{wheel}>;' in right_overlay, f'Missing wheel input listener: {wheel}'
assert 'diode-direction = "col2row"' in (ROOT/"boards/shields/gridroll/gridroll.dtsi").read_text()
assert 'wakeup-source;' in (ROOT/"boards/shields/gridroll/gridroll.dtsi").read_text()
shield=(ROOT/"boards/shields/gridroll/gridroll.dtsi").read_text()
for binding in ['zmk,battery = &vbat;', 'io-channels = <&adc 2>;',
                'output-ohms = <1000000>;', 'full-ohms = <3000000>;',
                'power-gpios = <&gpio0 5 GPIO_ACTIVE_HIGH>;',
                'gpios = <&gpio0 8 GPIO_ACTIVE_HIGH>;']:
    assert binding in shield, f'Battery/LED binding missing: {binding}'
print("GPIO order/flags, pin reservations/conflicts, 47-key transform, physical layout and 8 layers passed")
