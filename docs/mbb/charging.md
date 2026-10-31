# MBB Charging

## 0x48 -- charger_details

One entry per charger.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 10 | `bytes[10]` | `name` | Charger name, NUL-padded (e.g. ` 3kW`) |
| `0x0A` | 2 | `u16` | `status` | Status word. See [status](#status) |
| `0x0C` | 4 | `u32` | `dc_output_mv` | DC output voltage, mV |
| `0x10` | 2 | `u16` | `dc_current_a` | DC output current, A. mA in rev 7–15 |
| `0x12` | 2 | `u16` | `max_charge_current_a` | Maximum charge current, A. mA in rev 7–15 |
| `0x14` | 4 | `u32` | `max_charge_voltage_mv` | Maximum charge voltage, mV |
| `0x18` | 1 | `u8` | `cmd_in_a` | AC input current limit, A |
| `0x19` | 1 | `u8` | `charger_variant` | Charger model/firmware code. See [charger_variant](#charger_variant) |
| `0x1A` | 1 | `u8` | `ac_volts_v` | AC input voltage, V |
| `0x1B` | 2 | `u16` | `ac_current_a` | AC input current, A. mA in rev 7–15 |
| `0x1D` | 1 | `u8` | `ac_hz` | AC frequency, Hz |
| `0x1E` | 1 | `s8` | `temp_c` | Charger temperature, °C |
| `0x1F` | 1 | `u8` | `can_id` | CANopen node ID. `0x10` = first, `0x11` = second |
| `0x20` | 2 | `u16` | `version` | Charger firmware version |
| `0x22` | 4 | `u32` | `serial_number` | Charger serial number |
| `0x26` | 2 | `u16` | `status_code` | Charger type. See [status_code](#status_code) |
| `0x28` | 4 | `u32` | `setpt_voltage_mv` | Commanded charge voltage, mV |
| `0x2C` | 2 | `u16` | `setpt_current_a` | Commanded charge current, A. mA in rev 7–15 |
| `0x2E` | 2 | `u16` | `setpt_ac_input_a` | Commanded AC input current limit, A |
| `0x30` | 1 | `u8` | `en_flag` | Charger enabled |

Firmware rev 7–11: two chargers are logged as one 98-byte entry (two consecutive records).

| MBB firmware | Current fields |
|---|---|
| rev 7–15 | mA |
| rev 17+ | A |

### status

| Value | Meaning |
|---|---|
| `0x0480` | Charging, 110 V AC |
| `0x0080` | Charging, 220 V AC |
| `0x0020` | Idle |

### status_code

| Value | Meaning |
|---|---|
| 9 | 3 kW onboard charger |
| 10 | 6 kW onboard charger |
| 17 | Reserved |
| 28 | Calex charger |
| 29 | Flat 6 kW charger |

### charger_variant

Low bits give the power class: 1 = 3 kW, 2 = 6 kW.

| Value | Charger |
|---|---|
| 9 | 3 kW, firmware 101 / 201 |
| 10 | 6 kW, firmware 100 / 200 |
| 17 | 3 kW, firmware 202–207; 3kWFCC |
| 34 | Flt 6 (Calex) |

## 0x49 -- charging_state

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `u32` | `charging_target_mv` | Charge voltage target, mV |
| `0x04` | 2 | `u16` | `evse_pilot_current_a` | EVSE pilot current limit, A. 127 = no limit |
| `0x06` | 1 | `u8` | `charge_target_pct` | Charge target, % SOC |
| `0x07` | 2 | `u16` | `charger_output_current_a` | Total charger DC output current, A. mA in rev ≤ 15 |
| `0x09` | 4 | `s32` | `charge_current_a` | Total charge current, A. mA in rev ≤ 15 |
| `0x0D` | 1 | `u8` | `evse_disconnect_flags` | 0 = EVSE connected |
| `0x0E` | 1 | `u8` | `schedule_charge_enabled` | 1 = scheduled charging enabled |
| `0x0F` | 4 | `u32` | `active_sched_window_val` | Today's charge windows. See [active_sched_window_val](#active_sched_window_val) |
| `0x13` | 1 | `u8` | `charging_enabled` | 1 = charging enabled |
| `0x14` | 1 | `u8` | `evse_allowed_current_a` | EVSE allowed current, A |
| `0x15` | 4 | `u32` | `hard_charge_target_mv` | Hard charge target, mV. 0 = disabled |

### active_sched_window_val

Four bytes, in 30-minute slots. Times are after the bike's time-offset setting.

| Byte | Field | Range |
|---|---|---|
| 0 | Window A duration | 0–48 |
| 1 | Window A start | 0–47 |
| 2 | Window B duration | 0–48 |
| 3 | Window B start | 0–47 |

| Window | Role |
|---|---|
| A | Puts the charger into `WAIT` |
| B | Starts charging |

Window roles are from one firmware build.

The value is logged whether or not `schedule_charge_enabled` is set. A day setting of 0
leaves the previous value in place.

This layout applies from rev 13 onward. In rev 6–11, many non-zero values are not schedules.
