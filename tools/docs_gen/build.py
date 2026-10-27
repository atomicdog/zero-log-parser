"""Writes the datasheet pages into <repo>/docs. Usage: python tools/docs_gen/build.py [repo]

The pages under docs/ are generated; edit this file and rerun instead of editing them.
"""
import sys
from pathlib import Path
from spec import F, table, bits, values

OUT = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]) / 'docs'
PAGES = {}


def page(path, text):
    PAGES[path] = text.strip() + '\n'


ENTRY_HEADER = [
    F('sof', 'u8', '`0xB2`'),
    F('length', 'u8', 'Entry length on disk, including header and escape bytes'),
    F('type', 'u8', '`0xFB`'),
    F('timestamp', 'u32', 'Download time, Unix seconds, UTC'),
    F('usec', 'u32', 'Microseconds'),
    F('count', 'u8', 'Rolling entry counter'),
    F('utc_offset', 's8', 'UTC offset, hours'),
]

# --------------------------------------------------------------------------
# Common pages
# --------------------------------------------------------------------------

page('index.md', """
# Zero Gen3 Log Format

Binary event-log format written by the Gen3 (FST platform) Main Bike Board (MBB) and
Battery Management Unit (BMU/BMS), as downloaded through the Zero app.

| ECU | Log file | Entry types |
|---|---|---|
| MBB | 131,200 bytes | `0x46`–`0x54`, `0xFB`, `0xFD` |
| BMS | 131,328 bytes | `0x4B`–`0x8D`, `0xFB`, `0xFD` |

The MBB and BMS use separate type-code spaces. Several codes (`0x4B`–`0x54`) exist in
both with unrelated layouts; select the table by the file's ECU.

## Conventions

| Item | Convention |
|---|---|
| Byte order | Little-endian |
| Offsets | Hexadecimal, relative to the start of the payload (after the 13-byte entry header) unless stated otherwise. All offsets apply after un-escaping. |
| Sizes | Decimal bytes |
| `u8` `u16` `u32` `u64` | Unsigned integers |
| `s8` `s16` `s32` | Signed (two's complement) integers |
| `u24` | 3-byte unsigned integer |
| `char[n]` | Fixed-width ASCII, NUL-padded |
| `bytes[n]` | Fixed-width raw bytes |
| `—` | Field not present in that variant |

## Contents

- [File format](file-format.md): file sizes, block layout, BMS download stamp
- [Entry framing](framing.md): 13-byte entry header and byte stuffing
- [MBB](mbb/index.md): header and entry types
- [BMS](bms/index.md): header and entry types
- [Firmware versions](firmware.md): payload sizes by firmware revision
""")

page('file-format.md', """
# File Format

## Identification

| File size | First bytes¹ | `00 F0 FF 00` at each 128-byte block start | Content |
|---|---|---|---|
| 131,200 (1025 × 128) | `B2 75 FB` | No | MBB log |
| 131,200 (1025 × 128) | `B2 73 FB` | No | MBB log, firmware rev 6–11 header |
| 16,384 (128 × 128) | `B2 75 FB` | No | MBB log, smaller download window |
| 131,328 (1026 × 128) | `B2 7D FB` | Yes (blocks 1–1025) | BMS log |
| 131,200 (1025 × 128) | BMS header | No | BMS log, 2019–20 SR/F |

¹ After un-escaping. If the header entry contains an escape, the raw length byte is one
higher (`B2 76 FB`, `B2 7E FB`, …) and all later header bytes are shifted. Un-escape the
header entry before reading it.

Files are always a whole number of 128-byte blocks; a size that is not a multiple of 128
is not this format. Partial downloads have other sizes. The file content, not its name or
size, identifies the ECU.

## Block layout

| Block | MBB | BMS |
|---|---|---|
| 0 | Log header entry (`0xFB`), zero-padded to 128 bytes | Log header entry (`0xFB`), zero-padded to 128 bytes |
| 1–1024 | Most recent `0x20000` bytes of the log ring buffer | Most recent `0x20000` bytes of the log ring buffer, with download stamp |
| 1025 | — | Pad block (complete downloads only) |

The log header entry is generated at download time. It is not stored in the log.

### Ring buffer

| Parameter | MBB | BMS |
|---|---|---|
| Flash region | `0x001000`–`0xE80000` | `0x001000`–`0x1000000` |
| Erased byte | `0xFF` | `0xFF` |

- Erased bytes (`0xFF`) mark the write pointer.
- After a wrap, the data following the erased region is older than the data before it.
  File order is not time order; sort entries by timestamp.
- The entry at the write pointer may be truncated.
- Bytes between the end of one entry and the next `0xB2` are not part of any entry.

### BMS download stamp

In BMS files, bytes 0–3 of every block from block 1 onward read `00 F0 FF 00`. The
original 4 log bytes at those positions are lost.

| Entry position relative to stamp | Appearance |
|---|---|
| Starts at block byte 127 | `B2 00 F0 …` (length 0) |
| Starts at block byte 126 | Type `0x00`; timestamp low 3 bytes `F0 FF 00` |
| Starts at block bytes 0–3 | No `B2`/length; not framed |
| Spans a block start | Framing intact; 4 payload or header bytes replaced |
| Stamp covers an `0xFE` escape | Rest of the entry decodes 1 byte out of alignment |

### BMS pad block

| Offset | Size | Content |
|---|---|---|
| `0x00` | 4 | `00 F0 FF 00` |
| `0x04` | 124 | `00` |

Present as the last block of a complete BMS download. Identify it by content, not by file
size: a partial download ends on a block of real data. The final log entry may run into
the pad block; its tail bytes are then not log data.

### Repeated blocks

A download may contain the same 128-byte block more than once in succession. Adjacent
identical non-erased blocks are duplicates; discard all but the first.
""")

page('framing.md', """
# Entry Framing

Every entry, on both ECUs, starts with a 13-byte header.

""" + table([
    F('sof', 'u8', 'Start of frame, `0xB2`'),
    F('length', 'u8', 'Entry length on disk, including header and escape bytes. Max 128'),
    F('type', 'u8', 'Entry type'),
    F('timestamp', 'u32', 'Unix time, seconds, UTC'),
    F('usec', 'u32', 'Microseconds within the second (whole milliseconds). `999999` when the clock was behind the previous entry'),
    F('count', 'u8', 'Rolling entry counter, wraps at 256. See [count](#count)'),
    F('utc_offset', 's8', 'UTC offset, whole hours'),
], [(None, 13)]).replace('| Offset |', '| Entry offset |') + """

Payload: `length − 13` bytes after un-escaping, starting at entry offset `0x0D`.

## Byte stuffing

From the `type` byte to the end of the entry, `0xB2` and `0xFE` are escaped:

| Byte | Written as |
|---|---|
| `0xB2` | `FE 4D` |
| `0xFE` | `FE 01` |

Decoding: on `0xFE`, discard it and take the bitwise complement of the following byte.
`length` counts the escaped (on-disk) size.

## count

- Restarts at 0 on every boot and hibernate wake.
- Advances by 1 per entry, and also without a log write while the ECU is awake. A jump
  between consecutive entries is normal and does not indicate damage.
- The log header (`0xFB`) carries the counter at download time, so it differs between
  downloads of the same log.

## UTC offset

`utc_offset` is the bike's time-correction setting at the time of writing.

```
local_time = timestamp + utc_offset × 3600
```

| Raw | Offset |
|---|---|
| `0xF8` | −8 h |
| `0xF9` | −7 h |
| `0x01` | +1 h |
| `0x02` | +2 h |

## Timestamps

| Condition | Value |
|---|---|
| Logged before RTC sync | Near the Unix epoch |
| Log header entry (`0xFB`) | Download time |
""")

# --------------------------------------------------------------------------
# MBB
# --------------------------------------------------------------------------

MBB_HEADER = ENTRY_HEADER + [
    F('device_name', 'char[10]', '`MBB`'),
    F('mfg_version', 'u16', 'Manufacturing version, model year × 10 (e.g. `20230`)'),
    F('model', 'char[16]', 'Model (e.g. `SRS`, `DSRX`)'),
    F('vin', 'char[19]', 'VIN, 17 characters + NUL padding'),
    F('serial', 'char[32]', 'MBB serial number'),
    F('board_part', 'char[9]', 'Board part number (e.g. `40-08198`). 115-byte header: binary value, not a string'),
    F('board_id', 'u16', 'Board revision. 0–5 valid, `0xFF` unknown'),
    F('fw_rev_num', 'u16', 'Firmware revision (e.g. `41` for `75-08163-41`)'),
    F('fw_build_num', 'u16', 'Firmware build/package number', only={'117 B'}),
    F('fw_commit_hash', 'char[10]', 'Firmware git commit hash'),
]

