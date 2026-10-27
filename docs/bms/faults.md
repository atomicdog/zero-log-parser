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

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `pack_current_min_a` | Pack current minimum, A |
| `0x02` | 2 | `s16` | `pack_current_max_a` | Pack current maximum, A |
| `0x04` | 2 | `s16` | `pack_current_avg_a` | Pack current average, A |
| `0x06` | 2 | `s16` | `cur_sensor0_mv` | Current sensor 0 voltage, mV |
| `0x08` | 2 | `s16` | `cur_sensor1_mv` | Current sensor 1 voltage, mV |
| `0x0A` | 2 | `u16` | `max_allowed_amps` | Maximum current allowed, A (discharge or charge) |
| `0x0C` | 2 | `u16` | `oc_limit_1_a` | Overcurrent limit, tier 1, A |
| `0x0E` | 2 | `u16` | `oc_limit_2_a` | Overcurrent limit, tier 2, A |
| `0x10` | 2 | `u16` | `oc_limit_3_a` | Overcurrent limit, tier 3, A |
| `0x12` | 2 | `s16` | `trigger_cell_mv` | Discharge: lowest cell; charge: highest cell, mV |
| `0x14` | 1 | `s8` | `max_cell_temp_c` | Maximum cell temperature, °C |
| `0x15` | 1 | `u8` | `min_cell_temp_c` | Minimum cell temperature, °C |

## 0x55 -- cont_fault

Fault code `0x02`. Clear entry `0x56` has no payload.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `contactor_closed` | 1 = contactor closed |
| `0x01` | 1 | `u8` | `aux_state_is_2` | 1 = auxiliary contactor state 2 |
| `0x02` | 4 | `s32` | `time_close_enabled_ms` | Time contactor close has been enabled, ms |
| `0x06` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x0A` | 4 | `u32` | `switched_bplus_mv` | Switched B+ (load side) voltage, mV |

## Voltage

| Type | Name | Fault code | Trigger cell |
|---|---|---|---|
| `0x57` / `0x58` | `ov_fault` / `_clr` | `0x10` | Highest |
| `0x59` / `0x5A` | `uv_chg_fault` / `_clr` | `0x11` | Lowest |
| `0x5B` / `0x5C` | `uv_dischg_fault` / `_clr` | `0x12` | Lowest |

Set entries are 63 bytes; clear entries are 7 bytes.

| Offset<br>7 B | Offset<br>63 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 2 | `s16` | `trigger_cell_mv` | Trigger cell voltage, mV |
| `0x02` | `0x02` | 1 | `u8` | `trigger_cell_index` | Trigger cell, 0–27. `0xFF` = unavailable |
| `0x03` | `0x03` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| — | `0x07` | 56 | `u16[28]` | `cell_voltages` | Cell 0–27 voltages, mV |

## Temperature

| Type | Name | Fault code | Temperature |
|---|---|---|---|
| `0x5D` / `0x5E` | `ot_chg` / `_clr` | `0x13` | Maximum |
| `0x5F` / `0x60` | `ot_dischg` / `_clr` | `0x15` | Maximum |
| `0x61` / `0x62` | `ut_chg` / `_clr` | `0x14` | Minimum |
| `0x63` / `0x64` | `ut_dischg` / `_clr` | `0x16` | Minimum |
| `0x67` / `0x68` | `sev_ot` / `_clr` | `0x17` | Maximum |

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |
| `0x04` | 1 | `s8` | `cell_temp_c` | OT types: maximum, UT types: minimum cell temperature, °C |
| `0x05` | 4 | `s32` | `vpack_slope_1min` | Pack voltage slope, 1 min window, mV/min |
| `0x09` | 4 | `s32` | `vpack_slope_5min` | Pack voltage slope, 5 min window, mV/min |

## 0x65 / 0x66 -- chg_fault

Fault code `0x03`.

| Offset<br>18 B | Offset<br>26 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |
| `0x04` | `0x04` | 4 | `s32` | `vpack_slope_1min` | Pack voltage slope, 1 min window, mV/min |
| `0x08` | `0x08` | 4 | `s32` | `vpack_slope_5min` | Pack voltage slope, 5 min window, mV/min |
| `0x0C` | `0x0C` | 1 | `u8` | `charge_enabled` | 1 = pack allows charging |
| `0x0D` | `0x0D` | 1 | `u8` | `charge_commanded` | 1 = MBB commands charging |
| `0x0E` | `0x0E` | 4 | `s32` | `time_since_charge_disabled_ms` | Time since charge last disabled, ms |
| — | `0x12` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| — | `0x16` | 4 | `s32` | `charge_target_mv` | Charge target voltage, mV |

18-byte variant: 2019–20 SR/F firmware.

## Isolation and voltage sensor

| Type | Name | Fault code | `value` |
|---|---|---|---|
| `0x69` / `0x6A` | `voltage_sensor` / `_clr` | `0x0B` | Cell voltage sensor raw ADC value |
| `0x74` / `0x75` | `isolation_fault` / `_clr` | `0x19` | Isolation resistance, Ω |
| `0x8C` / `0x8D` | `isolation_severe` / `_clr` | — | Instantaneous isolation resistance, Ω (rev 17+) |

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `u32` | `value` | See table above |

## 0x79 / 0x7A -- cell_imbalance

Fault code `0x18`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `lowest_cell_mv` | Lowest unloaded cell voltage, mV |
| `0x02` | 1 | `u8` | `lowest_cell_index` | Lowest cell, 0–27. `0xFF` = unavailable |
| `0x03` | 2 | `s16` | `highest_cell_mv` | Highest unloaded cell voltage, mV |
| `0x05` | 1 | `u8` | `highest_cell_index` | Highest cell, 0–27. `0xFF` = unavailable |

## 0x76 -- lvc

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `lowest_cell_mv` | Lowest unloaded cell voltage, mV |
| `0x02` | 2 | `s16` | `lvc_threshold_mv` | LVC cell voltage threshold, mV |
| `0x04` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x08` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |
| `0x0C` | 1 | `u8` | `soc_pct` | State of charge, % |

## 0x77 -- not_ok_precharge

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |
| `0x04` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x08` | 4 | `u32` | `switched_bplus_mv` | Switched B+ (load side) voltage, mV |
| `0x0C` | 1 | `u8` | `contactor_closed` | 1 = contactor closed |
