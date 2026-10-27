# MBB

## Log header (`0xFB`)

Entry offsets (equal to file offsets once the entry is un-escaped).

| Offset<br>117 B | Offset<br>115 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 1 | `u8` | `sof` | `0xB2` |
| `0x01` | `0x01` | 1 | `u8` | `length` | Entry length on disk, including header and escape bytes |
| `0x02` | `0x02` | 1 | `u8` | `type` | `0xFB` |
| `0x03` | `0x03` | 4 | `u32` | `timestamp` | Download time, Unix seconds, UTC |
| `0x07` | `0x07` | 4 | `u32` | `usec` | Microseconds |
| `0x0B` | `0x0B` | 1 | `u8` | `count` | Rolling entry counter |
| `0x0C` | `0x0C` | 1 | `s8` | `utc_offset` | UTC offset, hours |
| `0x0D` | `0x0D` | 10 | `char[10]` | `device_name` | `MBB` |
| `0x17` | `0x17` | 2 | `u16` | `mfg_version` | Manufacturing version, model year × 10 (e.g. `20230`) |
| `0x19` | `0x19` | 16 | `char[16]` | `model` | Model (e.g. `SRS`, `DSRX`) |
| `0x29` | `0x29` | 19 | `char[19]` | `vin` | VIN, 17 characters + NUL padding |
| `0x3C` | `0x3C` | 32 | `char[32]` | `serial` | MBB serial number |
| `0x5C` | `0x5C` | 9 | `char[9]` | `board_part` | Board part number (e.g. `40-08198`). 115-byte header: binary value, not a string |
| `0x65` | `0x65` | 2 | `u16` | `board_id` | Board revision. 0–5 valid, `0xFF` unknown |
| `0x67` | `0x67` | 2 | `u16` | `fw_rev_num` | Firmware revision (e.g. `41` for `75-08163-41`) |
| `0x69` | — | 2 | `u16` | `fw_build_num` | Firmware build/package number |
| `0x6B` | `0x69` | 10 | `char[10]` | `fw_commit_hash` | Firmware git commit hash |

| Header length | Firmware |
|---|---|
| 117 (`0x75`) | rev 13 and later |
| 115 (`0x73`) | rev 6–11 |

## Entry types

| Type | Name | Payload (bytes) | Description | Layout |
|---|---|---|---|---|
| `0x46` | `bms_status` | 53 | BMS module status | [Status](status.md#0x46-bms_status) |
| `0x47` | `precharge_status` | 22 | Precharge status | [Status](status.md#0x47-precharge_status) |
| `0x48` | `charger_details` | 49 | Charger module details | [Charging](charging.md#0x48-charger_details) |
| `0x49` | `charging_state` | 25 | Charging state | [Charging](charging.md#0x49-charging_state) |
| `0x4A` | `elock_status` | 13 | Electronic lock status | [Status](status.md#0x4a-elock_status) |
| `0x4B` | `periodic_small` | 40 | Periodic snapshot, small, first generation | [Periodic](periodic.md#0x4b-periodic_small) |
| `0x4C` | `periodic_medium` | 71 / 74 | Periodic snapshot, medium, first generation | [Periodic](periodic.md#0x4c-periodic_medium) |
| `0x4D` | `periodic_large` | 83 / 86 | Periodic snapshot, large, first generation | [Periodic](periodic.md#0x4d-periodic_large) |
| `0x4E` | `firmware_updated` | 54 / 52 | Firmware updated | [Events](events.md#0x4e-firmware_updated) |
| `0x4F` | `queue_send_fail` | 18 | RTOS queue send failure | [Faults](faults.md#0x4f-queue_send_fail) |
| `0x50` | `mcu_fault` | 25 | MCU fault registers | [Faults](faults.md#0x50-mcu_fault) |
| `0x51` | `periodic_small2` | 62 / 58 | Periodic snapshot, small | [Periodic](periodic.md#0x51-periodic_small2) |
| `0x52` | `periodic_medium2` | 79 / 75 | Periodic snapshot, medium | [Periodic](periodic.md#0x52-periodic_medium2) |
| `0x53` | `periodic_large2` | 93 / 89 | Periodic snapshot, large | [Periodic](periodic.md#0x53-periodic_large2) |
| `0x54` | `torque_info` | 16 | Torque and power snapshot | [Periodic](periodic.md#0x54-torque_info) |
| `0xFB` | `log_header` | 104 | Log header (first entry of the file) | [Log header](#log-header-0xfb) |
| `0xFD` | `debug_message` | ≤ 115 | Text message | [Events](events.md#0xfd-debug_message) |

Payload sizes given as `a / b` have two firmware variants, selected by payload length.
See [Firmware versions](../firmware.md).