MBB_TYPES = values([
    ('`0x46`', '`bms_status`', '53', 'BMS module status', '[Status](status.md#0x46-bms_status)'),
    ('`0x47`', '`precharge_status`', '22', 'Precharge status', '[Status](status.md#0x47-precharge_status)'),
    ('`0x48`', '`charger_details`', '49', 'Charger module details', '[Charging](charging.md#0x48-charger_details)'),
    ('`0x49`', '`charging_state`', '25', 'Charging state', '[Charging](charging.md#0x49-charging_state)'),
    ('`0x4A`', '`elock_status`', '13', 'Electronic lock status', '[Status](status.md#0x4a-elock_status)'),
    ('`0x4B`', '`periodic_small`', '40', 'Periodic snapshot, small, first generation', '[Periodic](periodic.md#0x4b-periodic_small)'),
    ('`0x4C`', '`periodic_medium`', '71 / 74', 'Periodic snapshot, medium, first generation', '[Periodic](periodic.md#0x4c-periodic_medium)'),
    ('`0x4D`', '`periodic_large`', '83 / 86', 'Periodic snapshot, large, first generation', '[Periodic](periodic.md#0x4d-periodic_large)'),
    ('`0x4E`', '`firmware_updated`', '54 / 52', 'Firmware updated', '[Events](events.md#0x4e-firmware_updated)'),
    ('`0x4F`', '`queue_send_fail`', '18', 'RTOS queue send failure', '[Faults](faults.md#0x4f-queue_send_fail)'),
    ('`0x50`', '`mcu_fault`', '25', 'MCU fault registers', '[Faults](faults.md#0x50-mcu_fault)'),
    ('`0x51`', '`periodic_small2`', '62 / 58', 'Periodic snapshot, small', '[Periodic](periodic.md#0x51-periodic_small2)'),
    ('`0x52`', '`periodic_medium2`', '79 / 75', 'Periodic snapshot, medium', '[Periodic](periodic.md#0x52-periodic_medium2)'),
    ('`0x53`', '`periodic_large2`', '93 / 89', 'Periodic snapshot, large', '[Periodic](periodic.md#0x53-periodic_large2)'),
    ('`0x54`', '`torque_info`', '16', 'Torque and power snapshot', '[Periodic](periodic.md#0x54-torque_info)'),
    ('`0xFB`', '`log_header`', '104', 'Log header (first entry of the file)', '[Log header](#log-header-0xfb)'),
    ('`0xFD`', '`debug_message`', '≤ 115', 'Text message', '[Events](events.md#0xfd-debug_message)'),
], ('Type', 'Name', 'Payload (bytes)', 'Description', 'Layout'))

page('mbb/index.md', f"""
# MBB

## Log header (`0xFB`)

Entry offsets (equal to file offsets once the entry is un-escaped).

{table(MBB_HEADER, [('117 B', 117), ('115 B', 115)])}

| Header length | Firmware |
|---|---|
| 117 (`0x75`) | rev 13 and later |
| 115 (`0x73`) | rev 6–11 |

## Entry types

{MBB_TYPES}

Payload sizes given as `a / b` have two firmware variants, selected by payload length.
See [Firmware versions](../firmware.md).
""")

# periodic ----------------------------------------------------------------

def core(state_desc='Bike state. See [State](#state)'):
    return [
        F('dc_bus_voltage_mv', 's32', 'Controller DC bus voltage, mV (multiple of 100)'),
        F('dc_bus_current_ma', 's32', 'Controller DC bus current, mA (multiple of 100). + = discharge'),
        F('motor_rpm', 's32', 'Motor speed, rpm (×14/13 applied)'),
        F('soc_pct', 'u8', 'State of charge, %'),
        F('pack_voltage_mv', 'u32', 'Pack voltage, mV'),
        F('pack_current_ma', 's32', 'Pack current, mA. + = discharge, − = charge/regen'),
        F('state', 'char[5]', state_desc),
    ]


ERR = F('error_flags', 'u32', 'Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed)')
SPEED = F('speed_mm_hr', 's32', 'Vehicle speed, mm/h (÷ 10⁶ = km/h)')
RANGE = F('range_km_x100', 'u16', 'Estimated range, km × 100')


def temps(ambient, only=None):
    return [
        F('temp_flags', 'u32', 'Temperature read failures. See [temp_flags](#temp_flags)', only),
        F('ambient_c', 's32', f'Ambient temperature, {ambient}. See [ambient_c](#ambient_c)', only),
        F('t1_c', 's32', 'Motor temperature, °C. 0 / −1 = unavailable', only),
        F('t2_c', 's32', 'Controller temperature, °C. 0 / −1 = unavailable', only),
        F('bms_high_c', 's32', 'Highest cell temperature, °C. −1 = unavailable', only),
        F('bms_low_c', 's32', 'Lowest cell temperature, °C. −1 = unavailable', only),
    ]


BAT12 = F('battery_12v', 'u32', '12 V battery voltage, µV', only={'62 B', '79 B', '93 B'})
COUNTS = [
    F('num_can_modules', 'u8', 'BMS modules on CAN'),
    F('num_contactors_closed', 'u8', 'Contactors closed'),
]
SLOT = [
    F('controller_fault_code', 'u8', 'Motor controller fault code. 0 = none'),
    F('pack_index', 'u8', 'BMS slot of the next two fields (0)'),
    F('module_status_bits', 'u32', 'Status bits of that slot. See [module_status_bits](status.md#module_status_bits)'),
    F('capacity_ah', 'u16', 'Capacity of that slot, Ah'),
]
FLAGS2 = F('status_flags', 'u32', 'Validity flags. See [status_flags](#status_flags)')
MED2 = F('freeze_med2_flags', 'u32', 'Validity flags. See [freeze_med2_flags](#freeze_med2_flags)')
TAIL2 = [
    F('odometer_km_x10', 'u32', 'Odometer, km × 10'),
    SPEED,
    RANGE,
    F('bms_lowest_dis_allow', 'u8', 'Lowest BMS discharge allowance'),
]

P4B = [ERR, F('status_flags', 'u32', 'Validity flags. See [status_flags](#status_flags)')] + core() + [SPEED, RANGE]
def odometer(short, long):
    return [F('odometer_low_byte', 'u8', 'Odometer low byte, km × 10', only={short}),
            F('odometer_km_x10', 'u32', 'Odometer, km × 10', only={long})]


P4C = [ERR, F('freeze_status', 'u32', 'See [freeze_status](#freeze_status)'),
       F('status_flags', 'u32', 'Validity flags. See [status_flags](#status_flags)')] + core() + [SPEED, RANGE] + temps('°C') + COUNTS + odometer('71 B', '74 B')
P4D = [ERR, F('freeze_med2_err', 'u32', 'Bit 1 = medium snapshot failed. Undefined in rev 6–14'),
       F('freeze_status', 'u32', 'See [freeze_status](#freeze_status)'),
       F('status_flags', 'u32', 'Validity flags. See [status_flags](#status_flags)')] + core() + [SPEED, RANGE] + temps('°C') + COUNTS + odometer('83 B', '86 B') + SLOT
P51 = [ERR, FLAGS2] + core() + temps('°C × 100; °C in rev 18–19') + [dict(BAT12, only={'62 B'})]
P52 = [ERR, MED2, FLAGS2] + core() + temps('°C × 100; °C in rev 18–19') + [dict(BAT12, only={'79 B'})] + COUNTS + TAIL2
P53 = [ERR, F('freeze_med2_err', 'u32', 'Read failures. See [freeze_med2_err](#freeze_med2_err)'), MED2, FLAGS2] + core() + temps('°C × 100; °C in rev 18–19') + [
    dict(BAT12, only={'93 B'})] + COUNTS + TAIL2 + SLOT + [
    F('bms_avg_dis_allow', 'u8', 'Average BMS discharge allowance'),
    F('bms_avg_chg_allow', 'u8', 'Average BMS charge allowance'),
]
P54 = [
    F('torque_unm', 's32', 'Motor torque, µNm'),
    F('torque_demand_pct_x10', 's32', 'Torque demand, % × 10 (−1000…1000). − = regen'),
    F('filtered_motor_power_w', 's32', 'Motor power, first-order low-pass filtered, W. 0 at power-on'),
    F('disch_power_limit_w', 's32', 'Discharge power limit, W. −1 = BMS not active'),
]

STATES = values([
    (0, '`NONE`', 'No state'), (1, '`STRT`', 'Start'), (2, '`PWSU`', 'Power supply up'),
    (3, '`WAKE`', 'Wake'), (4, '`HIB`', 'Hibernate'), (5, '`STOP`', 'Stop'),
    (6, '`RUN`', 'Run'), (7, '`LIMP`', 'Limp'), (8, '`CHRG`', 'Charge'),
    (9, '`WAIT`', 'Wait'), (10, '`FWUP`', 'Firmware update'), (11, '`REV`', 'Reverse'),
    (12, '`PARK`', 'Park'),
], ('Index', 'String', 'State'))

page('mbb/periodic.md', f"""
# MBB Periodic Entries

| Type | Name | Payload (bytes) |
|---|---|---|
| `0x4B` | `periodic_small` | 40 |
| `0x4C` | `periodic_medium` | 71 / 74 |
| `0x4D` | `periodic_large` | 83 / 86 |
| `0x51` | `periodic_small2` | 58 / 62 |
| `0x52` | `periodic_medium2` | 75 / 79 |
| `0x53` | `periodic_large2` | 89 / 93 |
| `0x54` | `torque_info` | 16 |

Logged about every 120 s while riding and every 60 min while parked.

## 0x4B -- periodic_small

{table(P4B, [(None, 40)])}

## 0x4C -- periodic_medium

{table(P4C, [('71 B', 71), ('74 B', 74)])}

71 bytes: firmware rev 6–14. 74 bytes: firmware rev 21+ (not observed in logs).

## 0x4D -- periodic_large

{table(P4D, [('83 B', 83), ('86 B', 86)])}

83 bytes: firmware rev 6–14. 86 bytes: firmware rev 21+ (not observed in logs).

## 0x51 -- periodic_small2

{table(P51, [('58 B', 58), ('62 B', 62)])}

## 0x52 -- periodic_medium2

{table(P52, [('75 B', 75), ('79 B', 79)])}

## 0x53 -- periodic_large2

{table(P53, [('89 B', 89), ('93 B', 93)])}

## 0x54 -- torque_info

{table(P54, [(None, 16)])}

## Field definitions

### state

5-byte NUL-padded ASCII. Empty when the lookup failed (`status_flags` bit 7).

{STATES}

### status_flags

`0x51`–`0x53`. A set bit means the field is not a valid reading.

{bits([(1, '`dc_bus_voltage_mv` invalid'), (2, '`dc_bus_current_ma` invalid (not set by firmware)'),
       (3, '`motor_rpm` invalid'), (5, '`pack_voltage_mv` invalid'), (6, '`pack_current_ma` invalid'),
       (7, '`state` lookup failed'), (8, 'Temperature block failed'), (9, '`battery_12v` invalid')], 3)}

`0x4B`–`0x4D`: bit 8 (`0x100`) = `speed_mm_hr` invalid. Other bits are not mapped.

A zero `dc_bus_current_ma` with bit 1 set means no controller data.

### ambient_c

| Entry | MBB firmware | Unit |
|---|---|---|
| `0x4C`, `0x4D` | rev 6–14 | °C |
| `0x51`–`0x53` | rev 13–17 | °C × 100 |
| `0x51`–`0x53` | rev 18–19 | °C |
| `0x51`–`0x53` | rev 20+ | °C × 100 |

### temp_flags

{bits([(1, '`ambient_c` read failed'), (2, '`t1_c` read failed'), (3, '`t2_c` read failed'),
       (4, '`bms_high_c` read failed'), (5, '`bms_low_c` read failed')])}

### freeze_med2_flags

{bits([(1, 'Small snapshot failed'), (5, '`speed_mm_hr` invalid'), (7, '`bms_lowest_dis_allow` invalid')])}

### freeze_med2_err

`0x53`. A set bit means the read failed.

{bits([(1, 'Medium snapshot failed'), (6, '`bms_avg_dis_allow` unavailable'), (7, '`bms_avg_chg_allow` unavailable')])}

### freeze_status

{bits([(1, 'Small snapshot failed'), (2, 'Temperature block failed')])}
""")

