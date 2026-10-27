# File Format

## Identification

| File size | First bytes¹ | `00 F0 FF 00` at each 128-byte block start | Content |
|---|---|---|---|
| 131,200 (1025 × 128) | `B2 75 FB` | No | MBB log |
| 131,200 (1025 × 128) | `B2 73 FB` | No | MBB log, firmware rev 6–11 header |
| 16,384 (128 × 128) | `B2 75 FB` | No | MBB log, smaller download window |
| 131,328 (1026 × 128) | `B2 7D FB` | Yes (blocks 1–1025) | BMS log |
| 131,200 (1025 × 128) | BMS header | No | BMS log, 2019–20 SR/F |

¹ After un-escaping. If the header entry contains an escape, the raw length byte is one
higher (`B2 76 FB`, `B2 7E FB`, …) and all later header bytes are shifted. Un-escape the
header entry before reading it.

Files are always a whole number of 128-byte blocks; a size that is not a multiple of 128
is not this format. Partial downloads have other sizes. The file content, not its name or
size, identifies the ECU.

## Block layout

| Block | MBB | BMS |
|---|---|---|
| 0 | Log header entry (`0xFB`), zero-padded to 128 bytes | Log header entry (`0xFB`), zero-padded to 128 bytes |
| 1–1024 | Most recent `0x20000` bytes of the log ring buffer | Most recent `0x20000` bytes of the log ring buffer, with download stamp |
| 1025 | — | Pad block (complete downloads only) |

The log header entry is generated at download time. It is not stored in the log.

### Ring buffer

| Parameter | MBB | BMS |
|---|---|---|
| Flash region | `0x001000`–`0xE80000` | `0x001000`–`0x1000000` |
| Erased byte | `0xFF` | `0xFF` |

- Erased bytes (`0xFF`) mark the write pointer.
- After a wrap, the data following the erased region is older than the data before it.
  File order is not time order; sort entries by timestamp.
- The entry at the write pointer may be truncated.
- Bytes between the end of one entry and the next `0xB2` are not part of any entry.

### BMS download stamp

In BMS files, bytes 0–3 of every block from block 1 onward read `00 F0 FF 00`. The
original 4 log bytes at those positions are lost.

| Entry position relative to stamp | Appearance |
|---|---|
| Starts at block byte 127 | `B2 00 F0 …` (length 0) |
| Starts at block byte 126 | Type `0x00`; timestamp low 3 bytes `F0 FF 00` |
| Starts at block bytes 0–3 | No `B2`/length; not framed |
| Spans a block start | Framing intact; 4 payload or header bytes replaced |
| Stamp covers an `0xFE` escape | Rest of the entry decodes 1 byte out of alignment |

### BMS pad block

| Offset | Size | Content |
|---|---|---|
| `0x00` | 4 | `00 F0 FF 00` |
| `0x04` | 124 | `00` |

Present as the last block of a complete BMS download. Identify it by content, not by file
size: a partial download ends on a block of real data. The final log entry may run into
the pad block; its tail bytes are then not log data.

### Repeated blocks

A download may contain the same 128-byte block more than once in succession. Adjacent
identical non-erased blocks are duplicates; discard all but the first.
