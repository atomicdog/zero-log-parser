# Zero Gen3 Log Format

Binary event-log format written by the Gen3 (FST platform) Main Bike Board (MBB) and
Battery Management Unit (BMU/BMS), as downloaded through the Zero app.

| ECU | Log file | Entry types |
|---|---|---|
| MBB | 131,200 bytes | `0x46`–`0x54`, `0xFB`, `0xFD` |
| BMS | 131,328 bytes | `0x4B`–`0x8D`, `0xFB`, `0xFD` |

The MBB and BMS use separate type-code spaces. Several codes (`0x4B`–`0x54`) exist in
both with unrelated layouts; select the table by the file's ECU.

## Conventions

| Item | Convention |
|---|---|
| Byte order | Little-endian |
| Offsets | Hexadecimal, relative to the start of the payload (after the 13-byte entry header) unless stated otherwise. All offsets apply after un-escaping. |
| Sizes | Decimal bytes |
| zero-log-parser | Its Gen3 code starts the payload at `usec`: its offset = this offset + 6, and its payload sizes are these plus 6 (`0x51` 58 / 62 here is 64 / 68 there). Tag-relative offsets are the same. |
| `u8` `u16` `u32` `u64` | Unsigned integers |
| `s8` `s16` `s32` | Signed (two's complement) integers |
| `u24` | 3-byte unsigned integer |
| `char[n]` | Fixed-width ASCII, NUL-padded |
| `bytes[n]` | Fixed-width raw bytes |
| `—` | Field not present in that variant |

## Contents

- [File format](file-format.md): file sizes, block layout, BMS download stamp
- [Entry framing](framing.md): 13-byte entry header and byte stuffing
- [MBB](mbb/index.md): header and entry types
- [BMS](bms/index.md): header and entry types
- [Firmware versions](firmware.md): payload sizes by firmware revision
