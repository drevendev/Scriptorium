"""Minimal spreadsheet-formula neutralization for source-free CSV text fields.

RFC 4180 quoting prevents column breakout but not formula execution. Prefix risky
*text* cells with an apostrophe; numeric cells are validated by their callers.
The apostrophe intentionally changes the spreadsheet-facing string. This is a
best-effort CSV defense, not a promise about Excel's save/reopen behavior.
"""
from __future__ import annotations

import unicodedata

# Full-width formula operators may be interpreted in some spreadsheet locales.
_FORMULA_PREFIX = frozenset("=+-@＝＋－＠")
_CONTROL_PREFIX = frozenset("\t\r\n\x00")


def safe_csv_text(value: str) -> str:
    """Escape formula-like text, including formulas hidden behind format marks.

    Keep the original label unchanged after the leading apostrophe, so provenance
    can be reconstructed without silently stripping meaningful characters.
    """
    if not value:
        return value
    if value[0] in _CONTROL_PREFIX:
        return "'" + value
    # Spreadsheet importers may ignore leading Unicode whitespace / formatting
    # chars such as BOM (U+FEFF), zero-width space (U+200B) and word joiner.
    first = next((char for char in value if not (char.isspace() or unicodedata.category(char) == "Cf")), "")
    if first in _FORMULA_PREFIX:
        return "'" + value
    return value
