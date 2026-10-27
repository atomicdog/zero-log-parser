# BMS Diagnostics

## 0x6B / 0x6C -- cur_sense

Fault code `0x05`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `sensor0_current_a` | Current sensor 0 discharge current, A |
| `0x02` | 2 | `s16` | `sensor0_voltage_mv` | Current sensor 0 voltage, mV |
| `0x04` | 2 | `s16` | `sensor1_current_a` | Current sensor 1 discharge current, A |
| `0x06` | 2 | `s16` | `sensor1_voltage_mv` | Current sensor 1 voltage, mV |
| `0x08` | 2 | `s16` | `supply_5v_mv` | 5 V supply, filtered, mV |
| `0x0A` | 2 | `s16` | `vref_mv` | ADC reference, filtered, mV |
| `0x0C` | 4 | `u32` | `time_since_valid_ms` | Time since last valid current reading, ms |
| `0x10` | 1 | `u8` | `supply_9v5v_on` | 1 = 9 V / 5 V supply on |

## 0x6E / 0x6F -- temp_sen

Fault code `0x06`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 9 | `u8[9]` | `temp_sensors_c` | Temperature sensors 0–8, °C |
| `0x09` | 2 | `s16` | `supply_5v_mv` | 5 V supply, filtered, mV |
| `0x0B` | 2 | `s16` | `vref_mv` | ADC reference, mV |
| `0x0D` | 4 | `u32` | `time_since_valid_ms` | Time since last valid pack temperature reading, ms |

## 0x70 / 0x71 -- power_supply

Fault code `0x08`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `supply_12v_mv` | BMU 12 V supply, filtered, mV |
| `0x02` | 2 | `s16` | `supply_12v_out_mv` | 12 V output to bike, filtered, mV |
| `0x04` | 1 | `u8` | `supply_5v_good` | 1 = 5 V supply good |
| `0x05` | 2 | `s16` | `bmu_5v_mv` | BMU 5 V supply, mV |
| `0x07` | 1 | `u8` | `supply_3v3_good` | 1 = 3.3 V supply good |
| `0x08` | 2 | `s16` | `bmu_3v3_mv` | BMU 3.3 V supply, mV |
| `0x0A` | 2 | `s16` | `pack_9v_mv` | Pack-side 9 V supply, mV. 0 = off |
| `0x0C` | 2 | `s16` | `supply_5v_mv` | Pack-side 5 V supply, filtered, mV |

## 0x72 / 0x73 -- pack_io

Fault codes `0x09`, `0x0A`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `s16` | `ltc_vref_0_mv` | Cell monitor 0 reference voltage, mV |
| `0x02` | 2 | `s16` | `ltc_vref_1_mv` | Cell monitor 1 reference voltage, mV |
| `0x04` | 2 | `s16` | `ltc_die_temp_0_c` | Cell monitor 0 die temperature, °C |
| `0x06` | 2 | `s16` | `ltc_die_temp_1_c` | Cell monitor 1 die temperature, °C |
| `0x08` | 2 | `s16` | `ltc_digital_supply_0_mv` | Cell monitor 0 digital supply, mV |
| `0x0A` | 2 | `s16` | `ltc_digital_supply_1_mv` | Cell monitor 1 digital supply, mV |
| `0x0C` | 2 | `s16` | `ltc_analog_supply_0_mv` | Cell monitor 0 analog supply, mV |
| `0x0E` | 2 | `s16` | `ltc_analog_supply_1_mv` | Cell monitor 1 analog supply, mV |

## 0x78 -- queue_send_fail

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 10 | `char[10]` | `queue_name` | Queue name |
| `0x0A` | 4 | `u32` | `queue_id` | Queue identifier |
| `0x0E` | 4 | `u32` | `message_id` | Failed message identifier |

## 0x7E -- mcu_fault

Logged at startup after an MCU fault in the previous session.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `fault_type` | Fault type. 1 = hard fault |
| `0x01` | 4 | `u32` | `hfsr` | Hard Fault Status Register |
| `0x05` | 4 | `u32` | `cfsr` | Configurable Fault Status Register |
| `0x09` | 4 | `u32` | `bfar` | Bus Fault Address Register (valid when CFSR bit 15 set) |
| `0x0D` | 4 | `u32` | `exception_sp` | Stack pointer at fault |
| `0x11` | 4 | `u32` | `lr` | Link register from exception frame |
| `0x15` | 4 | `u32` | `pc` | Program counter from exception frame |

### CFSR bits

| Bit | Mask | Meaning |
|---|---|---|
| 0 | `0x00000001` | IACCVIOL: instruction access violation |
| 1 | `0x00000002` | DACCVIOL: data access violation |
| 3 | `0x00000008` | MUNSTKERR: unstacking error |
| 4 | `0x00000010` | MSTKERR: stacking error |
| 7 | `0x00000080` | MMARVALID |
| 8 | `0x00000100` | IBUSERR: instruction bus error |
| 9 | `0x00000200` | PRECISERR: precise data bus error |
| 10 | `0x00000400` | IMPRECISERR: imprecise data bus error |
| 11 | `0x00000800` | UNSTKERR: unstacking error |
| 12 | `0x00001000` | STKERR: stacking error |
| 15 | `0x00008000` | BFARVALID |
| 16 | `0x00010000` | UNDEFINSTR: undefined instruction |
| 17 | `0x00020000` | INVSTATE: invalid state |
| 18 | `0x00040000` | INVPC: invalid PC load |
| 19 | `0x00080000` | NOCP: no coprocessor |
| 24 | `0x01000000` | UNALIGNED: unaligned access |
| 25 | `0x02000000` | DIVBYZERO: divide by zero |

## 0x7F / 0x80 -- fuse_temp

Fault code `0x28`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `s8` | `temp_c` | Fuse temperature, °C |
| `0x01` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |

## 0x81 / 0x82 -- fuse_voltage

Fault code `0x29`.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `s32` | `fuse_drop_mv` | Voltage drop across the fuse, filtered, mV. 0–120000 |
| `0x04` | 4 | `s32` | `pack_voltage_mv` | Pack voltage, mV |
| `0x08` | 4 | `s32` | `pack_current_ma` | Pack current, filtered, mA |

## 0x8A / 0x8B -- fan

| Type | Name |
|---|---|
| `0x8A` | `fan_on` |
| `0x8B` | `fan_off` |

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `s8` | `max_cell_temp_c` | Maximum cell temperature when the fan switched, °C |

## Damaged entries

| Appearance | Meaning |
|---|---|
| `B2 00 F0 …` | Entry overwritten by the download stamp. See [File format](../file-format.md#bms-download-stamp) |
| Type `0x00` | Entry whose type byte was overwritten by the download stamp |