# status ------------------------------------------------------------------

P46 = [
    F('error_result', 'u32', '0 = OK, 2 = module not found'),
    F('error_flags', 'u32', 'Bit 7 = module name mismatch, bit 8 = precharge info failed'),
    F('module_id', 'u8', 'BMS module index, 0–5'),
    F('time_since_ms', 'u64', 'Time since module timestamp event, ms'),
    F('module_registered', 'u8', '1 = registered'),
    F('eligibility_flags', 'u8', 'See [eligibility_flags](#eligibility_flags)'),
    F('capacity_ah', 'u16', 'Module capacity, Ah'),
    F('pack_voltage_mv', 'u32', 'Module pack voltage, mV'),
    F('module_name', 'char[10]', 'Module device name'),
    F('precharge_status_bits', 'u32', 'Bit 3 = precharge percentage unreadable'),
    F('precharge_state_active', 'u8', '1 = precharge in progress'),
    F('precharge_active_bit', 'u8', '`module_status_bits` bit 2'),
    F('precharge_pct', 'u8', 'Precharge, 0–100 %'),
    F('connect_state_closed', 'u8', '1 = MBB connection state is closed'),
    F('contactor_closed_bit', 'u8', '`module_status_bits` bit 1'),
    F('module_locked', 'u8', '1 = module locked by MBB'),
    F('pack_current_ma', 's32', 'Module pack current, mA'),
    F('module_status_bits', 'u32', 'See [module_status_bits](#module_status_bits)'),
]
P47 = [
    F('error_flags', 'u32', '0 = OK, `0x2` = module name unavailable, `0x8` = precharge percentage unreadable'),
    F('module_name', 'char[10]', 'Module device name'),
    F('module_id', 'u8', 'BMS module index'),
    F('precharge_status_bits', 'u32', 'Bit 3 = precharge percentage unreadable'),
    F('precharge_state_active', 'u8', '1 = precharge in progress'),
    F('precharge_active_bit', 'u8', '`module_status_bits` bit 2'),
    F('precharge_pct', 'u8', 'Precharge, 0–100 %'),
]
P4A = [
    F('immobilizer_locked', 'u8', '1 = immobilized, 0 = not immobilized'),
    F('elock_status_flag', 'u8', 'Lock frame byte 6, bit 4'),
    F('elock_addr', 'u32', 'Lock device ID. 0 = no frame, `0xFFFFFFFF` = unprogrammed'),
    F('elock_sw_version', 'u8', 'Lock software version'),
    F('elock_status_code', 'u8', 'Lock status. See [elock_status_code](#elock_status_code)'),
    F('auth_flag', 'u8', 'Lock frame byte 1, bit 4. 1 = authenticated'),
    F('key_number', 'u8', 'Key slot, 0 = none, 1–5'),
    F('status_flag_2', 'u8', 'Lock frame byte 7, bit 2, inverted'),
    F('transponder_auth_ok', 'u8', 'Lock frame byte 7, bit 3, inverted. Tracks device presence'),
    F('reset_request', 'u8', '1 = re-pair request pending'),
]

page('mbb/status.md', f"""
# MBB BMS and Lock Status

## 0x46 -- bms_status

{table(P46, [(None, 53)])}

### eligibility_flags

| Firmware | Value |
|---|---|
| rev ≤ 24 | 1 = module eligible |
| rev ≥ 30 | Bit 0 = discharge eligible, bit 1 = charge eligible |

### module_status_bits

{bits([(1, 'Contactor closed'), (2, 'Precharging'), (4, 'Discharge enabled'), (5, 'Charge enabled')])}

Upper bits carry BMS fault flags (not mapped).

## 0x47 -- precharge_status

{table(P47, [(None, 22)])}

## 0x4A -- elock_status

{table(P4A, [(None, 13)])}

Logged on: key on with no lock frame, unregistered lock seen, lock registered, re-pair
request and re-pair success.

### elock_status_code

{values([(0, 'Invalid'), (1, 'Unlocked'), (2, 'Locked'), (3, 'Failed'), (4, 'OK')])}
""")

# charging ----------------------------------------------------------------

P48 = [
    F('name', 'bytes[10]', 'Charger name, NUL-padded (e.g. ` 3kW`)'),
    F('status', 'u16', 'Status word. See [status](#status)'),
    F('dc_output_mv', 'u32', 'DC output voltage, mV'),
    F('dc_current_a', 'u16', 'DC output current, A. mA in rev 7–15'),
    F('max_charge_current_a', 'u16', 'Maximum charge current, A. mA in rev 7–15'),
    F('max_charge_voltage_mv', 'u32', 'Maximum charge voltage, mV'),
    F('cmd_in_a', 'u8', 'AC input current limit, A'),
    F('charger_variant', 'u8', 'Charger model/firmware code. See [charger_variant](#charger_variant)'),
    F('ac_volts_v', 'u8', 'AC input voltage, V'),
    F('ac_current_a', 'u16', 'AC input current, A. mA in rev 7–15'),
    F('ac_hz', 'u8', 'AC frequency, Hz'),
    F('temp_c', 's8', 'Charger temperature, °C'),
    F('can_id', 'u8', 'CANopen node ID. `0x10` = first, `0x11` = second'),
    F('version', 'u16', 'Charger firmware version'),
    F('serial_number', 'u32', 'Charger serial number'),
    F('status_code', 'u16', 'Charger type. See [status_code](#status_code)'),
    F('setpt_voltage_mv', 'u32', 'Commanded charge voltage, mV'),
    F('setpt_current_a', 'u16', 'Commanded charge current, A. mA in rev 7–15'),
    F('setpt_ac_input_a', 'u16', 'Commanded AC input current limit, A'),
    F('en_flag', 'u8', 'Charger enabled'),
]
P49 = [
    F('charging_target_mv', 'u32', 'Charge voltage target, mV'),
    F('evse_pilot_current_a', 'u16', 'EVSE pilot current limit, A. 127 = no limit'),
    F('charge_target_pct', 'u8', 'Charge target, % SOC'),
    F('charger_output_current_a', 'u16', 'Total charger DC output current, A. mA in rev ≤ 15'),
    F('charge_current_a', 's32', 'Total charge current, A. mA in rev ≤ 15'),
    F('evse_disconnect_flags', 'u8', '0 = EVSE connected'),
    F('schedule_charge_enabled', 'u8', '1 = scheduled charging enabled'),
    F('active_sched_window_val', 'u32', "Today's charge window. See [active_sched_window_val](#active_sched_window_val)"),
    F('charging_enabled', 'u8', '1 = charging enabled'),
    F('evse_allowed_current_a', 'u8', 'EVSE allowed current, A'),
    F('hard_charge_target_mv', 'u32', 'Hard charge target, mV. 0 = disabled'),
]

page('mbb/charging.md', f"""
# MBB Charging

## 0x48 -- charger_details

One entry per charger.

{table(P48, [(None, 49)])}

Firmware rev 7–11: two chargers are logged as one 98-byte entry (two consecutive records).

| MBB firmware | Current fields |
|---|---|
| rev 7–15 | mA |
| rev 17+ | A |

### status

{values([('`0x0480`', 'Charging, 110 V AC'), ('`0x0080`', 'Charging, 220 V AC'), ('`0x0020`', 'Idle')])}

### status_code

{values([(9, '3 kW onboard charger'), (10, '6 kW onboard charger'), (17, 'Reserved'), (28, 'Calex charger'), (29, 'Flat 6 kW charger')])}

### charger_variant

Low bits give the power class: 1 = 3 kW, 2 = 6 kW.

{values([(9, '3 kW, firmware 101 / 201'), (10, '6 kW, firmware 100 / 200'), (17, '3 kW, firmware 202–207; 3kWFCC'), (34, 'Flt 6 (Calex)')], ('Value', 'Charger'))}

## 0x49 -- charging_state

{table(P49, [(None, 25)])}

### active_sched_window_val

| Bits | Field | Scale |
|---|---|---|
| 25:21 | Start hour | × 8 |
| 17:13 | Start minute | × 8 |
| 9:5 | End hour | × 8 |
| 4:0 | End minute | × 8 |

0 = no schedule.

Bit layout and scale are unconfirmed.
""")

# faults ------------------------------------------------------------------

