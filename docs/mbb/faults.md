# MBB Faults

## 0x4F -- queue_send_fail

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 10 | `char[10]` | `queue_name` | Queue name |
| `0x0A` | 4 | `u32` | `msgs_waiting` | Messages waiting in the queue |
| `0x0E` | 4 | `u32` | `send_fail_count` | Failed sends, all queues, since power-on |

### Queue names

| Queue | Typical `msgs_waiting` |
|---|---|
| `CAN0RxQ` | 48 |
| `CAN1RxQ` | 64 |
| `CAN1txQ` | 32, 64 |
| `CAN2RxQ` | 32 |
| `CAN2txQ` | 16 |
| `dashQ` | 6 |
| `logQ` | 8 |
| `pduQ` | 5 |
| `uartrxQ` | 128 |
| `uarttxQ` | 958, 991 |

## 0x50 -- mcu_fault

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `fault_type` | Fault type. 1 = hard, 2 = bus, 4 = usage |
| `0x01` | 4 | `u32` | `fault_data_0` | HFSR |
| `0x05` | 4 | `u32` | `fault_data_1` | CFSR |
| `0x09` | 4 | `u32` | `fault_data_2` | BFAR |
| `0x0D` | 4 | `u32` | `fault_data_3` | Exception stack pointer |
| `0x11` | 4 | `u32` | `fault_data_4` | LR |
| `0x15` | 4 | `u32` | `fault_data_5` | PC |

See [CFSR bits](../bms/diagnostics.md#cfsr-bits).
