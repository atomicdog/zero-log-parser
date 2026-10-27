# BMS Cell Data and Limits

## 0x83 -- cell_voltages

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 56 | `u16[28]` | `cell_voltages` | Cell 0–27 voltages, mV. Valid 800–6501 |

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

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `static_discharge_current_limit_a` | Static discharge current limit, A |
| `0x02` | 2 | `s16` | `dynamic_discharge_current_limit_a` | Dynamic discharge current limit, A |
| `0x04` | 2 | `s16` | `static_charge_current_limit_a` | Static charge current limit, A |
| `0x06` | 2 | `s16` | `dynamic_charge_current_limit_a` | Dynamic charge current limit, A |
| `0x08` | 2 | `s16` | `pack_current_a` | Pack current, A |
| `0x0A` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x0B` | 2 | `s16` | `lowest_cell_mv` | Lowest unloaded cell voltage, mV |
| `0x0D` | 2 | `s16` | `highest_cell_mv` | Highest unloaded cell voltage, mV |
| `0x0F` | 1 | `s8` | `min_cell_temp_c` | Minimum cell temperature, °C |
| `0x10` | 1 | `s8` | `max_cell_temp_c` | Maximum cell temperature, °C |

## 0x84 / 0x85 -- charger cell voltage

| Type | Name |
|---|---|
| `0x84` | `cell_too_low_for_chg` |
| `0x85` | `cell_too_high_for_chg` |

| Offset<br>2 B | Offset<br>3 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 2 | `s16` | `cell_mv` | `0x84`: lowest, `0x85`: highest unloaded cell voltage, mV |
| — | `0x02` | 1 | `u8` | `trigger_cell_index` | Trigger cell, 0–27. `0xFF` = unavailable |

3-byte variant: BMU rev 17+.

## 0x86 – 0x89 -- cell temperature limits

| Type | Name |
|---|---|
| `0x86` | `cell_temp_too_low_for_chg` |
| `0x87` | `cell_temp_too_high_for_chg` |
| `0x88` | `cell_temp_too_low_for_dischg` |
| `0x89` | `cell_temp_too_high_for_dischg` |

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `s8` | `temp_c` | Cell temperature, °C |

## 0xFD -- debug_message

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | variable | `bytes` | `message` | ASCII text, NUL-terminated |

### CapEst line

MY19 BMS `75-08156-19` and `-20` log the capacity estimator as:

```
CapEst, %lld,%d,%d,%d,%d,%d,%d,%d,%lld,%lld
```

| Index | Field | Unit | Description |
|---|---|---|---|
| 1 | `timestamp_ms` | ms | Time since boot |
| 2 | `capest_c_rate_milli` | C × 1000 | C-rate |
| 3 | `pack_current_ma` | mA | Pack current. + = discharge |
| 4 | `soc_pct` | % | State of charge |
| 5 | `soc_pct2` | % | Second state of charge |
| 6 | `est_cap_uah` | µAh | Estimated capacity (long-term) |
| 7 | `adj_cap_uah` | µAh | Adjusted capacity (short-term) |
| 8 | `sample_cap_uah` | µAh | Capacity implied by this sample |
| 9 | `blended_cap_uah` | µAh | [8] blended with [7] by C-rate |
| 10 | `instant_cap_uah` | µAh | Running capacity after this sample (low 32 bits) |
