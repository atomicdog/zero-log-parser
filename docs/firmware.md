# Firmware Versions

Payload sizes (bytes) declared by each firmware build.

## MBB (`75-08163`, `75-08383`)

| Type | Name | rev 21<br>486 | rev 22<br>519 | rev 24<br>611 | rev 41<br>bom5 | rev 42<br>bom2 | rev 43<br>bom13 | rev 44<br>bom14 | rev 44<br>bom18 |
|---|---|---|---|---|---|---|---|---|---|
| | *Date* | 2022-01 | 2022-02 | 2022-06 | 2025-01 | 2025-09 | 2025-10 | 2025-12 | 2026-03 |
| `0x46` | `BmsStatus` | 53 | 53 | 53 | 53 | 53 | 53 | 53 | 53 |
| `0x47` | `PrechargeStatus` | 22 | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| `0x48` | `ChargerDetails` | 49 | 49 | 49 | 49 | 49 | 49 | 49 | 49 |
| `0x49` | `ChargingState` | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| `0x4A` | `ElockStatus` | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| `0x4B` | `PeriodicSmall` | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| `0x4C` | `PeriodicMedium` | 74 | 74 | 74 | 74 | 74 | 74 | 74 | 74 |
| `0x4D` | `PeriodicLarge` | 86 | 86 | 86 | 86 | 86 | 86 | 86 | 86 |
| `0x4E` | `FirmwareUpdated` | 54 | 54 | 54 | 54 | 54 | 54 | 54 | 54 |
| `0x4F` | `QueueSendFail` | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 |
| `0x50` | `McuFault` | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| `0x51` | `PeriodicSmall2` | 58 | 58 | 58 | 62 | 62 | 62 | 62 | 62 |
| `0x52` | `PeriodicMedium2` | 75 | 75 | 75 | 79 | 79 | 79 | 79 | 79 |
| `0x53` | `PeriodicLarge2` | 89 | 89 | 89 | 93 | 93 | 93 | 93 | 93 |
| `0x54` | `TorqueInfo` | — | — | — | 16 | 16 | 16 | 16 | 16 |
| `0xFB` | `LogHeaderEntry` | 104 | 104 | 104 | 104 | 104 | 104 | 104 | 104 |

### Older MBB firmware

| Firmware | Difference |
|---|---|
| rev 6–11 | Log header 115 bytes, no `fw_build_num` |
| rev 7–11 | `0x48` two chargers in one 98-byte entry; currents in mA |
| rev 8–11 | `0x4E` 52 bytes |
| rev ≤ 14 | `0x4C` 71 bytes, `0x4D` 83 bytes |
| rev ≤ 24 | `0x46` byte `0x12` = single eligibility byte |
| rev ≥ 30 | `0x46` byte `0x12` = eligibility bit pair |

## BMU (`75-08274`, `75-08384`)

All BMU types not listed below have the same size in every build: see
[Entry types](bms/index.md#entry-types).

| Type | Name | rev 3<br>486 | rev 4<br>519 | rev 5<br>611 | rev 17<br>bom5 | rev 17<br>bom2 | rev 18<br>bom13 | rev 19<br>bom14 | rev 20<br>bom18 |
|---|---|---|---|---|---|---|---|---|---|
| `0x4B` | `BmsPeriodicSmall` | 37 | 37 | 37 | 39 | 39 | 39 | 39 | 39 |
| `0x4C` | `BmsPeriodicMedium` | 55 | 55 | 55 | 57 | 57 | 57 | 57 | 57 |
| `0x4D` | `BmsPeriodicLarge` | 63 | 63 | 63 | 65 | 65 | 65 | 65 | 65 |
| `0x84` | `BmsCellTooLowForCharge` | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 |
| `0x85` | `BmsCellTooHighForCharge` | 2 | 2 | 2 | 3 | 3 | 3 | 3 | 3 |
| `0x8C` | `BmsIsolationFaultSevere` | — | — | — | 4 | 4 | 4 | 4 | 4 |
| `0x8D` | `BmsIsolationFaultSevereClr` | — | — | — | 4 | 4 | 4 | 4 | 4 |
| `0xFB` | `LogHeaderEntry` | 112 | 112 | 112 | 112 | 112 | 112 | 112 | 112 |

`75-08384` has no rev 3 / 486 build.

### MY19 BMS (`75-08156`)

| Firmware | Difference |
|---|---|
| 2019–20 SR/F (rev 8, 9, 11) | `0x4B`/`0x4C`/`0x4D` 33/49/57 bytes; `0x65`/`0x66` 18 bytes |
| rev 19, 20 | `0xFD` carries the `CapEst` line |

## Package build numbers

`fw_build_num` and `commit_hash` identify the firmware package. All ECU images in one
package share them (e.g. MBB rev 41 and BMU rev 17 in package `bom5`: build 5, commit
`39e9c5ea1`).
