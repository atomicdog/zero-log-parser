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

| Offset<br>33 B | Offset<br>37 B | Offset<br>39 B | Size | Type | Field | Description |
|---|---|---|---|---|---|---|
| `0x00` | `0x00` | `0x00` | 4 | `u32` | `entry_error_flags` | See [Status words](#status-words) |
| `0x04` | `0x04` | `0x04` | 4 | `u32` | `sensor_read_failures` | See [Status words](#status-words) |
| `0x08` | `0x08` | `0x08` | 2 | `u16` | `cell_low_mv` | Lowest cell voltage, mV |
| `0x0A` | `0x0A` | `0x0A` | 2 | `u16` | `lowest_cell_oc_mv` | Lowest cell open-circuit voltage, mV. 0 = no estimate |
| `0x0C` | `0x0C` | `0x0C` | 2 | `u16` | `cell_high_mv` | Highest cell voltage, mV |
| `0x0E` | `0x0E` | `0x0E` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x0F` | `0x0F` | `0x0F` | 4 | `s32` | `pack_current_ma` | Pack current, mA |
| `0x13` | `0x13` | `0x13` | 1 | `s8` | `temp_fuse_c` | Fuse temperature, °C |
| `0x14` | `0x14` | `0x14` | 4 | `u32` | `pack_io_control_flags` | See [pack_io_control_flags](#pack_io_control_flags) |
| `0x18` | `0x18` | `0x18` | 8 | `u64` | `bms_faults` | Active faults. See [bms_faults](#bms_faults) |
| `0x20` | `0x20` | `0x20` | 1 | `u8` | `num_cmu_boards` | CMU boards in the pack |
| — | `0x21` | `0x21` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| — | — | `0x25` | 1 | `u8` | `lowest_cell_index` | Lowest cell, 0–27. `0xFF` = unavailable |
| — | — | `0x26` | 1 | `u8` | `highest_cell_index` | Highest cell, 0–27. `0xFF` = unavailable |

## 0x4C -- periodic_medium

| Offset<br>49 B | Offset<br>55 B | Offset<br>57 B | Size | Type | Field | Description |
|---|---|---|---|---|---|---|
| `0x00` | `0x00` | `0x00` | 4 | `u32` | `entry_error_flags` | See [Status words](#status-words) |
| `0x04` | `0x04` | `0x04` | 4 | `u32` | `snapshot_read_failures` | See [Status words](#status-words) |
| `0x08` | `0x08` | `0x08` | 4 | `u32` | `sensor_read_failures` | See [Status words](#status-words) |
| `0x0C` | `0x0C` | `0x0C` | 2 | `u16` | `cell_low_mv` | Lowest cell voltage, mV |
| `0x0E` | `0x0E` | `0x0E` | 2 | `u16` | `lowest_cell_oc_mv` | Lowest cell open-circuit voltage, mV. 0 = no estimate |
| `0x10` | `0x10` | `0x10` | 2 | `u16` | `cell_high_mv` | Highest cell voltage, mV |
| `0x12` | `0x12` | `0x12` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x13` | `0x13` | `0x13` | 4 | `s32` | `pack_current_ma` | Pack current, mA |
| `0x17` | `0x17` | `0x17` | 1 | `s8` | `temp_fuse_c` | Fuse temperature, °C |
| `0x18` | `0x18` | `0x18` | 4 | `u32` | `pack_io_control_flags` | See [pack_io_control_flags](#pack_io_control_flags) |
| `0x1C` | `0x1C` | `0x1C` | 8 | `u64` | `bms_faults` | Active faults. See [bms_faults](#bms_faults) |
| `0x24` | `0x24` | `0x24` | 1 | `u8` | `num_cmu_boards` | CMU boards in the pack |
| — | `0x25` | `0x25` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| — | — | `0x29` | 1 | `u8` | `lowest_cell_index` | Lowest cell, 0–27. `0xFF` = unavailable |
| — | — | `0x2A` | 1 | `u8` | `highest_cell_index` | Highest cell, 0–27. `0xFF` = unavailable |
| `0x25` | `0x29` | `0x2B` | 1 | `s8` | `temp_board_c` | Minimum cell temperature, °C |
| `0x26` | `0x2A` | `0x2C` | 1 | `s8` | `temp_ambient_c` | Maximum cell temperature, °C |
| `0x27` | `0x2B` | `0x2D` | 1 | `u8` | `soc_meas_disch_pct` | SOC from measured discharge vs ideal capacity, % |
| `0x28` | `0x2C` | `0x2E` | 2 | `u16` | `max_disch_amps` | Maximum discharge current allowed, A |
| `0x2A` | `0x2E` | `0x30` | 2 | `u16` | `max_chg_amps` | Maximum charge current allowed, A |
| `0x2C` | `0x30` | `0x32` | 4 | `u32` | `adj_pack_cap_mah` | Adjusted pack capacity, mAh |
| `0x30` | `0x34` | `0x36` | 1 | `u8` | `storage_mode` | 1 = long-term storage mode |
| — | `0x35` | `0x37` | 2 | `s16` | `cell_imbalance_mv` | Highest − lowest cell voltage, mV |

## 0x4D -- periodic_large

| Offset<br>57 B | Offset<br>63 B | Offset<br>65 B | Size | Type | Field | Description |
|---|---|---|---|---|---|---|
| `0x00` | `0x00` | `0x00` | 4 | `u32` | `entry_status` | See [Status words](#status-words) |
| `0x04` | `0x04` | `0x04` | 4 | `u32` | `entry_error_flags` | See [Status words](#status-words) |
| `0x08` | `0x08` | `0x08` | 4 | `u32` | `snapshot_read_failures` | See [Status words](#status-words) |
| `0x0C` | `0x0C` | `0x0C` | 4 | `u32` | `sensor_read_failures` | See [Status words](#status-words) |
| `0x10` | `0x10` | `0x10` | 2 | `u16` | `cell_low_mv` | Lowest cell voltage, mV |
| `0x12` | `0x12` | `0x12` | 2 | `u16` | `lowest_cell_oc_mv` | Lowest cell open-circuit voltage, mV. 0 = no estimate |
| `0x14` | `0x14` | `0x14` | 2 | `u16` | `cell_high_mv` | Highest cell voltage, mV |
| `0x16` | `0x16` | `0x16` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x17` | `0x17` | `0x17` | 4 | `s32` | `pack_current_ma` | Pack current, mA |
| `0x1B` | `0x1B` | `0x1B` | 1 | `s8` | `temp_fuse_c` | Fuse temperature, °C |
| `0x1C` | `0x1C` | `0x1C` | 4 | `u32` | `pack_io_control_flags` | See [pack_io_control_flags](#pack_io_control_flags) |
| `0x20` | `0x20` | `0x20` | 8 | `u64` | `bms_faults` | Active faults. See [bms_faults](#bms_faults) |
| `0x28` | `0x28` | `0x28` | 1 | `u8` | `num_cmu_boards` | CMU boards in the pack |
| — | `0x29` | `0x29` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| — | — | `0x2D` | 1 | `u8` | `lowest_cell_index` | Lowest cell, 0–27. `0xFF` = unavailable |
| — | — | `0x2E` | 1 | `u8` | `highest_cell_index` | Highest cell, 0–27. `0xFF` = unavailable |
| `0x29` | `0x2D` | `0x2F` | 1 | `s8` | `temp_board_c` | Minimum cell temperature, °C |
| `0x2A` | `0x2E` | `0x30` | 1 | `s8` | `temp_ambient_c` | Maximum cell temperature, °C |
| `0x2B` | `0x2F` | `0x31` | 1 | `u8` | `soc_meas_disch_pct` | SOC from measured discharge vs ideal capacity, % |
| `0x2C` | `0x30` | `0x32` | 2 | `u16` | `max_disch_amps` | Maximum discharge current allowed, A |
| `0x2E` | `0x32` | `0x34` | 2 | `u16` | `max_chg_amps` | Maximum charge current allowed, A |
| `0x30` | `0x34` | `0x36` | 4 | `u32` | `adj_pack_cap_mah` | Adjusted pack capacity, mAh |
| `0x34` | `0x38` | `0x3A` | 1 | `u8` | `storage_mode` | 1 = long-term storage mode |
| — | `0x39` | `0x3B` | 2 | `s16` | `cell_imbalance_mv` | Highest − lowest cell voltage, mV |
| `0x35` | `0x3B` | `0x3D` | 4 | `u32` | `est_pack_cap_mah` | Estimated pack capacity, mAh |

## 0x4E -- soc_snapshot

Logged while charging.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `dis_cur_sensor0_ma` | Discharge current, sensor 0, mA |
| `0x02` | 2 | `s16` | `dis_cur_sensor1_ma` | Discharge current, sensor 1, mA |
| `0x04` | 4 | `s32` | `total_pack_dis_current_ma` | Total pack discharge current, filtered, mA |
| `0x08` | 2 | `s16` | `zero_a` | Always 0 |
| `0x0A` | 2 | `s16` | `lowest_unloaded_cell_mv` | Lowest unloaded cell voltage, mV |
| `0x0C` | 2 | `s16` | `lowest_cell_oc_mv` | Lowest cell open-circuit voltage, mV |
| `0x0E` | 1 | `s8` | `mean_pack_temp_c` | Mean pack temperature, °C |
| `0x0F` | 1 | `u8` | `soc_ocv_raw_pct` | SOC from cell voltage, unfiltered, % |
| `0x10` | 1 | `u8` | `soc_ocv_filt_pct` | SOC from cell voltage, filtered, % |
| `0x11` | 1 | `u8` | `soc_ref_pct` | SOC at last reset, % |
| `0x12` | 1 | `u8` | `soc_blend_input_pct` | Blend-filter input SOC, % |
| `0x13` | 1 | `u8` | `soc_meas_vs_ideal_mah_pct` | SOC, measured mAh vs ideal capacity, % |
| `0x14` | 1 | `u8` | `soc_meas_vs_ideal_mwh_pct` | SOC, measured mWh vs ideal capacity, % |
| `0x15` | 1 | `u8` | `soc_est_vs_adj_mah_pct` | SOC, estimated mAh vs adjusted capacity, % (reported SOC) |
| `0x16` | 1 | `u8` | `soc_est_vs_adj_alt_pct` | SOC, secondary accumulator, % |
| `0x17` | 4 | `u32` | `adj_pack_cap_mah` | Adjusted pack capacity, mAh |
| `0x1B` | 4 | `u32` | `est_pack_cap_mah` | Estimated pack capacity, mAh |
| `0x1F` | 4 | `u32` | `adj_pack_cap_mwh` | Adjusted pack capacity, mWh |
| `0x23` | 4 | `u32` | `est_pack_cap_mwh` | Estimated pack capacity, mWh |
| `0x27` | 4 | `u32` | `meas_disch_mah` | Measured discharge, mAh |
| `0x2B` | 4 | `u32` | `est_disch_mah` | Estimated discharge, mAh |
| `0x2F` | 4 | `u32` | `meas_disch_mwh` | Measured discharge, mWh |
| `0x33` | 4 | `u32` | `est_disch_mwh` | Estimated discharge, mWh |
| `0x37` | 4 | `u32` | `ideal_pack_cap_mah` | Ideal (new) pack capacity, mAh |
| `0x3B` | 4 | `u32` | `ideal_pack_cap_mwh` | Ideal (new) pack capacity, mWh |
| `0x3F` | 4 | `s32` | `reserved_zero_a` | Always 0 |
| `0x43` | 4 | `s32` | `reserved_zero_b` | Always 0 |
| `0x47` | 4 | `u32` | `reserved_zero_c` | Always 0 |
| `0x4B` | 4 | `u32` | `measured_cell_impedance_uohm` | Measured cell impedance, µΩ. 0 = not yet measured |
| `0x4F` | 2 | `s16` | `estimated_cell_sag_mv` | Estimated cell sag under load, mV |
| `0x51` | 2 | `s16` | `measured_cell_sag_mv` | Measured cell sag, mV |
| `0x53` | 2 | `s16` | `zero_b` | Always 0 |
| `0x55` | 4 | `s32` | `reserved_zero_d` | Always 0 |

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

| Bit | Mask | Meaning |
|---|---|---|
| 0 | `0x01` | Logging |
| 1 | `0x02` | Precharge |
| 2 | `0x04` | Contactor |
| 3 | `0x08` | Charge |
| 4 | `0x10` | Discharge |
| 5 | `0x20` | Current sensor |
| 6 | `0x40` | Temperature sensor |
| 7 | `0x80` | Temperature sensor alert |

### pack_io_control_flags

Select the map by `fw_part` in the [log header](index.md#log-header-0xfb).

#### BMU (`75-08274`, `75-08384`)

| Bit | Mask | Meaning |
|---|---|---|
| 0 | `0x00000001` | Cell measurements requested |
| 1 | `0x00000002` | Cell measurements applied |
| 2 | `0x00000004` | Read UV/OV thresholds (one-shot) |
| 3 | `0x00000008` | Threshold read sent |
| 4 | `0x00000010` | Pack ADC measurements requested |
| 5 | `0x00000020` | Pack ADC measurements applied |
| 6 | `0x00000040` | Write OV threshold (one-shot) |
| 7 | `0x00000080` | OV threshold written |
| 8 | `0x00000100` | Write UV threshold (one-shot) |
| 9 | `0x00000200` | UV threshold written |
| 10 | `0x00000400` | Balancing requested |
| 11 | `0x00000800` | Balancing applied |
| 12 | `0x00001000` | Precharge enable requested |
| 13 | `0x00002000` | Precharge enable applied |
| 14 | `0x00004000` | Precharge on requested |
| 15 | `0x00008000` | Precharge on applied |
| 16 | `0x00010000` | Contactor close requested |
| 17 | `0x00020000` | Contactor close applied |
| 18 | `0x00040000` | Contactor close latched |
| 19 | `0x00080000` | 9 V / 5 V supply on |
| 20 | `0x00100000` | 9 V / 5 V supply applied |
| 21 | `0x00200000` | Low-power B+ (LPBP) on |
| 22 | `0x00400000` | LPBP applied |
| 23 | `0x00800000` | LPBP output on |
| 24 | `0x01000000` | LPBP output applied |

Bits 25–31 unused. Typical values: `0x00780033` (contactor open), `0x01FF0033` (bike on).

#### MY19 BMS (`75-08156`, rev 16–26)

| Bit | Mask | Meaning |
|---|---|---|
| 0 | `0x00000001` | Measurement requested |
| 1 | `0x00000002` | Measurement cancelled |
| 2 | `0x00000004` | Measurement active |
| 3 | `0x00000008` | Measurement supply on |
| 4 | `0x00000010` | Measurement supply settled |
| 5 | `0x00000020` | Supplies held on |
| 6 | `0x00000040` | Second measurement stage on |
| 7 | `0x00000080` | Second stage settled |
| 8 | `0x00000100` | Fuse-voltage sense on |
| 9 | `0x00000200` | Fuse-voltage sense settled |
| 10 | `0x00000400` | Precharge requested |
| 11 | `0x00000800` | Precharge output on |
| 12 | `0x00001000` | Bus voltage ≥ 90 % of pack voltage |
| 13 | `0x00002000` | Bus voltage ≥ 85 % of pack voltage |
| 14 | `0x00004000` | Contactor close requested |
| 15 | `0x00008000` | Contactor closed (driven) |
| 16 | `0x00010000` | Contactor closed on previous pass |
| 17 | `0x00020000` | Contactor feedback closed |
| 18 | `0x00040000` | Pack manager running |
| 19 | `0x00080000` | Balancing on |
| 20 | `0x00100000` | Balancing stop pending |
| 21 | `0x00200000` | Read thresholds (one-shot) |
| 22 | `0x00400000` | Write threshold A (one-shot) |
| 23 | `0x00800000` | Write threshold B (one-shot) |
| 24 | `0x01000000` | Write balance mask (one-shot) |
| 25 | `0x02000000` | Second stage settled ≥ 2 s |
| 26 | `0x04000000` | Current sensors zero-offset calibrated |
| 27 | `0x08000000` | Cell monitor configured |

Typical values: `0x0E0403D8` (idle), `0x0E07F3D8` (contactor closed).

### storage_mode

| Value | Meaning |
|---|---|
| 0 | Normal |
| 1 | Long-term storage mode |
