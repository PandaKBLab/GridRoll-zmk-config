#!/usr/bin/env python3
"""Check DYA's protobuf wire contract against the locked firmware modules.

Message/field names and proto packages may differ without changing the wire.
Compare numeric tags, scalar types, repeatedness, nested messages and enums,
then cross-decode real processor read/write messages. This is a software check,
not a browser/device connection test.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import time
from urllib.request import Request, urlopen

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory
from grpc_tools import protoc

ROOT = Path(__file__).resolve().parents[1]


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def download(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "GridRoll-protocol-check"}),
                         timeout=20) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def load_schema(data, folder):
    folder.mkdir()
    source = folder / "contract.proto"
    source.write_bytes(data)
    output = folder / "contract.pb"
    rc = protoc.main(["protoc", f"-I{folder}", f"--descriptor_set_out={output}", str(source)])
    assert rc == 0, "Protocol descriptor generation failed"
    file = descriptor_pb2.FileDescriptorSet.FromString(output.read_bytes()).file[0]
    pool = descriptor_pool.DescriptorPool()
    pool.Add(file)
    messages = {"." + file.package + "." + m.name: m for m in file.message_type}
    enums = {"." + file.package + "." + e.name: e for e in file.enum_type}
    return file.package, pool, messages, enums


def check_wire(frontend, firmware):
    seen = set()
    field_count = 0

    def compare(left_name, right_name):
        nonlocal field_count
        if (left_name, right_name) in seen:
            return
        seen.add((left_name, right_name))
        left, right = frontend[2][left_name], firmware[2][right_name]
        right_fields = {f.number: f for f in right.field}
        for lf in left.field:
            rf = right_fields.get(lf.number)
            assert rf is not None, f"Missing firmware field: {left_name} tag {lf.number}"
            assert lf.type == rf.type, f"Wire type mismatch: {left_name} tag {lf.number}"
            assert (lf.label == 3) == (rf.label == 3), f"Repeatedness mismatch: {left_name}"
            field_count += 1
            if lf.type == 11:  # TYPE_MESSAGE
                compare(lf.type_name, rf.type_name)
            elif lf.type == 14:  # TYPE_ENUM
                lv = {v.number for v in frontend[3][lf.type_name].value}
                rv = {v.number for v in firmware[3][rf.type_name].value}
                assert lv <= rv, f"Unsupported enum values: {left_name} tag {lf.number}"

    for name in ("Request", "Response", "Notification"):
        if name == "Notification" and "." + frontend[0] + "." + name not in frontend[2]:
            continue
        compare("." + frontend[0] + "." + name, "." + firmware[0] + "." + name)
    return len(seen), field_count


def message(schema, name):
    return message_factory.GetMessageClass(
        schema[1].FindMessageTypeByName(schema[0] + "." + name))()


def field(msg, tag):
    return getattr(msg, msg.DESCRIPTOR.fields_by_number[tag].name)


def cross_decode_processor(frontend, firmware):
    request = message(frontend, "Request")
    field(request, 4).id = 1
    field(request, 4).value = 60
    decoded = message(firmware, "Request")
    decoded.ParseFromString(request.SerializeToString())
    assert field(decoded, 4).id == 1 and field(decoded, 4).value == 60
    response = message(firmware, "Response")
    processor = field(field(response, 3), 1)
    processor.id, processor.name = 1, "mouse"
    processor.scale_multiplier, processor.scale_divisor = 1, 60
    decoded = message(frontend, "Response")
    decoded.ParseFromString(response.SerializeToString())
    processor = field(field(decoded, 3), 1)
    assert (processor.id, processor.name, processor.scale_divisor) == (1, "mouse", 60)


def cross_decode_encoder(frontend, firmware):
    # The last of eight layers must remain addressable through DYA's RPC.
    request = message(frontend, "Request")
    write = request.set_layer_cw_binding
    write.sensor_index, write.layer = 0, 7
    write.binding.behavior_id, write.binding.param1, write.binding.tap_ms = 42, 65526, 20
    decoded = message(firmware, "Request")
    decoded.ParseFromString(request.SerializeToString())
    write = decoded.set_layer_cw_binding
    assert (write.sensor_index, write.layer, write.binding.param1, write.binding.tap_ms) == (0, 7, 65526, 20)
    response = message(firmware, "Response")
    for layer in range(8):
        binding = response.get_all_layer_bindings.bindings.add()
        binding.layer = layer
        binding.cw_binding.behavior_id, binding.cw_binding.param1 = 42, 65526
        binding.ccw_binding.behavior_id, binding.ccw_binding.param1 = 42, 10
        binding.cw_binding.tap_ms = binding.ccw_binding.tap_ms = 20
    decoded = message(frontend, "Response")
    decoded.ParseFromString(response.SerializeToString())
    bindings = decoded.get_all_layer_bindings.bindings
    assert len(bindings) == 8 and bindings[-1].layer == 7
    assert bindings[-1].cw_binding.param1 == 65526 and bindings[-1].ccw_binding.param1 == 10
    response = message(firmware, "Response")
    sensor = response.get_sensors.sensors.add()
    sensor.index, sensor.name = 0, "encoder"
    decoded.ParseFromString(response.SerializeToString())
    assert decoded.get_sensors.sensors[0].name == "encoder"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    contract = json.loads((ROOT / "ci/studio-compatibility.json").read_text())
    with tempfile.TemporaryDirectory() as temporary:
        for entry in contract["protocols"]:
            frontend_data = download("https://raw.githubusercontent.com/cormoran/dya-studio/"
                                     + contract["dya_commit"] + "/" + entry["frontend_path"])
            firmware_data = (args.workspace / entry["firmware_path"]).read_bytes()
            assert blob_sha(frontend_data) == entry["frontend_blob"], "DYA snapshot mismatch"
            assert blob_sha(firmware_data) == entry["firmware_blob"], "Firmware pin mismatch"
            base = Path(temporary)
            frontend = load_schema(frontend_data, base / (entry["name"] + "-frontend"))
            firmware = load_schema(firmware_data, base / (entry["name"] + "-firmware"))
            messages, fields = check_wire(frontend, firmware)
            if entry["name"] == "runtime_input_processor":
                cross_decode_processor(frontend, firmware)
                handler = (args.workspace / "zmk-module-runtime-input-processor"
                           / "src/studio/custom_handler.c").read_text()
                assert "ZMK_RPC_CUSTOM_SUBSYSTEM(cormoran_rip," in handler
            if entry["name"] == "runtime_sensor_rotate":
                cross_decode_encoder(frontend, firmware)
                handler = (args.workspace / "zmk-behavior-runtime-sensor-rotate"
                           / "src/studio/custom_handler.c").read_text()
                assert "ZMK_RPC_CUSTOM_SUBSYSTEM(cormoran_rsr," in handler
            print(f"DYA {entry['name']}: {messages} messages / {fields} fields compatible")
    print("DYA Studio protocol and processor read/write cross-decoding passed")


if __name__ == "__main__":
    main()
