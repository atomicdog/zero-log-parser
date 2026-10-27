# MBB Events

## 0x4E -- firmware_updated

Logged at the first boot of a new firmware image.

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `u16` | `prev_fw_rev` | Previous firmware revision |
| `0x02` | 2 | `u16` | `fw_rev` | Firmware revision of the running image |
| `0x04` | 32 | `char[32]` | `prev_fw_state` | Previous firmware state. Default `UNINITIALIZED` |
| `0x24` | 2 | `u16` | `fw_build` | Build/package number of the running image |
| `0x26` | 6 | `char[6]` | `bank_name` | Flash bank: `banka` or `bankb` |
| `0x2C` | 10 | `char[10]` | `commit_hash` | Git commit hash of the running image |

Firmware rev 8–11 (52 bytes):

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 2 | `u16` | `prev_fw_rev` | Previous firmware revision |
| `0x02` | 2 | `u16` | `fw_rev` | Firmware revision of the running image |
| `0x04` | 32 | `char[32]` | `prev_fw_state` | Previous firmware state (image compile timestamp) |
| `0x24` | 10 | `char[10]` | `commit_hash` | Git commit hash, first 5 characters |
| `0x2E` | 6 | `char[6]` | `bank_name` | Flash bank |

## 0xFB -- log_header

See [Log header](index.md#log-header-0xfb).

## 0xFD -- debug_message

| Offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | ≤ 115 | `bytes` | `message` | ASCII text, NUL-terminated |

- Maximum 114 characters + NUL.
- Truncated messages end in `$`.
- Some entries contain non-ASCII bytes.
