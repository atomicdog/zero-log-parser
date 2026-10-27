# BMS

## Log header (`0xFB`)

Entry offsets (equal to file offsets once the entry is un-escaped).

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `sof` | `0xB2` |
| `0x01` | 1 | `u8` | `length` | Entry length on disk, including header and escape bytes |
| `0x02` | 1 | `u8` | `type` | `0xFB` |
| `0x03` | 4 | `u32` | `timestamp` | Download time, Unix seconds, UTC |
| `0x07` | 4 | `u32` | `usec` | Microseconds |
| `0x0B` | 1 | `u8` | `count` | Rolling entry counter |
| `0x0C` | 1 | `s8` | `utc_offset` | UTC offset, hours |
| `0x0D` | 10 | `char[10]` | `device_name` | `BMS` |
| `0x17` | 16 | `char[16]` | `module_model` | Module model (e.g. `FST BCB`) |
| `0x27` | 1 | `u8` | `num_parallel_cells` | Cells in parallel per series group |
| `0x28` | 16 | `char[16]` | `board_part` | Board part number (e.g. `40-08295-01`) |
| `0x38` | 16 | `char[16]` | `serial` | BMS serial number |
| `0x48` | 16 | `char[16]` | `bcbm_id` | BCBM identifier (e.g. `BCBM2546`) |
| `0x58` | 16 | `char[16]` | `fw_part` | BMU firmware part number (`75-08274`, `75-08384`) |
| `0x68` | 2 | `u16` | `fw_rev_num` | Firmware revision |
| `0x6A` | 2 | `u16` | `fw_build_num` | Firmware package build number |
| `0x6C` | 16 | `char[16]` | `commit_hash` | Firmware package git commit hash |
| `0x7C` | 1 | `u8` | `firmware_bank` | Running flash bank. 1 = A, 2 = B |

A 126-byte variant carries one trailing `0x00`.

### Board variants

| `fw_part` | `board_part` | MCU |
|---|---|---|
| `75-08274` | `40-08247-01` | Infineon XMC4500 |
| `75-08384` | `40-08295-01` | Infineon XMC4800 |

Both produce identical entry layouts.

## Entry types

