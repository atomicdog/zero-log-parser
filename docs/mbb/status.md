# MBB BMS and Lock Status

## 0x46 -- bms_status

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `u32` | `error_result` | 0 = OK, 2 = module not found |
| `0x04` | 4 | `u32` | `error_flags` | Bit 7 = module name mismatch, bit 8 = precharge info failed |
| `0x08` | 1 | `u8` | `module_id` | BMS module index, 0–5 |
| `0x09` | 8 | `u64` | `time_since_ms` | Time since module timestamp event, ms |
| `0x11` | 1 | `u8` | `module_registered` | 1 = registered |
| `0x12` | 1 | `u8` | `eligibility_flags` | See [eligibility_flags](#eligibility_flags) |
| `0x13` | 2 | `u16` | `capacity_ah` | Module capacity, Ah |
| `0x15` | 4 | `u32` | `pack_voltage_mv` | Module pack voltage, mV |
| `0x19` | 10 | `char[10]` | `module_name` | Module device name |
| `0x23` | 4 | `u32` | `precharge_status_bits` | Bit 3 = precharge percentage unreadable |
| `0x27` | 1 | `u8` | `precharge_state_active` | 1 = precharge in progress |
| `0x28` | 1 | `u8` | `precharge_active_bit` | `module_status_bits` bit 2 |
| `0x29` | 1 | `u8` | `precharge_pct` | Precharge, 0–100 % |
| `0x2A` | 1 | `u8` | `connect_state_closed` | 1 = MBB connection state is closed |
| `0x2B` | 1 | `u8` | `contactor_closed_bit` | `module_status_bits` bit 1 |
| `0x2C` | 1 | `u8` | `module_locked` | 1 = module locked by MBB |
| `0x2D` | 4 | `s32` | `pack_current_ma` | Module pack current, mA |
| `0x31` | 4 | `u32` | `module_status_bits` | See [module_status_bits](#module_status_bits) |

### eligibility_flags

| Firmware | Value |
|---|---|
| rev ≤ 24 | 1 = module eligible |
| rev ≥ 30 | Bit 0 = discharge eligible, bit 1 = charge eligible |

### module_status_bits

| Bit | Mask | Meaning |
|---|---|---|
| 1 | `0x02` | Contactor closed |
| 2 | `0x04` | Precharging |
| 4 | `0x10` | Discharge enabled |
| 5 | `0x20` | Charge enabled |

Upper bits carry BMS fault flags (not mapped).

## 0x47 -- precharge_status

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 4 | `u32` | `error_flags` | 0 = OK, `0x2` = module name unavailable, `0x8` = precharge percentage unreadable |
| `0x04` | 10 | `char[10]` | `module_name` | Module device name |
| `0x0E` | 1 | `u8` | `module_id` | BMS module index |
| `0x0F` | 4 | `u32` | `precharge_status_bits` | Bit 3 = precharge percentage unreadable |
| `0x13` | 1 | `u8` | `precharge_state_active` | 1 = precharge in progress |
| `0x14` | 1 | `u8` | `precharge_active_bit` | `module_status_bits` bit 2 |
| `0x15` | 1 | `u8` | `precharge_pct` | Precharge, 0–100 % |

## 0x4A -- elock_status

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `immobilizer_locked` | 1 = immobilized, 0 = not immobilized |
| `0x01` | 1 | `u8` | `elock_status_flag` | Lock frame byte 6, bit 4 |
| `0x02` | 4 | `u32` | `elock_addr` | Lock device ID. 0 = no frame, `0xFFFFFFFF` = unprogrammed |
| `0x06` | 1 | `u8` | `elock_sw_version` | Lock software version |
| `0x07` | 1 | `u8` | `elock_status_code` | Lock status. See [elock_status_code](#elock_status_code) |
| `0x08` | 1 | `u8` | `auth_flag` | Lock frame byte 1, bit 4. 1 = authenticated |
| `0x09` | 1 | `u8` | `key_number` | Key slot, 0 = none, 1–5 |
| `0x0A` | 1 | `u8` | `status_flag_2` | Lock frame byte 7, bit 2, inverted |
| `0x0B` | 1 | `u8` | `transponder_auth_ok` | Lock frame byte 7, bit 3, inverted. Tracks device presence |
| `0x0C` | 1 | `u8` | `reset_request` | 1 = re-pair request pending |

Logged on: key on with no lock frame, unregistered lock seen, lock registered, re-pair
request and re-pair success.

### elock_status_code

| Value | Meaning |
|---|---|
| 0 | Invalid |
| 1 | Unlocked |
| 2 | Locked |
| 3 | Failed |
| 4 | OK |
