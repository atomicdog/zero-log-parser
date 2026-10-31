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

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x08` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x0C` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x10` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x14` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x15` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x19` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x1D` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x22` | 4 | `s32` | `speed_mm_hr` | Rear wheel speed, mm/h (÷ 10⁶ = km/h). See [speed_mm_hr](#speed_mm_hr) |
| `0x26` | 2 | `u16` | `range_km_x100` | Estimated range, km × 100 |

## 0x4C -- periodic_medium

| Offset<br>71 B | Offset<br>74 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | `0x04` | 4 | `u32` | `freeze_status` | See [freeze_status](#freeze_status) |
| `0x08` | `0x08` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x0C` | `0x0C` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x10` | `0x10` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x14` | `0x14` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x18` | `0x18` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x19` | `0x19` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x1D` | `0x1D` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x21` | `0x21` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x26` | `0x26` | 4 | `s32` | `speed_mm_hr` | Rear wheel speed, mm/h (÷ 10⁶ = km/h). See [speed_mm_hr](#speed_mm_hr) |
| `0x2A` | `0x2A` | 2 | `u16` | `range_km_x100` | Estimated range, km × 100 |
| `0x2C` | `0x2C` | 4 | `u32` | `temp_flags` | Temperature read failures. See [temp_flags](#temp_flags) |
| `0x30` | `0x30` | 4 | `s32` | `ambient_c` | Ambient temperature, °C. See [ambient_c](#ambient_c) |
| `0x34` | `0x34` | 4 | `s32` | `t1_c` | Motor temperature, °C. 0 / −1 = unavailable |
| `0x38` | `0x38` | 4 | `s32` | `t2_c` | Controller temperature, °C. 0 / −1 = unavailable |
| `0x3C` | `0x3C` | 4 | `s32` | `bms_high_c` | Highest cell temperature, °C. −1 = unavailable |
| `0x40` | `0x40` | 4 | `s32` | `bms_low_c` | Lowest cell temperature, °C. −1 = unavailable |
| `0x44` | `0x44` | 1 | `u8` | `num_can_modules` | BMS modules on CAN |
| `0x45` | `0x45` | 1 | `u8` | `num_contactors_closed` | Contactors closed |
| `0x46` | — | 1 | `u8` | `odometer_low_byte` | Odometer low byte, km × 10 |
| — | `0x46` | 4 | `u32` | `odometer_km_x10` | Odometer, km × 10. See [odometer_km_x10](#odometer_km_x10) |

71 bytes: firmware rev 6–14. 74 bytes: firmware rev 21+ (not observed in logs).

## 0x4D -- periodic_large

| Offset<br>83 B | Offset<br>86 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | `0x04` | 4 | `u32` | `freeze_med2_err` | Bit 1 = medium snapshot failed. Undefined in rev 6–14 |
| `0x08` | `0x08` | 4 | `u32` | `freeze_status` | See [freeze_status](#freeze_status) |
| `0x0C` | `0x0C` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x10` | `0x10` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x14` | `0x14` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x18` | `0x18` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x1C` | `0x1C` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x1D` | `0x1D` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x21` | `0x21` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x25` | `0x25` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x2A` | `0x2A` | 4 | `s32` | `speed_mm_hr` | Rear wheel speed, mm/h (÷ 10⁶ = km/h). See [speed_mm_hr](#speed_mm_hr) |
| `0x2E` | `0x2E` | 2 | `u16` | `range_km_x100` | Estimated range, km × 100 |
| `0x30` | `0x30` | 4 | `u32` | `temp_flags` | Temperature read failures. See [temp_flags](#temp_flags) |
| `0x34` | `0x34` | 4 | `s32` | `ambient_c` | Ambient temperature, °C. See [ambient_c](#ambient_c) |
| `0x38` | `0x38` | 4 | `s32` | `t1_c` | Motor temperature, °C. 0 / −1 = unavailable |
| `0x3C` | `0x3C` | 4 | `s32` | `t2_c` | Controller temperature, °C. 0 / −1 = unavailable |
| `0x40` | `0x40` | 4 | `s32` | `bms_high_c` | Highest cell temperature, °C. −1 = unavailable |
| `0x44` | `0x44` | 4 | `s32` | `bms_low_c` | Lowest cell temperature, °C. −1 = unavailable |
| `0x48` | `0x48` | 1 | `u8` | `num_can_modules` | BMS modules on CAN |
| `0x49` | `0x49` | 1 | `u8` | `num_contactors_closed` | Contactors closed |
| `0x4A` | — | 1 | `u8` | `odometer_low_byte` | Odometer low byte, km × 10 |
| — | `0x4A` | 4 | `u32` | `odometer_km_x10` | Odometer, km × 10. See [odometer_km_x10](#odometer_km_x10) |
| `0x4B` | `0x4E` | 1 | `u8` | `controller_fault_code` | Motor controller fault code. 0 = none |
| `0x4C` | `0x4F` | 1 | `u8` | `pack_index` | BMS slot of the next two fields (0) |
| `0x4D` | `0x50` | 4 | `u32` | `module_status_bits` | Status bits of that slot. See [module_status_bits](status.md#module_status_bits) |
| `0x51` | `0x54` | 2 | `u16` | `capacity_ah` | Capacity of that slot, Ah |

83 bytes: firmware rev 6–14. 86 bytes: firmware rev 21+ (not observed in logs).

## 0x51 -- periodic_small2

| Offset<br>58 B | Offset<br>62 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | `0x04` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x08` | `0x08` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x0C` | `0x0C` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x10` | `0x10` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x14` | `0x14` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x15` | `0x15` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x19` | `0x19` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x1D` | `0x1D` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x22` | `0x22` | 4 | `u32` | `temp_flags` | Temperature read failures. See [temp_flags](#temp_flags) |
| `0x26` | `0x26` | 4 | `s32` | `ambient_c` | Ambient temperature, °C × 100; °C in rev 18–19. See [ambient_c](#ambient_c) |
| `0x2A` | `0x2A` | 4 | `s32` | `t1_c` | Motor temperature, °C. 0 / −1 = unavailable |
| `0x2E` | `0x2E` | 4 | `s32` | `t2_c` | Controller temperature, °C. 0 / −1 = unavailable |
| `0x32` | `0x32` | 4 | `s32` | `bms_high_c` | Highest cell temperature, °C. −1 = unavailable |
| `0x36` | `0x36` | 4 | `s32` | `bms_low_c` | Lowest cell temperature, °C. −1 = unavailable |
| — | `0x3A` | 4 | `u32` | `battery_12v` | 12 V battery voltage, µV |

## 0x52 -- periodic_medium2

| Offset<br>75 B | Offset<br>79 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | `0x04` | 4 | `u32` | `freeze_med2_flags` | Validity flags. See [freeze_med2_flags](#freeze_med2_flags) |
| `0x08` | `0x08` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x0C` | `0x0C` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x10` | `0x10` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x14` | `0x14` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x18` | `0x18` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x19` | `0x19` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x1D` | `0x1D` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x21` | `0x21` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x26` | `0x26` | 4 | `u32` | `temp_flags` | Temperature read failures. See [temp_flags](#temp_flags) |
| `0x2A` | `0x2A` | 4 | `s32` | `ambient_c` | Ambient temperature, °C × 100; °C in rev 18–19. See [ambient_c](#ambient_c) |
| `0x2E` | `0x2E` | 4 | `s32` | `t1_c` | Motor temperature, °C. 0 / −1 = unavailable |
| `0x32` | `0x32` | 4 | `s32` | `t2_c` | Controller temperature, °C. 0 / −1 = unavailable |
| `0x36` | `0x36` | 4 | `s32` | `bms_high_c` | Highest cell temperature, °C. −1 = unavailable |
| `0x3A` | `0x3A` | 4 | `s32` | `bms_low_c` | Lowest cell temperature, °C. −1 = unavailable |
| — | `0x3E` | 4 | `u32` | `battery_12v` | 12 V battery voltage, µV |
| `0x3E` | `0x42` | 1 | `u8` | `num_can_modules` | BMS modules on CAN |
| `0x3F` | `0x43` | 1 | `u8` | `num_contactors_closed` | Contactors closed |
| `0x40` | `0x44` | 4 | `u32` | `odometer_km_x10` | Odometer, km × 10. See [odometer_km_x10](#odometer_km_x10) |
| `0x44` | `0x48` | 4 | `s32` | `speed_mm_hr` | Rear wheel speed, mm/h (÷ 10⁶ = km/h). See [speed_mm_hr](#speed_mm_hr) |
| `0x48` | `0x4C` | 2 | `u16` | `range_km_x100` | Estimated range, km × 100 |
| `0x4A` | `0x4E` | 1 | `u8` | `bms_lowest_dis_allow` | Lowest BMS discharge allowance |

## 0x53 -- periodic_large2

| Offset<br>89 B | Offset<br>93 B | Size | Type | Field | Description |
|---|---|---|---|---|---|
| `0x00` | `0x00` | 4 | `u32` | `error_flags` | Result code. 0 = OK, 2 = no app instance (rev ≤ 11: 1 = reads failed) |
| `0x04` | `0x04` | 4 | `u32` | `freeze_med2_err` | Read failures. See [freeze_med2_err](#freeze_med2_err) |
| `0x08` | `0x08` | 4 | `u32` | `freeze_med2_flags` | Validity flags. See [freeze_med2_flags](#freeze_med2_flags) |
| `0x0C` | `0x0C` | 4 | `u32` | `status_flags` | Validity flags. See [status_flags](#status_flags) |
| `0x10` | `0x10` | 4 | `s32` | `dc_bus_voltage_mv` | Controller DC bus voltage, mV (multiple of 100) |
| `0x14` | `0x14` | 4 | `s32` | `dc_bus_current_ma` | Controller DC bus current, mA (multiple of 100). + = discharge |
| `0x18` | `0x18` | 4 | `s32` | `motor_rpm` | Motor speed, rpm (×14/13 applied) |
| `0x1C` | `0x1C` | 1 | `u8` | `soc_pct` | State of charge, % |
| `0x1D` | `0x1D` | 4 | `u32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x21` | `0x21` | 4 | `s32` | `pack_current_ma` | Pack current, mA. + = discharge, − = charge/regen |
| `0x25` | `0x25` | 5 | `char[5]` | `state` | Bike state. See [State](#state) |
| `0x2A` | `0x2A` | 4 | `u32` | `temp_flags` | Temperature read failures. See [temp_flags](#temp_flags) |
| `0x2E` | `0x2E` | 4 | `s32` | `ambient_c` | Ambient temperature, °C × 100; °C in rev 18–19. See [ambient_c](#ambient_c) |
| `0x32` | `0x32` | 4 | `s32` | `t1_c` | Motor temperature, °C. 0 / −1 = unavailable |
| `0x36` | `0x36` | 4 | `s32` | `t2_c` | Controller temperature, °C. 0 / −1 = unavailable |
| `0x3A` | `0x3A` | 4 | `s32` | `bms_high_c` | Highest cell temperature, °C. −1 = unavailable |
| `0x3E` | `0x3E` | 4 | `s32` | `bms_low_c` | Lowest cell temperature, °C. −1 = unavailable |
| — | `0x42` | 4 | `u32` | `battery_12v` | 12 V battery voltage, µV |
| `0x42` | `0x46` | 1 | `u8` | `num_can_modules` | BMS modules on CAN |
| `0x43` | `0x47` | 1 | `u8` | `num_contactors_closed` | Contactors closed |
| `0x44` | `0x48` | 4 | `u32` | `odometer_km_x10` | Odometer, km × 10. See [odometer_km_x10](#odometer_km_x10) |
| `0x48` | `0x4C` | 4 | `s32` | `speed_mm_hr` | Rear wheel speed, mm/h (÷ 10⁶ = km/h). See [speed_mm_hr](#speed_mm_hr) |
| `0x4C` | `0x50` | 2 | `u16` | `range_km_x100` | Estimated range, km × 100 |
| `0x4E` | `0x52` | 1 | `u8` | `bms_lowest_dis_allow` | Lowest BMS discharge allowance |
| `0x4F` | `0x53` | 1 | `u8` | `controller_fault_code` | Motor controller fault code. 0 = none |
| `0x50` | `0x54` | 1 | `u8` | `pack_index` | BMS slot of the next two fields (0) |
| `0x51` | `0x55` | 4 | `u32` | `module_status_bits` | Status bits of that slot. See [module_status_bits](status.md#module_status_bits) |
| `0x55` | `0x59` | 2 | `u16` | `capacity_ah` | Capacity of that slot, Ah |
| `0x57` | `0x5B` | 1 | `u8` | `bms_avg_dis_allow` | Average BMS discharge allowance |
| `0x58` | `0x5C` | 1 | `u8` | `bms_avg_chg_allow` | Average BMS charge allowance |

## 0x54 -- torque_info

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `s32` | `torque_unm` | Motor torque, µNm |
| `0x04` | 4 | `s32` | `torque_demand_pct_x10` | Torque demand, % × 10 (−1000…1000). − = regen |
| `0x08` | 4 | `s32` | `filtered_motor_power_w` | Motor power, first-order low-pass filtered, W. 0 at power-on |
| `0x0C` | 4 | `s32` | `disch_power_limit_w` | Discharge power limit, W. −1 = BMS not active |

## Field definitions

### state

5-byte NUL-padded ASCII. Empty when the lookup failed (`status_flags` bit 7).

| Index | String | State |
|---|---|---|
| 0 | `NONE` | No state |
| 1 | `STRT` | Start |
| 2 | `PWSU` | Power supply up |
| 3 | `WAKE` | Wake |
| 4 | `HIB` | Hibernate |
| 5 | `STOP` | Stop |
| 6 | `RUN` | Run |
| 7 | `LIMP` | Limp |
| 8 | `CHRG` | Charge |
| 9 | `WAIT` | Wait |
| 10 | `FWUP` | Firmware update |
| 11 | `REV` | Reverse |
| 12 | `PARK` | Park |

### status_flags

`0x51`–`0x53`. A set bit means the field is not a valid reading.

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x002` | `dc_bus_voltage_mv` invalid |
| 2 | `0x004` | `dc_bus_current_ma` invalid (not set by firmware) |
| 3 | `0x008` | `motor_rpm` invalid |
| 5 | `0x020` | `pack_voltage_mv` invalid |
| 6 | `0x040` | `pack_current_ma` invalid |
| 7 | `0x080` | `state` lookup failed |
| 8 | `0x100` | Temperature block failed |
| 9 | `0x200` | `battery_12v` invalid |

`0x4B`–`0x4D`: bit 8 (`0x100`) = `speed_mm_hr` invalid. Other bits are not mapped.

A zero `dc_bus_current_ma` with bit 1 set means no controller data.

### speed_mm_hr

Rear wheel speed from the ABS module: CAN `0x12B` bytes 2–3, `u16` × 56,250 mm/h. Values are
multiples of 56,250.

### odometer_km_x10

Exactly 100 m per count. Derived from motor revolutions and a gearing setting, not from wheel
speed, so it does not match `speed_mm_hr` integrated over time.

| Platform | Odometer distance / rear wheel distance |
|---|---|
| SR/F, SR/S, SR, S | 1.006 |
| DSR/X, DSR | 1.052 |
| DS | 1.051 |

### ambient_c

| Entry | MBB firmware | Unit |
|---|---|---|
| `0x4C`, `0x4D` | rev 6–14 | °C |
| `0x51`–`0x53` | rev 13–17 | °C × 100 |
| `0x51`–`0x53` | rev 18–19 | °C |
| `0x51`–`0x53` | rev 20+ | °C × 100 |

### temp_flags

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x02` | `ambient_c` read failed |
| 2 | `0x04` | `t1_c` read failed |
| 3 | `0x08` | `t2_c` read failed |
| 4 | `0x10` | `bms_high_c` read failed |
| 5 | `0x20` | `bms_low_c` read failed |

### freeze_med2_flags

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x02` | Small snapshot failed |
| 5 | `0x20` | `speed_mm_hr` invalid |
| 7 | `0x80` | `bms_lowest_dis_allow` invalid |

### freeze_med2_err

`0x53`. A set bit means the read failed.

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x02` | Medium snapshot failed |
| 6 | `0x40` | `bms_avg_dis_allow` unavailable |
| 7 | `0x80` | `bms_avg_chg_allow` unavailable |

### freeze_status

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x02` | Small snapshot failed |
| 2 | `0x04` | Temperature block failed |