| Type | Name | Payload (bytes) | Description | Layout |
|---|---|---|---|---|
| `0x4B` | `periodic_small` | 33 / 37 / 39 | Periodic snapshot, small | [Periodic](periodic.md#0x4b-periodic_small) |
| `0x4C` | `periodic_medium` | 49 / 55 / 57 | Periodic snapshot, medium | [Periodic](periodic.md#0x4c-periodic_medium) |
| `0x4D` | `periodic_large` | 57 / 63 / 65 | Periodic snapshot, large | [Periodic](periodic.md#0x4d-periodic_large) |
| `0x4E` | `soc_snapshot` | 89 | State-of-charge estimator snapshot | [Periodic](periodic.md#0x4e-soc_snapshot) |
| `0x4F` | `dis_overcur` | 22 | Discharge overcurrent, set | [Faults](faults.md#overcurrent) |
| `0x50` | `chg_overcur` | 22 | Charge overcurrent, set | [Faults](faults.md#overcurrent) |
| `0x51` | `sev_dis_overcur` | 22 | Severe discharge overcurrent, set | [Faults](faults.md#overcurrent) |
| `0x52` | `sev_chg_overcur` | 22 | Severe charge overcurrent, set | [Faults](faults.md#overcurrent) |
| `0x53` | `dis_overcur_clr` | 22 | Discharge overcurrent, clear | [Faults](faults.md#overcurrent) |
| `0x54` | `chg_overcur_clr` | 22 | Charge overcurrent, clear | [Faults](faults.md#overcurrent) |
| `0x55` | `cont_fault` | 14 | Contactor fault, set | [Faults](faults.md#0x55-cont_fault) |
| `0x56` | `cont_fault_clr` | 0 | Contactor fault, clear | — |
| `0x57` | `ov_fault` | 63 | Cell overvoltage, set | [Faults](faults.md#voltage) |
| `0x58` | `ov_fault_clr` | 7 | Cell overvoltage, clear | [Faults](faults.md#voltage) |
| `0x59` | `uv_chg_fault` | 63 | Cell undervoltage (charge), set | [Faults](faults.md#voltage) |
| `0x5A` | `uv_chg_fault_clr` | 7 | Cell undervoltage (charge), clear | [Faults](faults.md#voltage) |
| `0x5B` | `uv_dischg_fault` | 63 | Cell undervoltage (discharge), set | [Faults](faults.md#voltage) |
| `0x5C` | `uv_dischg_fault_clr` | 7 | Cell undervoltage (discharge), clear | [Faults](faults.md#voltage) |
| `0x5D` | `ot_chg` | 13 | Overtemperature (charge), set | [Faults](faults.md#temperature) |
| `0x5E` | `ot_chg_clr` | 13 | Overtemperature (charge), clear | [Faults](faults.md#temperature) |
| `0x5F` | `ot_dischg` | 13 | Overtemperature (discharge), set | [Faults](faults.md#temperature) |
| `0x60` | `ot_dischg_clr` | 13 | Overtemperature (discharge), clear | [Faults](faults.md#temperature) |
| `0x61` | `ut_chg` | 13 | Undertemperature (charge), set | [Faults](faults.md#temperature) |
| `0x62` | `ut_chg_clr` | 13 | Undertemperature (charge), clear | [Faults](faults.md#temperature) |
| `0x63` | `ut_dischg` | 13 | Undertemperature (discharge), set | [Faults](faults.md#temperature) |
| `0x64` | `ut_dischg_clr` | 13 | Undertemperature (discharge), clear | [Faults](faults.md#temperature) |
| `0x65` | `chg_fault` | 18 / 26 | Charge fault, set | [Faults](faults.md#0x65-0x66-chg_fault) |
| `0x66` | `chg_fault_clr` | 18 / 26 | Charge fault, clear | [Faults](faults.md#0x65-0x66-chg_fault) |
| `0x67` | `sev_ot` | 13 | Severe overtemperature, set | [Faults](faults.md#temperature) |
| `0x68` | `sev_ot_clr` | 13 | Severe overtemperature, clear | [Faults](faults.md#temperature) |
| `0x69` | `voltage_sensor` | 4 | Voltage sensor fault, set | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0x6A` | `voltage_sensor_clr` | 4 | Voltage sensor fault, clear | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0x6B` | `cur_sense` | 17 | Current sensor fault, set | [Diagnostics](diagnostics.md#0x6b-0x6c-cur_sense) |
| `0x6C` | `cur_sense_clr` | 17 | Current sensor fault, clear | [Diagnostics](diagnostics.md#0x6b-0x6c-cur_sense) |
| `0x6D` | `can_sync_fail` | 0 | CAN sync failure | — |
| `0x6E` | `temp_sen` | 17 | Temperature sensor fault, set | [Diagnostics](diagnostics.md#0x6e-0x6f-temp_sen) |
| `0x6F` | `temp_sen_clr` | 17 | Temperature sensor fault, clear | [Diagnostics](diagnostics.md#0x6e-0x6f-temp_sen) |
| `0x70` | `power_supply` | 14 | Power supply fault, set | [Diagnostics](diagnostics.md#0x70-0x71-power_supply) |
| `0x71` | `power_supply_clr` | 14 | Power supply fault, clear | [Diagnostics](diagnostics.md#0x70-0x71-power_supply) |
| `0x72` | `pack_io` | 16 | Pack I/O fault, set | [Diagnostics](diagnostics.md#0x72-0x73-pack_io) |
| `0x73` | `pack_io_clr` | 16 | Pack I/O fault, clear | [Diagnostics](diagnostics.md#0x72-0x73-pack_io) |
| `0x74` | `isolation_fault` | 4 | Isolation fault, set | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0x75` | `isolation_fault_clr` | 4 | Isolation fault, clear | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0x76` | `lvc` | 13 | Low-voltage cutoff | [Faults](faults.md#0x76-lvc) |
| `0x77` | `not_ok_precharge` | 13 | Not OK to precharge | [Faults](faults.md#0x77-not_ok_precharge) |
| `0x78` | `queue_send_fail` | 18 | RTOS queue send failure | [Diagnostics](diagnostics.md#0x78-queue_send_fail) |
| `0x79` | `cell_imbalance` | 6 | Cell imbalance, set | [Faults](faults.md#0x79-0x7a-cell_imbalance) |
| `0x7A` | `cell_imbalance_clr` | 6 | Cell imbalance, clear | [Faults](faults.md#0x79-0x7a-cell_imbalance) |
| `0x7B` | `sev_dis_overcur_clr` | 22 | Severe discharge overcurrent, clear | [Faults](faults.md#overcurrent) |
| `0x7C` | `sev_chg_overcur_clr` | 22 | Severe charge overcurrent, clear | [Faults](faults.md#overcurrent) |
| `0x7D` | `limits` | 17 | Operating limits | [Cell data](cell-data.md#0x7d-limits) |
| `0x7E` | `mcu_fault` | 25 | MCU fault registers | [Diagnostics](diagnostics.md#0x7e-mcu_fault) |
| `0x7F` | `fuse_temp` | 5 | Fuse temperature fault, set | [Diagnostics](diagnostics.md#0x7f-0x80-fuse_temp) |
| `0x80` | `fuse_temp_clr` | 5 | Fuse temperature fault, clear | [Diagnostics](diagnostics.md#0x7f-0x80-fuse_temp) |
| `0x81` | `fuse_voltage` | 12 | Fuse voltage fault, set | [Diagnostics](diagnostics.md#0x81-0x82-fuse_voltage) |
| `0x82` | `fuse_voltage_clr` | 12 | Fuse voltage fault, clear | [Diagnostics](diagnostics.md#0x81-0x82-fuse_voltage) |
| `0x83` | `cell_voltages` | 56 | All cell voltages | [Cell data](cell-data.md#0x83-cell_voltages) |
| `0x84` | `cell_too_low_for_chg` | 2 / 3 | Cell too low to charge | [Cell data](cell-data.md#0x84-0x85-charger-cell-voltage) |
| `0x85` | `cell_too_high_for_chg` | 2 / 3 | Cell too high to charge | [Cell data](cell-data.md#0x84-0x85-charger-cell-voltage) |
| `0x86` | `cell_temp_too_low_for_chg` | 1 | Cell too cold to charge | [Cell data](cell-data.md#0x86-0x89-cell-temperature-limits) |
| `0x87` | `cell_temp_too_high_for_chg` | 1 | Cell too hot to charge | [Cell data](cell-data.md#0x86-0x89-cell-temperature-limits) |
| `0x88` | `cell_temp_too_low_for_dischg` | 1 | Cell too cold to discharge | [Cell data](cell-data.md#0x86-0x89-cell-temperature-limits) |
| `0x89` | `cell_temp_too_high_for_dischg` | 1 | Cell too hot to discharge | [Cell data](cell-data.md#0x86-0x89-cell-temperature-limits) |
| `0x8A` | `fan_on` | 0 | Fan turned on | — |
| `0x8B` | `fan_off` | 0 | Fan turned off | — |
| `0x8C` | `isolation_severe` | 4 | Severe isolation fault, set (rev 17+) | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0x8D` | `isolation_severe_clr` | 4 | Severe isolation fault, clear (rev 17+) | [Faults](faults.md#isolation-and-voltage-sensor) |
| `0xFB` | `log_header` | 112 | Log header (first entry of the file) | [Log header](#log-header-0xfb) |
| `0xFD` | `debug_message` | variable | Text message | [Cell data](cell-data.md#0xfd-debug_message) |

Payload sizes given as `a / b` have several firmware variants, selected by payload length.
See [Firmware versions](../firmware.md).

## Sign convention

BMS current fields: + = discharge, − = charge. (MBB `pack_current_ma` uses the same sign.)
