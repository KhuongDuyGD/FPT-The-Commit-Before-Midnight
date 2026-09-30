"""Check the bundled fonts' cmap tables without installing font libraries."""
from pathlib import Path
import argparse
import json
import struct

ROOT = Path(__file__).resolve().parents[1]


def covered_characters(path, characters):
    data = path.read_bytes()
    u16 = lambda offset: struct.unpack_from(">H", data, offset)[0]
    u32 = lambda offset: struct.unpack_from(">I", data, offset)[0]
    table_count = u16(4)
    cmap = next(u32(12 + i * 16 + 8) for i in range(table_count)
                if data[12 + i * 16:16 + i * 16] == b"cmap")
    covered = set()
    for i in range(u16(cmap + 2)):
        table = cmap + u32(cmap + 4 + i * 8 + 4)
        fmt = u16(table)
        if fmt == 12:
            for j in range(u32(table + 12)):
                start, end, first = struct.unpack_from(">III", data, table + 16 + j * 12)
                covered.update(cp for cp in characters if start <= cp <= end and first + cp - start != 0)
        elif fmt == 4:
            segments = u16(table + 6) // 2
            end_at = table + 14
            start_at = end_at + 2 * segments + 2
            delta_at = start_at + 2 * segments
            range_at = delta_at + 2 * segments
            for j in range(segments):
                start, end, delta = u16(start_at + 2 * j), u16(end_at + 2 * j), u16(delta_at + 2 * j)
                offset = u16(range_at + 2 * j)
                for cp in characters:
                    if not start <= cp <= end:
                        continue
                    glyph = u16(range_at + 2 * j + offset + 2 * (cp - start)) if offset else cp
                    if glyph and (glyph + delta) & 0xffff:
                        covered.add(cp)
    return covered


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sdk", type=Path)
    args = parser.parse_args()
    source = (ROOT.parent / "FPT_The_Commit_Before_Midnight_MASTER_REBUILD_PROMPT.md").read_text(encoding="utf-8")
    required = {ord(ch) for ch in source if not ch.isspace()}
    fonts = args.sdk / "renpy/common"
    regular = covered_characters(fonts / "DejaVuSans.ttf", required)
    emoji = covered_characters(fonts / "TwemojiCOLRv0.ttf", required)
    # Match FontGroup's actual ordering/ranges.
    covered = (regular - set(range(0x1f000, 0x20000))) | (emoji & set(range(0x1f000, 0x20000)))
    missing = sorted(required - covered)
    report = dict(required_codepoints=len(required), missing=[chr(cp) for cp in missing], fonts=["DejaVuSans.ttf", "TwemojiCOLRv0.ttf"])
    (ROOT / "tests/rebuild/font-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    assert not missing, "Some source characters cannot be rendered"