P4F = [
    F('queue_name', 'char[10]', 'Queue name'),
    F('msgs_waiting', 'u32', 'Messages waiting in the queue'),
    F('send_fail_count', 'u32', 'Failed sends, all queues, since power-on'),
]
P50 = [
    F('fault_type', 'u8', 'Fault type. 1 = hard fault'),
    F('fault_data_0', 'u32', 'HFSR'),
    F('fault_data_1', 'u32', 'CFSR'),
    F('fault_data_2', 'u32', 'BFAR'),
    F('fault_data_3', 'u32', 'Exception stack pointer'),
    F('fault_data_4', 'u32', 'LR'),
    F('fault_data_5', 'u32', 'PC'),
]

page('mbb/faults.md', f"""
# MBB Faults

## 0x4F -- queue_send_fail

{table(P4F, [(None, 18)])}

### Queue names

{values([('`CAN0RxQ`', 48), ('`CAN1RxQ`', 64), ('`CAN1txQ`', '32, 64'), ('`CAN2RxQ`', 32), ('`CAN2txQ`', 16),
         ('`dashQ`', 6), ('`logQ`', 8), ('`pduQ`', 5), ('`uartrxQ`', 128), ('`uarttxQ`', '958, 991')],
        ('Queue', 'Typical `msgs_waiting`'))}

## 0x50 -- mcu_fault

{table(P50, [(None, 25)])}

!!! note
    Register assignment of `fault_data_0`–`fault_data_5` follows the BMS
    [`0x7E` mcu_fault](../bms/diagnostics.md#0x7e-mcu_fault) layout and is unconfirmed for the MBB.

See [CFSR bits](../bms/diagnostics.md#cfsr-bits).
""")

# events ------------------------------------------------------------------

P4E = [
    F('prev_fw_rev', 'u16', 'Previous firmware revision'),
    F('fw_rev', 'u16', 'Firmware revision of the running image'),
    F('prev_fw_state', 'char[32]', 'Previous firmware state. Default `UNINITIALIZED`'),
    F('fw_build', 'u16', 'Build/package number of the running image'),
    F('bank_name', 'char[6]', 'Flash bank: `banka` or `bankb`'),
    F('commit_hash', 'char[10]', 'Git commit hash of the running image'),
]
P4E_OLD = [
    F('prev_fw_rev', 'u16', 'Previous firmware revision'),
    F('fw_rev', 'u16', 'Firmware revision of the running image'),
    F('prev_fw_state', 'char[32]', 'Previous firmware state (image compile timestamp)'),
    F('commit_hash', 'char[10]', 'Git commit hash, first 5 characters'),
    F('bank_name', 'char[6]', 'Flash bank'),
]

page('mbb/events.md', f"""
# MBB Events

## 0x4E -- firmware_updated

Logged at the first boot of a new firmware image.

{table(P4E, [(None, 54)])}

Firmware rev 8–11 (52 bytes):

{table(P4E_OLD, [(None, 52)])}

## 0xFB -- log_header

See [Log header](index.md#log-header-0xfb).

## 0xFD -- debug_message

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | ≤ 115 | `bytes` | `message` | ASCII text, NUL-terminated |

- Maximum 114 characters + NUL.
- Truncated messages end in `$`.
- Some entries contain non-ASCII bytes.
""")

# --------------------------------------------------------------------------
# BMS
# --------------------------------------------------------------------------

BMS_HEADER = ENTRY_HEADER + [
    F('device_name', 'char[10]', '`BMS`'),
    F('module_model', 'char[16]', 'Module model (e.g. `FST BCB`)'),
    F('num_parallel_cells', 'u8', 'Cells in parallel per series group'),
    F('board_part', 'char[16]', 'Board part number (e.g. `40-08295-01`)'),
    F('serial', 'char[16]', 'BMS serial number'),
    F('bcbm_id', 'char[16]', 'BCBM identifier (e.g. `BCBM0000`)'),
    F('fw_part', 'char[16]', 'BMU firmware part number (`75-08274`, `75-08384`)'),
    F('fw_rev_num', 'u16', 'Firmware revision'),
    F('fw_build_num', 'u16', 'Firmware package build number'),
    F('commit_hash', 'char[16]', 'Firmware package git commit hash'),
    F('firmware_bank', 'u8', 'Running flash bank. 1 = A, 2 = B'),
]

