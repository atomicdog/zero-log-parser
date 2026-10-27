"""Layout tables for the Gen3 datasheet.

Each layout is a list of fields; offsets are computed from sizes, so a table
can never disagree with itself. `only` restricts a field to some variants.
"""
import re

SIZES = {'u8': 1, 's8': 1, 'u16': 2, 's16': 2, 'u24': 3, 'u32': 4, 's32': 4, 'u64': 8}


def size_of(t):
    if t in SIZES:
        return SIZES[t]
    m = re.fullmatch(r'(?:char|u8|u16|bytes)\[(\d+)\]', t)
    if not m:
        raise ValueError(t)
    n = int(m.group(1))
    return n * 2 if t.startswith('u16') else n


def F(name, typ, desc='', only=None):
    return dict(name=name, type=typ, desc=desc, only=only)


def table(fields, variants=None):
    """variants: list of (label, expected_total). Returns markdown."""
    variants = variants or [(None, None)]
    offs = {v: 0 for v, _ in variants}
    rows = []
    for f in fields:
        sz = size_of(f['type'])
        cells = []
        for v, _ in variants:
            if f['only'] is None or v in f['only']:
                cells.append(f'`0x{offs[v]:02X}`')
                offs[v] += sz
            else:
                cells.append('—')
        rows.append(cells + [str(sz), f"`{f['type']}`", f"`{f['name']}`", f['desc']])
    for v, total in variants:
        if total is not None and offs[v] != total:
            raise AssertionError(f'{v}: computed {offs[v]}, expected {total}: {[f["name"] for f in fields]}')
    if len(variants) == 1:
        head = ['Offset']
    else:
        head = [f'Offset<br>{v}' for v, _ in variants]
    head += ['Size', 'Type', 'Field', 'Description']
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    out += ['| ' + ' | '.join(r) + ' |' for r in rows]
    return '\n'.join(out)


def bits(rows, mask_width=None):
    """rows: (bit, meaning). Renders bit / mask / meaning."""
    w = mask_width or max(2, (max(b for b, _ in rows) // 4) + 1)
    out = ['| Bit | Mask | Meaning |', '|---|---|---|']
    for b, m in rows:
        out.append(f'| {b} | `0x{1 << b:0{w}X}` | {m} |')
    return '\n'.join(out)


def values(rows, head=('Value', 'Meaning')):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
    out += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)
