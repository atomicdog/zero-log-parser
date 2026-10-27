# Entry Framing

Every entry, on both ECUs, starts with a 13-byte header.

| Entry offset | Size | Type | Field | Description |
|---|---|---|---|---|
| `0x00` | 1 | `u8` | `sof` | Start of frame, `0xB2` |
| `0x01` | 1 | `u8` | `length` | Entry length on disk, including header and escape bytes. Max 128 |
| `0x02` | 1 | `u8` | `type` | Entry type |
| `0x03` | 4 | `u32` | `timestamp` | Unix time, seconds, UTC |
| `0x07` | 4 | `u32` | `usec` | Microseconds within the second (whole milliseconds). `999999` when the clock was behind the previous entry |
| `0x0B` | 1 | `u8` | `count` | Rolling entry counter, wraps at 256. See [count](#count) |
| `0x0C` | 1 | `s8` | `utc_offset` | UTC offset, whole hours |

Payload: `length − 13` bytes after un-escaping, starting at entry offset `0x0D`.

## Byte stuffing

From the `type` byte to the end of the entry, `0xB2` and `0xFE` are escaped:

| Byte | Written as |
|---|---|
| `0xB2` | `FE 4D` |
| `0xFE` | `FE 01` |

Decoding: on `0xFE`, discard it and take the bitwise complement of the following byte.
`length` counts the escaped (on-disk) size.

## count

- Restarts at 0 on every boot and hibernate wake.
- Advances by 1 per entry, and also without a log write while the ECU is awake. A jump
  between consecutive entries is normal and does not indicate damage.
- The log header (`0xFB`) carries the counter at download time, so it differs between
  downloads of the same log.

## UTC offset

`utc_offset` is the bike's time-correction setting at the time of writing.

```
local_time = timestamp + utc_offset × 3600
```

| Raw | Offset |
|---|---|
| `0xF8` | −8 h |
| `0xF9` | −7 h |
| `0x01` | +1 h |
| `0x02` | +2 h |

## Timestamps

| Condition | Value |
|---|---|
| Logged before RTC sync | Near the Unix epoch |
| Log header entry (`0xFB`) | Download time |