BMS_TYPES = values([
    ('`0x4B`', '`periodic_small`', '33 / 37 / 39', 'Periodic snapshot, small', '[Periodic](periodic.md#0x4b-periodic_small)'),
    ('`0x4C`', '`periodic_medium`', '49 / 55 / 57', 'Periodic snapshot, medium', '[Periodic](periodic.md#0x4c-periodic_medium)'),
    ('`0x4D`', '`periodic_large`', '57 / 63 / 65', 'Periodic snapshot, large', '[Periodic](periodic.md#0x4d-periodic_large)'),
    ('`0x4E`', '`soc_snapshot`', '89', 'State-of-charge estimator snapshot', '[Periodic](periodic.md#0x4e-soc_snapshot)'),
    ('`0x4F`', '`dis_overcur`', '22', 'Discharge overcurrent, set', '[Faults](faults.md#overcurrent)'),
    ('`0x50`', '`chg_overcur`', '22', 'Charge overcurrent, set', '[Faults](faults.md#overcurrent)'),
    ('`0x51`', '`sev_dis_overcur`', '22', 'Severe discharge overcurrent, set', '[Faults](faults.md#overcurrent)'),
    ('`0x52`', '`sev_chg_overcur`', '22', 'Severe charge overcurrent, set', '[Faults](faults.md#overcurrent)'),
    ('`0x53`', '`dis_overcur_clr`', '22', 'Discharge overcurrent, clear', '[Faults](faults.md#overcurrent)'),
    ('`0x54`', '`chg_overcur_clr`', '22', 'Charge overcurrent, clear', '[Faults](faults.md#overcurrent)'),
    ('`0x55`', '`cont_fault`', '14', 'Contactor fault, set', '[Faults](faults.md#0x55-cont_fault)'),
    ('`0x56`', '`cont_fault_clr`', '0', 'Contactor fault, clear', '—'),
    ('`0x57`', '`ov_fault`', '63', 'Cell overvoltage, set', '[Faults](faults.md#voltage)'),
    ('`0x58`', '`ov_fault_clr`', '7', 'Cell overvoltage, clear', '[Faults](faults.md#voltage)'),
    ('`0x59`', '`uv_chg_fault`', '63', 'Cell undervoltage (charge), set', '[Faults](faults.md#voltage)'),
    ('`0x5A`', '`uv_chg_fault_clr`', '7', 'Cell undervoltage (charge), clear', '[Faults](faults.md#voltage)'),
    ('`0x5B`', '`uv_dischg_fault`', '63', 'Cell undervoltage (discharge), set', '[Faults](faults.md#voltage)'),
    ('`0x5C`', '`uv_dischg_fault_clr`', '7', 'Cell undervoltage (discharge), clear', '[Faults](faults.md#voltage)'),
    ('`0x5D`', '`ot_chg`', '13', 'Overtemperature (charge), set', '[Faults](faults.md#temperature)'),
    ('`0x5E`', '`ot_chg_clr`', '13', 'Overtemperature (charge), clear', '[Faults](faults.md#temperature)'),
    ('`0x5F`', '`ot_dischg`', '13', 'Overtemperature (discharge), set', '[Faults](faults.md#temperature)'),
    ('`0x60`', '`ot_dischg_clr`', '13', 'Overtemperature (discharge), clear', '[Faults](faults.md#temperature)'),
    ('`0x61`', '`ut_chg`', '13', 'Undertemperature (charge), set', '[Faults](faults.md#temperature)'),
    ('`0x62`', '`ut_chg_clr`', '13', 'Undertemperature (charge), clear', '[Faults](faults.md#temperature)'),
    ('`0x63`', '`ut_dischg`', '13', 'Undertemperature (discharge), set', '[Faults](faults.md#temperature)'),
    ('`0x64`', '`ut_dischg_clr`', '13', 'Undertemperature (discharge), clear', '[Faults](faults.md#temperature)'),
    ('`0x65`', '`chg_fault`', '18 / 26', 'Charge fault, set', '[Faults](faults.md#0x65-0x66-chg_fault)'),
    ('`0x66`', '`chg_fault_clr`', '18 / 26', 'Charge fault, clear', '[Faults](faults.md#0x65-0x66-chg_fault)'),
    ('`0x67`', '`sev_ot`', '13', 'Severe overtemperature, set', '[Faults](faults.md#temperature)'),
    ('`0x68`', '`sev_ot_clr`', '13', 'Severe overtemperature, clear', '[Faults](faults.md#temperature)'),
    ('`0x69`', '`voltage_sensor`', '4', 'Voltage sensor fault, set', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0x6A`', '`voltage_sensor_clr`', '4', 'Voltage sensor fault, clear', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0x6B`', '`cur_sense`', '17', 'Current sensor fault, set', '[Diagnostics](diagnostics.md#0x6b-0x6c-cur_sense)'),
    ('`0x6C`', '`cur_sense_clr`', '17', 'Current sensor fault, clear', '[Diagnostics](diagnostics.md#0x6b-0x6c-cur_sense)'),
    ('`0x6D`', '`can_sync_fail`', '0', 'CAN sync failure', '—'),
    ('`0x6E`', '`temp_sen`', '17', 'Temperature sensor fault, set', '[Diagnostics](diagnostics.md#0x6e-0x6f-temp_sen)'),
    ('`0x6F`', '`temp_sen_clr`', '17', 'Temperature sensor fault, clear', '[Diagnostics](diagnostics.md#0x6e-0x6f-temp_sen)'),
    ('`0x70`', '`power_supply`', '14', 'Power supply fault, set', '[Diagnostics](diagnostics.md#0x70-0x71-power_supply)'),
    ('`0x71`', '`power_supply_clr`', '14', 'Power supply fault, clear', '[Diagnostics](diagnostics.md#0x70-0x71-power_supply)'),
    ('`0x72`', '`pack_io`', '16', 'Pack I/O fault, set', '[Diagnostics](diagnostics.md#0x72-0x73-pack_io)'),
    ('`0x73`', '`pack_io_clr`', '16', 'Pack I/O fault, clear', '[Diagnostics](diagnostics.md#0x72-0x73-pack_io)'),
    ('`0x74`', '`isolation_fault`', '4', 'Isolation fault, set', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0x75`', '`isolation_fault_clr`', '4', 'Isolation fault, clear', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0x76`', '`lvc`', '13', 'Low-voltage cutoff', '[Faults](faults.md#0x76-lvc)'),
    ('`0x77`', '`not_ok_precharge`', '13', 'Not OK to precharge', '[Faults](faults.md#0x77-not_ok_precharge)'),
    ('`0x78`', '`queue_send_fail`', '18', 'RTOS queue send failure', '[Diagnostics](diagnostics.md#0x78-queue_send_fail)'),
    ('`0x79`', '`cell_imbalance`', '6', 'Cell imbalance, set', '[Faults](faults.md#0x79-0x7a-cell_imbalance)'),
    ('`0x7A`', '`cell_imbalance_clr`', '6', 'Cell imbalance, clear', '[Faults](faults.md#0x79-0x7a-cell_imbalance)'),
    ('`0x7B`', '`sev_dis_overcur_clr`', '22', 'Severe discharge overcurrent, clear', '[Faults](faults.md#overcurrent)'),
    ('`0x7C`', '`sev_chg_overcur_clr`', '22', 'Severe charge overcurrent, clear', '[Faults](faults.md#overcurrent)'),
    ('`0x7D`', '`limits`', '17', 'Operating limits', '[Cell data](cell-data.md#0x7d-limits)'),
    ('`0x7E`', '`mcu_fault`', '25', 'MCU fault registers', '[Diagnostics](diagnostics.md#0x7e-mcu_fault)'),
    ('`0x7F`', '`fuse_temp`', '5', 'Fuse temperature fault, set', '[Diagnostics](diagnostics.md#0x7f-0x80-fuse_temp)'),
    ('`0x80`', '`fuse_temp_clr`', '5', 'Fuse temperature fault, clear', '[Diagnostics](diagnostics.md#0x7f-0x80-fuse_temp)'),
    ('`0x81`', '`fuse_voltage`', '12', 'Fuse voltage fault, set', '[Diagnostics](diagnostics.md#0x81-0x82-fuse_voltage)'),
    ('`0x82`', '`fuse_voltage_clr`', '12', 'Fuse voltage fault, clear', '[Diagnostics](diagnostics.md#0x81-0x82-fuse_voltage)'),
    ('`0x83`', '`cell_voltages`', '56', 'All cell voltages', '[Cell data](cell-data.md#0x83-cell_voltages)'),
    ('`0x84`', '`cell_too_low_for_chg`', '2 / 3', 'Cell too low to charge', '[Cell data](cell-data.md#0x84-0x85-charger-cell-voltage)'),
    ('`0x85`', '`cell_too_high_for_chg`', '2 / 3', 'Cell too high to charge', '[Cell data](cell-data.md#0x84-0x85-charger-cell-voltage)'),
    ('`0x86`', '`cell_temp_too_low_for_chg`', '1', 'Cell too cold to charge', '[Cell data](cell-data.md#0x86-0x89-cell-temperature-limits)'),
    ('`0x87`', '`cell_temp_too_high_for_chg`', '1', 'Cell too hot to charge', '[Cell data](cell-data.md#0x86-0x89-cell-temperature-limits)'),
    ('`0x88`', '`cell_temp_too_low_for_dischg`', '1', 'Cell too cold to discharge', '[Cell data](cell-data.md#0x86-0x89-cell-temperature-limits)'),
    ('`0x89`', '`cell_temp_too_high_for_dischg`', '1', 'Cell too hot to discharge', '[Cell data](cell-data.md#0x86-0x89-cell-temperature-limits)'),
    ('`0x8A`', '`fan_on`', '1', 'Fan turned on', '[Diagnostics](diagnostics.md#0x8a-0x8b-fan)'),
    ('`0x8B`', '`fan_off`', '1', 'Fan turned off', '[Diagnostics](diagnostics.md#0x8a-0x8b-fan)'),
    ('`0x8C`', '`isolation_severe`', '4', 'Severe isolation fault, set (rev 17+)', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0x8D`', '`isolation_severe_clr`', '4', 'Severe isolation fault, clear (rev 17+)', '[Faults](faults.md#isolation-and-voltage-sensor)'),
    ('`0xFB`', '`log_header`', '112', 'Log header (first entry of the file)', '[Log header](#log-header-0xfb)'),
    ('`0xFD`', '`debug_message`', 'variable', 'Text message', '[Cell data](cell-data.md#0xfd-debug_message)'),
], ('Type', 'Name', 'Payload (bytes)', 'Description', 'Layout'))

page('bms/index.md', f"""
# BMS

## Log header (`0xFB`)

Entry offsets (equal to file offsets once the entry is un-escaped).

{table(BMS_HEADER, [(None, 125)])}

A 126-byte variant carries one trailing `0x00`.

### Board variants

| `fw_part` | `board_part` | MCU |
|---|---|---|
| `75-08274` | `40-08247-01` | Infineon XMC4500 |
| `75-08384` | `40-08295-01` | Infineon XMC4800 |

Both produce identical entry layouts.

## Entry types

{BMS_TYPES}

Payload sizes given as `a / b` have several firmware variants, selected by payload length.
See [Firmware versions](../firmware.md).

## Sign convention

BMS current fields: + = discharge, − = charge. (MBB `pack_current_ma` uses the same sign.)
""")

# BMS periodic -------------------------------------------------------------

V3 = [('33 B', None), ('37 B', None), ('39 B', None)]


def vs(sizes):
    return [(f'{s} B', s) for s in sizes]


def bms_small(sizes):
    a, b, c = (f'{s} B' for s in sizes)
    return [
        F('cell_low_mv', 'u16', 'Lowest cell voltage, mV'),
        F('lowest_cell_oc_mv', 'u16', 'Lowest cell open-circuit voltage, mV. 0 = no estimate'),
        F('cell_high_mv', 'u16', 'Highest cell voltage, mV'),
        F('soc_pct', 'u8', 'State of charge, %'),
        F('pack_current_ma', 's32', 'Pack current, mA'),
        F('temp_fuse_c', 's8', 'Fuse temperature, °C'),
        F('pack_io_control_flags', 'u32', 'See [pack_io_control_flags](#pack_io_control_flags)'),
        F('bms_faults', 'u64', 'Active faults. See [bms_faults](#bms_faults)'),
        F('num_cmu_boards', 'u8', 'CMU boards in the pack'),
        F('pack_voltage_mv', 's32', 'Pack voltage, mV', only={b, c}),
        F('lowest_cell_index', 'u8', 'Lowest cell, 0–27. `0xFF` = unavailable', only={c}),
        F('highest_cell_index', 'u8', 'Highest cell, 0–27. `0xFF` = unavailable', only={c}),
    ]


def bms_medium_tail(sizes):
    a, b, c = (f'{s} B' for s in sizes)
    return [
        F('min_cell_temp_c', 's8', 'Minimum cell temperature, °C'),
        F('max_cell_temp_c', 's8', 'Maximum cell temperature, °C'),
        F('soc_meas_disch_pct', 'u8', 'SOC from measured discharge vs ideal capacity, %'),
        F('max_disch_amps', 'u16', 'Maximum discharge current allowed, A'),
        F('max_chg_amps', 'u16', 'Maximum charge current allowed, A'),
        F('adj_pack_cap_mah', 'u32', 'Adjusted pack capacity, mAh'),
        F('storage_mode', 'u8', '1 = long-term storage mode'),
        F('cell_imbalance_mv', 's16', 'Highest − lowest cell voltage, mV', only={b, c}),
    ]


SENS = F('sensor_read_failures', 'u32', 'See [Status words](#status-words)')
EEF = F('entry_error_flags', 'u32', 'See [Status words](#status-words)')
SRF = F('snapshot_read_failures', 'u32', 'See [Status words](#status-words)')

B4B = [EEF, SENS] + bms_small((33, 37, 39))
B4C = [EEF, SRF, SENS] + bms_small((49, 55, 57)) + bms_medium_tail((49, 55, 57))
B4D = [F('entry_status', 'u32', 'See [Status words](#status-words)'), EEF, SRF, SENS] + bms_small((57, 63, 65)) + bms_medium_tail((57, 63, 65)) + [
    F('est_pack_cap_mah', 'u32', 'Estimated pack capacity, mAh')]

B4E = [
    F('dis_cur_sensor0_ma', 's16', 'Discharge current, sensor 0, mA'),
    F('dis_cur_sensor1_ma', 's16', 'Discharge current, sensor 1, mA'),
    F('total_pack_dis_current_ma', 's32', 'Total pack discharge current, filtered, mA'),
    F('zero_a', 's16', 'Always 0'),
    F('lowest_unloaded_cell_mv', 's16', 'Lowest unloaded cell voltage, mV'),
    F('lowest_cell_oc_mv', 's16', 'Lowest cell open-circuit voltage, mV'),
    F('mean_pack_temp_c', 's8', 'Mean pack temperature, °C'),
    F('soc_ocv_raw_pct', 'u8', 'SOC from cell voltage, unfiltered, %'),
    F('soc_ocv_filt_pct', 'u8', 'SOC from cell voltage, filtered, %'),
    F('soc_ref_pct', 'u8', 'SOC at last reset, %'),
    F('soc_blend_input_pct', 'u8', 'Blend-filter input SOC, %'),
    F('soc_meas_vs_ideal_mah_pct', 'u8', 'SOC, measured mAh vs ideal capacity, %'),
    F('soc_meas_vs_ideal_mwh_pct', 'u8', 'SOC, measured mWh vs ideal capacity, %'),
    F('soc_est_vs_adj_mah_pct', 'u8', 'SOC, estimated mAh vs adjusted capacity, % (reported SOC)'),
    F('soc_est_vs_adj_alt_pct', 'u8', 'SOC, secondary accumulator, %'),
    F('adj_pack_cap_mah', 'u32', 'Adjusted pack capacity, mAh'),
    F('est_pack_cap_mah', 'u32', 'Estimated pack capacity, mAh'),
    F('adj_pack_cap_mwh', 'u32', 'Adjusted pack capacity, mWh'),
    F('est_pack_cap_mwh', 'u32', 'Estimated pack capacity, mWh'),
    F('meas_disch_mah', 'u32', 'Measured discharge, mAh'),
    F('est_disch_mah', 'u32', 'Estimated discharge, mAh'),
    F('meas_disch_mwh', 'u32', 'Measured discharge, mWh'),
    F('est_disch_mwh', 'u32', 'Estimated discharge, mWh'),
    F('ideal_pack_cap_mah', 'u32', 'Ideal (new) pack capacity, mAh'),
    F('ideal_pack_cap_mwh', 'u32', 'Ideal (new) pack capacity, mWh'),
    F('reserved_zero_a', 's32', 'Always 0'),
    F('reserved_zero_b', 's32', 'Always 0'),
    F('reserved_zero_c', 'u32', 'Always 0'),
    F('measured_cell_impedance_uohm', 'u32', 'Measured cell impedance, µΩ. 0 = not yet measured'),
    F('estimated_cell_sag_mv', 's16', 'Estimated cell sag under load, mV'),
    F('measured_cell_sag_mv', 's16', 'Measured cell sag, mV'),
    F('zero_b', 's16', 'Always 0'),
    F('reserved_zero_d', 's32', 'Always 0'),
]

PIO_BMU = [
    (0, 'Cell measurements requested'), (1, 'Cell measurements applied'),
    (2, 'Read UV/OV thresholds (one-shot)'), (3, 'Threshold read sent'),
    (4, 'Pack ADC measurements requested'), (5, 'Pack ADC measurements applied'),
    (6, 'Write OV threshold (one-shot)'), (7, 'OV threshold written'),
    (8, 'Write UV threshold (one-shot)'), (9, 'UV threshold written'),
    (10, 'Balancing requested'), (11, 'Balancing applied'),
    (12, 'Precharge enable requested'), (13, 'Precharge enable applied'),
    (14, 'Precharge on requested'), (15, 'Precharge on applied'),
    (16, 'Contactor close requested'), (17, 'Contactor close applied'),
    (18, 'Contactor close latched'), (19, '9 V / 5 V supply on'),
    (20, '9 V / 5 V supply applied'), (21, 'Low-power B+ (LPBP) on'),
    (22, 'LPBP applied'), (23, 'LPBP output on'), (24, 'LPBP output applied'),
]
PIO_MY19 = [
    (0, 'Measurement requested'), (1, 'Measurement cancelled'), (2, 'Measurement active'),
    (3, 'Measurement supply on'), (4, 'Measurement supply settled'), (5, 'Supplies held on'),
    (6, 'Second measurement stage on'), (7, 'Second stage settled'),
    (8, 'Fuse-voltage sense on'), (9, 'Fuse-voltage sense settled'),
    (10, 'Precharge requested'), (11, 'Precharge output on'),
    (12, 'Bus voltage ≥ 90 % of pack voltage'), (13, 'Bus voltage ≥ 85 % of pack voltage'),
    (14, 'Contactor close requested'), (15, 'Contactor closed (driven)'),
    (16, 'Contactor closed on previous pass'), (17, 'Contactor feedback closed'),
    (18, 'Pack manager running'), (19, 'Balancing on'), (20, 'Balancing stop pending'),
    (21, 'Read thresholds (one-shot)'), (22, 'Write threshold A (one-shot)'),
    (23, 'Write threshold B (one-shot)'), (24, 'Write balance mask (one-shot)'),
    (25, 'Second stage settled ≥ 2 s'), (26, 'Current sensors zero-offset calibrated'),
    (27, 'Cell monitor configured'),
]

page('bms/periodic.md', f"""
# BMS Periodic Entries

| Type | Name | Payload (bytes) |
|---|---|---|
| `0x4B` | `periodic_small` | 33 / 37 / 39 |
| `0x4C` | `periodic_medium` | 49 / 55 / 57 |
| `0x4D` | `periodic_large` | 57 / 63 / 65 |
| `0x4E` | `soc_snapshot` | 89 |

| Variant | Firmware |
|---|---|
| 33 / 49 / 57 | 2019–20 SR/F (BMS rev 8, 9, 11) |
| 37 / 55 / 63 | BMU rev 3–5 |
| 39 / 57 / 65 | BMU rev 17+ |

## 0x4B -- periodic_small

{table(B4B, vs((33, 37, 39)))}

## 0x4C -- periodic_medium

{table(B4C, vs((49, 55, 57)))}

## 0x4D -- periodic_large

{table(B4D, vs((57, 63, 65)))}

## 0x4E -- soc_snapshot

Logged while charging.

{table(B4E, [(None, 89)])}

## Field definitions

### Status words

| Field | Bit | Mask | Meaning |
|---|---|---|---|
| `entry_status` | 1 | `0x002` | BMS instance missing |
| `entry_error_flags` | 1 | `0x002` | Snapshot not built |
| `snapshot_read_failures` | 1 | `0x002` | Small snapshot failed |
| `snapshot_read_failures` | 9 | `0x200` | `cell_imbalance_mv` unreadable |
| `sensor_read_failures` | 1 | `0x002` | `cell_low_mv` unreadable |
| `sensor_read_failures` | 3 | `0x008` | `cell_high_mv` unreadable |
| `sensor_read_failures` | 5 | `0x020` | `pack_current_ma` unreadable |
| `sensor_read_failures` | 6 | `0x040` | `temp_fuse_c` unreadable |
| `sensor_read_failures` | 10 | `0x400` | `pack_voltage_mv` unreadable |

A set bit means the matching field is not a reading. `soc_pct` = 0 with
`sensor_read_failures` bit 5 set, or with `lowest_cell_oc_mv` = 0, is not a reading.

2019–20 SR/F firmware writes `entry_error_flags` = 1, `sensor_read_failures` = `0x10` in a
reduced-reporting state; `soc_pct` and `pack_current_ma` then read 0.

### bms_faults

Only bits 0–7 are written; bytes 1–7 are always 0.

{bits([(0, 'Logging'), (1, 'Precharge'), (2, 'Contactor'), (3, 'Charge'), (4, 'Discharge'),
       (5, 'Current sensor'), (6, 'Temperature sensor'), (7, 'Temperature sensor alert')])}

### pack_io_control_flags

Select the map by `fw_part` and firmware revision in the [log header](index.md#log-header-0xfb).
MY19 BMS rev ≤ 15: not mapped.

#### BMU (`75-08274`, `75-08384`)

{bits(PIO_BMU, 8)}

Bits 25–31 unused. Typical values: `0x00780033` (contactor open), `0x01FF0033` (bike on).

#### MY19 BMS (`75-08156`, rev 16–26)

{bits(PIO_MY19, 8)}

Typical values: `0x0E0403D8` (idle), `0x0E07F3D8` (contactor closed).

### storage_mode

| Value | Meaning |
|---|---|
| 0 | Normal |
| 1 | Long-term storage mode |
""")

# BMS faults ---------------------------------------------------------------

BOC = [
    F('pack_current_min_a', 's16', 'Pack current minimum, A'),
    F('pack_current_max_a', 's16', 'Pack current maximum, A'),
    F('pack_current_avg_a', 's16', 'Pack current average, A'),
    F('cur_sensor0_mv', 's16', 'Current sensor 0 voltage, mV'),
    F('cur_sensor1_mv', 's16', 'Current sensor 1 voltage, mV'),
    F('max_allowed_amps', 'u16', 'Maximum current allowed, A (discharge or charge)'),
    F('oc_limit_1_a', 'u16', 'Overcurrent limit, tier 1, A'),
    F('oc_limit_2_a', 'u16', 'Overcurrent limit, tier 2, A'),
    F('oc_limit_3_a', 'u16', 'Overcurrent limit, tier 3, A'),
    F('trigger_cell_mv', 's16', 'Discharge: lowest cell; charge: highest cell, mV'),
    F('min_cell_temp_c', 's8', 'Minimum cell temperature, °C'),
    F('max_cell_temp_c', 's8', 'Maximum cell temperature, °C'),
]
B55 = [
    F('contactor_closed', 'u8', '1 = contactor closed'),
    F('aux_state_is_2', 'u8', '1 = auxiliary contactor state 2'),
    F('time_close_enabled_ms', 's32', 'Time contactor close has been enabled, ms'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV'),
    F('switched_bplus_mv', 'u32', 'Switched B+ (load side) voltage, mV'),
]
BVS = [
    F('trigger_cell_mv', 's16', 'Trigger cell voltage, mV'),
    F('trigger_cell_index', 'u8', 'Trigger cell, 0–27. `0xFF` = unavailable'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV'),
    F('cell_voltages', 'u16[28]', 'Cell 0–27 voltages, mV', only={'63 B'}),
]
BTF = [
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
    F('cell_temp_c', 's8', 'OT types: maximum, UT types: minimum cell temperature, °C'),
    F('vpack_slope_1min', 's32', 'Pack voltage slope, 1 min window, mV/min'),
    F('vpack_slope_5min', 's32', 'Pack voltage slope, 5 min window, mV/min'),
]
B65 = [
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
    F('vpack_slope_1min', 's32', 'Pack voltage slope, 1 min window, mV/min'),
    F('vpack_slope_5min', 's32', 'Pack voltage slope, 5 min window, mV/min'),
    F('charge_enabled', 'u8', '1 = pack allows charging'),
    F('charge_commanded', 'u8', '1 = MBB commands charging'),
    F('time_since_charge_disabled_ms', 's32', 'Time since charge last disabled, ms'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV', only={'26 B'}),
    F('charge_target_mv', 's32', 'Charge target voltage, mV', only={'26 B'}),
]
B79 = [
    F('lowest_cell_mv', 's16', 'Lowest unloaded cell voltage, mV'),
    F('lowest_cell_index', 'u8', 'Lowest cell, 0–27. `0xFF` = unavailable'),
    F('highest_cell_mv', 's16', 'Highest unloaded cell voltage, mV'),
    F('highest_cell_index', 'u8', 'Highest cell, 0–27. `0xFF` = unavailable'),
]
B76 = [
    F('lowest_cell_mv', 's16', 'Lowest unloaded cell voltage, mV'),
    F('lvc_threshold_mv', 's16', 'LVC cell voltage threshold, mV'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV'),
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
    F('soc_pct', 'u8', 'State of charge, %'),
]
B77 = [
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV'),
    F('switched_bplus_mv', 'u32', 'Switched B+ (load side) voltage, mV'),
    F('contactor_closed', 'u8', '1 = contactor closed'),
]

page('bms/faults.md', f"""
# BMS Faults

Set and clear entries of a fault share one layout.

## Overcurrent

| Type | Name | Fault code | Direction |
|---|---|---|---|
| `0x4F` | `dis_overcur` | `0x0C` | Discharge, set |
| `0x53` | `dis_overcur_clr` | `0x0C` | Discharge, clear |
| `0x51` | `sev_dis_overcur` | `0x0D` | Discharge severe, set |
| `0x7B` | `sev_dis_overcur_clr` | `0x0D` | Discharge severe, clear |
| `0x50` | `chg_overcur` | `0x0E` | Charge, set |
| `0x54` | `chg_overcur_clr` | `0x0E` | Charge, clear |
| `0x52` | `sev_chg_overcur` | `0x0F` | Charge severe, set |
| `0x7C` | `sev_chg_overcur_clr` | `0x0F` | Charge severe, clear |

{table(BOC, [(None, 22)])}

## 0x55 -- cont_fault

Fault code `0x02`. Clear entry `0x56` has no payload.

{table(B55, [(None, 14)])}

## Voltage

| Type | Name | Fault code | Trigger cell |
|---|---|---|---|
| `0x57` / `0x58` | `ov_fault` / `_clr` | `0x10` | Highest |
| `0x59` / `0x5A` | `uv_chg_fault` / `_clr` | `0x11` | Lowest |
| `0x5B` / `0x5C` | `uv_dischg_fault` / `_clr` | `0x12` | Lowest |

Set entries are 63 bytes; clear entries are 7 bytes.

{table(BVS, [('7 B', 7), ('63 B', 63)])}

## Temperature

| Type | Name | Fault code | Temperature |
|---|---|---|---|
| `0x5D` / `0x5E` | `ot_chg` / `_clr` | `0x13` | Maximum |
| `0x5F` / `0x60` | `ot_dischg` / `_clr` | `0x15` | Maximum |
| `0x61` / `0x62` | `ut_chg` / `_clr` | `0x14` | Minimum |
| `0x63` / `0x64` | `ut_dischg` / `_clr` | `0x16` | Minimum |
| `0x67` / `0x68` | `sev_ot` / `_clr` | `0x17` | Maximum |

{table(BTF, [(None, 13)])}

## 0x65 / 0x66 -- chg_fault

Fault code `0x03`.

{table(B65, [('18 B', 18), ('26 B', 26)])}

18-byte variant: 2019–20 SR/F firmware.

## Isolation and voltage sensor

| Type | Name | Fault code | `value` |
|---|---|---|---|
| `0x69` / `0x6A` | `voltage_sensor` / `_clr` | `0x0B` | Cell voltage sensor raw ADC value |
| `0x74` / `0x75` | `isolation_fault` / `_clr` | `0x19` | Isolation resistance, Ω |
| `0x8C` / `0x8D` | `isolation_severe` / `_clr` | — | Instantaneous isolation resistance, Ω (rev 17+) |

{table([F('value', 'u32', 'See table above')], [(None, 4)])}

## 0x79 / 0x7A -- cell_imbalance

Fault code `0x18`.

{table(B79, [(None, 6)])}

## 0x76 -- lvc

{table(B76, [(None, 13)])}

## 0x77 -- not_ok_precharge

{table(B77, [(None, 13)])}
""")

# BMS cell data ------------------------------------------------------------

B7D = [
    F('static_discharge_current_limit_a', 's16', 'Static discharge current limit, A'),
    F('dynamic_discharge_current_limit_a', 's16', 'Dynamic discharge current limit, A'),
    F('static_charge_current_limit_a', 's16', 'Static charge current limit, A'),
    F('dynamic_charge_current_limit_a', 's16', 'Dynamic charge current limit, A'),
    F('pack_current_a', 's16', 'Pack current, A'),
    F('soc_pct', 'u8', 'State of charge, %'),
    F('lowest_cell_mv', 's16', 'Lowest unloaded cell voltage, mV'),
    F('highest_cell_mv', 's16', 'Highest unloaded cell voltage, mV'),
    F('min_cell_temp_c', 's8', 'Minimum cell temperature, °C'),
    F('max_cell_temp_c', 's8', 'Maximum cell temperature, °C'),
]
B84 = [
    F('cell_mv', 's16', '`0x84`: lowest, `0x85`: highest unloaded cell voltage, mV'),
    F('trigger_cell_index', 'u8', 'Trigger cell, 0–27. `0xFF` = unavailable', only={'3 B'}),
]
CAPEST = values([
    (1, '`timestamp_ms`', 'ms', 'Time since boot'),
    (2, '`capest_c_rate_milli`', 'C × 1000', 'C-rate'),
    (3, '`pack_current_ma`', 'mA', 'Pack current. + = discharge'),
    (4, '`soc_pct`', '%', 'State of charge'),
    (5, '`soc_pct2`', '%', 'Second state of charge'),
    (6, '`est_cap_uah`', 'µAh', 'Estimated capacity (long-term)'),
    (7, '`adj_cap_uah`', 'µAh', 'Adjusted capacity (short-term)'),
    (8, '`sample_cap_uah`', 'µAh', 'Capacity implied by this sample'),
    (9, '`blended_cap_uah`', 'µAh', '[8] blended with [7] by C-rate'),
    (10, '`instant_cap_uah`', 'µAh', 'Running capacity after this sample (low 32 bits)'),
], ('Index', 'Field', 'Unit', 'Description'))

page('bms/cell-data.md', f"""
# BMS Cell Data and Limits

## 0x83 -- cell_voltages

{table([F('cell_voltages', 'u16[28]', 'Cell 0–27 voltages, mV. Valid 800–6501')], [(None, 56)])}

| Cells | CMU board |
|---|---|
| 0–3 | 0 |
| 4–7 | 1 |
| 8–11 | 2 |
| 12–15 | 3 |
| 16–19 | 4 |
| 20–23 | 5 |
| 24–27 | 6 |

## 0x7D -- limits

{table(B7D, [(None, 17)])}

## 0x84 / 0x85 -- charger cell voltage

| Type | Name |
|---|---|
| `0x84` | `cell_too_low_for_chg` |
| `0x85` | `cell_too_high_for_chg` |

{table(B84, [('2 B', 2), ('3 B', 3)])}

3-byte variant: BMU rev 17+.

## 0x86 – 0x89 -- cell temperature limits

| Type | Name |
|---|---|
| `0x86` | `cell_temp_too_low_for_chg` |
| `0x87` | `cell_temp_too_high_for_chg` |
| `0x88` | `cell_temp_too_low_for_dischg` |
| `0x89` | `cell_temp_too_high_for_dischg` |

{table([F('temp_c', 's8', 'Cell temperature, °C')], [(None, 1)])}

## 0xFD -- debug_message

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | variable | `bytes` | `message` | ASCII text, NUL-terminated |

### CapEst line

MY19 BMS `75-08156-19` and `-20` log the capacity estimator as:

```
CapEst, %lld,%d,%d,%d,%d,%d,%d,%d,%lld,%lld
```

{CAPEST}
""")

# BMS diagnostics ----------------------------------------------------------

B6B = [
    F('sensor0_current_a', 's16', 'Current sensor 0 discharge current, A'),
    F('sensor0_voltage_mv', 's16', 'Current sensor 0 voltage, mV'),
    F('sensor1_current_a', 's16', 'Current sensor 1 discharge current, A'),
    F('sensor1_voltage_mv', 's16', 'Current sensor 1 voltage, mV'),
    F('supply_5v_mv', 's16', '5 V supply, filtered, mV'),
    F('vref_mv', 's16', 'ADC reference, filtered, mV'),
    F('time_since_valid_ms', 'u32', 'Time since last valid current reading, ms'),
    F('supply_9v5v_on', 'u8', '1 = 9 V / 5 V supply on'),
]
B6E = [
    F('temp_sensors_c', 'u8[9]', 'Temperature sensors 0–8, °C'),
    F('supply_5v_mv', 's16', '5 V supply, filtered, mV'),
    F('vref_mv', 's16', 'ADC reference, mV'),
    F('time_since_valid_ms', 'u32', 'Time since last valid pack temperature reading, ms'),
]
B70 = [
    F('supply_12v_mv', 's16', 'BMU 12 V supply, filtered, mV'),
    F('supply_12v_out_mv', 's16', '12 V output to bike, filtered, mV'),
    F('supply_5v_good', 'u8', '1 = 5 V supply good'),
    F('bmu_5v_mv', 's16', 'BMU 5 V supply, mV'),
    F('supply_3v3_good', 'u8', '1 = 3.3 V supply good'),
    F('bmu_3v3_mv', 's16', 'BMU 3.3 V supply, mV'),
    F('pack_9v_mv', 's16', 'Pack-side 9 V supply, mV. 0 = off'),
    F('supply_5v_mv', 's16', 'Pack-side 5 V supply, filtered, mV'),
]
B72 = [
    F('ltc_vref_0_mv', 's16', 'Cell monitor 0 reference voltage, mV'),
    F('ltc_vref_1_mv', 's16', 'Cell monitor 1 reference voltage, mV'),
    F('ltc_die_temp_0_c', 's16', 'Cell monitor 0 die temperature, °C'),
    F('ltc_die_temp_1_c', 's16', 'Cell monitor 1 die temperature, °C'),
    F('ltc_digital_supply_0_mv', 's16', 'Cell monitor 0 digital supply, mV'),
    F('ltc_digital_supply_1_mv', 's16', 'Cell monitor 1 digital supply, mV'),
    F('ltc_analog_supply_0_mv', 's16', 'Cell monitor 0 analog supply, mV'),
    F('ltc_analog_supply_1_mv', 's16', 'Cell monitor 1 analog supply, mV'),
]
B78 = [
    F('queue_name', 'char[10]', 'Queue name'),
    F('queue_id', 'u32', 'Queue identifier'),
    F('message_id', 'u32', 'Failed message identifier'),
]
B7E = [
    F('fault_type', 'u8', 'Fault type. 1 = hard fault'),
    F('hfsr', 'u32', 'Hard Fault Status Register'),
    F('cfsr', 'u32', 'Configurable Fault Status Register'),
    F('bfar', 'u32', 'Bus Fault Address Register (valid when CFSR bit 15 set)'),
    F('exception_sp', 'u32', 'Stack pointer at fault'),
    F('lr', 'u32', 'Link register from exception frame'),
    F('pc', 'u32', 'Program counter from exception frame'),
]
B7F = [
    F('temp_c', 's8', 'Fuse temperature, °C'),
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
]
B81 = [
    F('fuse_drop_mv', 's32', 'Voltage drop across the fuse, filtered, mV. 0–120000'),
    F('pack_voltage_mv', 's32', 'Pack voltage, mV'),
    F('pack_current_ma', 's32', 'Pack current, filtered, mA'),
]
CFSR = bits([
    (0, 'IACCVIOL: instruction access violation'), (1, 'DACCVIOL: data access violation'),
    (3, 'MUNSTKERR: unstacking error'), (4, 'MSTKERR: stacking error'), (7, 'MMARVALID'),
    (8, 'IBUSERR: instruction bus error'), (9, 'PRECISERR: precise data bus error'),
    (10, 'IMPRECISERR: imprecise data bus error'), (11, 'UNSTKERR: unstacking error'),
    (12, 'STKERR: stacking error'), (15, 'BFARVALID'),
    (16, 'UNDEFINSTR: undefined instruction'), (17, 'INVSTATE: invalid state'),
    (18, 'INVPC: invalid PC load'), (19, 'NOCP: no coprocessor'),
    (24, 'UNALIGNED: unaligned access'), (25, 'DIVBYZERO: divide by zero'),
], 8)

page('bms/diagnostics.md', f"""
# BMS Diagnostics

## 0x6B / 0x6C -- cur_sense

Fault code `0x05`.

{table(B6B, [(None, 17)])}

## 0x6E / 0x6F -- temp_sen

Fault code `0x06`.

{table(B6E, [(None, 17)])}

## 0x70 / 0x71 -- power_supply

Fault code `0x08`.

{table(B70, [(None, 14)])}

## 0x72 / 0x73 -- pack_io

Fault codes `0x09`, `0x0A`.

{table(B72, [(None, 16)])}

## 0x78 -- queue_send_fail

{table(B78, [(None, 18)])}

## 0x7E -- mcu_fault

Logged at startup after an MCU fault in the previous session.

{table(B7E, [(None, 25)])}

### CFSR bits

{CFSR}

## 0x7F / 0x80 -- fuse_temp

Fault code `0x28`.

{table(B7F, [(None, 5)])}

## 0x81 / 0x82 -- fuse_voltage

Fault code `0x29`.

{table(B81, [(None, 12)])}

## 0x8A / 0x8B -- fan

| Type | Name |
|---|---|
| `0x8A` | `fan_on` |
| `0x8B` | `fan_off` |

{table([F('max_cell_temp_c', 's8', 'Maximum cell temperature when the fan switched, °C')], [(None, 1)])}

## Damaged entries

| Appearance | Meaning |
|---|---|
| `B2 00 F0 …` | Entry overwritten by the download stamp. See [File format](../file-format.md#bms-download-stamp) |
| Type `0x00` | Entry whose type byte was overwritten by the download stamp |
""")

# --------------------------------------------------------------------------
# Firmware versions
# --------------------------------------------------------------------------

MBB_REVS = ['21', '22', '24', '41', '42', '43', '44', '44', '45', '46']
MBB_PKGS = ['486', '519', '611', 'bom5', 'bom2', 'bom13', 'bom14', 'bom18', 'bom43', 'bom4']
MBB_DATES = ['2022-01', '2022-02', '2022-06', '2025-01', '2025-09', '2025-10', '2025-12', '2026-03', '2026-05', '2026-07']
MBB_MATRIX = [
    ('0x46', 'BmsStatus', ['53'] * 10), ('0x47', 'PrechargeStatus', ['22'] * 10),
    ('0x48', 'ChargerDetails', ['49'] * 10), ('0x49', 'ChargingState', ['25'] * 10),
    ('0x4A', 'ElockStatus', ['13'] * 10), ('0x4B', 'PeriodicSmall', ['40'] * 10),
    ('0x4C', 'PeriodicMedium', ['74'] * 10), ('0x4D', 'PeriodicLarge', ['86'] * 10),
    ('0x4E', 'FirmwareUpdated', ['54'] * 10), ('0x4F', 'QueueSendFail', ['18'] * 10),
    ('0x50', 'McuFault', ['25'] * 10),
    ('0x51', 'PeriodicSmall2', ['58'] * 3 + ['62'] * 7),
    ('0x52', 'PeriodicMedium2', ['75'] * 3 + ['79'] * 7),
    ('0x53', 'PeriodicLarge2', ['89'] * 3 + ['93'] * 7),
    ('0x54', 'TorqueInfo', ['—'] * 3 + ['16'] * 7),
    ('0xFB', 'LogHeaderEntry', ['104'] * 10),
]

BMU_REVS = ['3', '4', '5', '17', '17', '18', '19', '20', '21', '22']
BMU_PKGS = ['486', '519', '611', 'bom5', 'bom2', 'bom13', 'bom14', 'bom18', 'bom43', 'bom4']
BMU_DIFF = [
    ('0x4B', 'BmsPeriodicSmall', ['37'] * 3 + ['39'] * 7),
    ('0x4C', 'BmsPeriodicMedium', ['55'] * 3 + ['57'] * 7),
    ('0x4D', 'BmsPeriodicLarge', ['63'] * 3 + ['65'] * 7),
    ('0x84', 'BmsCellTooLowForCharge', ['2'] * 3 + ['3'] * 7),
    ('0x85', 'BmsCellTooHighForCharge', ['2'] * 3 + ['3'] * 7),
    ('0x8C', 'BmsIsolationFaultSevere', ['—'] * 3 + ['4'] * 7),
    ('0x8D', 'BmsIsolationFaultSevereClr', ['—'] * 3 + ['4'] * 7),
    ('0xFB', 'LogHeaderEntry', ['112'] * 10),
]


def matrix(revs, pkgs, rows, dates=None):
    head = ['Type', 'Name'] + [f'rev {r}<br>{p}' for r, p in zip(revs, pkgs)]
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    if dates:
        out.append('| | *Date* | ' + ' | '.join(dates) + ' |')
    for code, name, sizes in rows:
        out.append(f'| `{code}` | `{name}` | ' + ' | '.join(sizes) + ' |')
    return '\n'.join(out)


page('firmware.md', f"""
# Firmware Versions

Payload sizes (bytes) declared by each firmware build.

## MBB (`75-08163`, `75-08383`)

{matrix(MBB_REVS, MBB_PKGS, MBB_MATRIX, MBB_DATES)}

Revisions are those of `75-08163`. `75-08383` has no 486 build; its 519 build is rev 22
and its 611 build is rev 3. Sizes are the same.

### Older MBB firmware

| Firmware | Difference |
|---|---|
| rev 6–11 | Log header 115 bytes, no `fw_build_num` |
| rev 7–11 | `0x48` two chargers in one 98-byte entry |
| rev ≤ 15 | `0x48`, `0x49` currents in mA |
| rev 8–11 | `0x4E` 52 bytes |
| rev ≤ 14 | `0x4C` 71 bytes, `0x4D` 83 bytes |
| rev ≤ 24 | `0x46` byte `0x12` = single eligibility byte |
| rev ≥ 30 | `0x46` byte `0x12` = eligibility bit pair |

## BMU (`75-08274`, `75-08384`)

All BMU types not listed below have the same size in every build: see
[Entry types](bms/index.md#entry-types).

{matrix(BMU_REVS, BMU_PKGS, BMU_DIFF)}

Revisions are those of `75-08274`. `75-08384` has no 486 build; its 519 build is rev 4
and its 611 build is rev 3. Sizes are the same.

### MY19 BMS (`75-08156`)

| Firmware | Difference |
|---|---|
| 2019–20 SR/F (rev 8, 9, 11) | `0x4B`/`0x4C`/`0x4D` 33/49/57 bytes; `0x65`/`0x66` 18 bytes |
| rev 19, 20 | `0xFD` carries the `CapEst` line |

## Package build numbers

`fw_build_num` and `commit_hash` identify the firmware package. All ECU images in one
package share them (e.g. MBB rev 41 and BMU rev 17 in package `bom5`: build 5, commit
`39e9c5ea1`).
""")

for path, text in PAGES.items():
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print('wrote', p)
