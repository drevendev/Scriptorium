# 2026-10-23 — Private EPUB Reader candidate (#289)

- Added a bounded, local-only EPUB 2/3 XHTML-spine importer wired into the installed Reader CLI, preserving the canonical 29-metric JSON/HTML/CSV and private comparator.
- Recorded separate SHA-256 identities for the original EPUB archive, extracted UTF-8 literary body, and normalized analyzer text; the extraction profile is versioned and derived receipts omit prose.
- Rejected encrypted/unsafe/malformed archives, duplicate or aliased ZIP members, traversal and remote spine targets, XML DTD/entities, missing spine references and oversized/decompression-bomb inputs.
- Added original synthetic EPUB reading-order, Unicode, identity, security and no-overwrite regressions plus installed-wheel smoke for EPUB -> Reader -> compare.
- Scientific corpus/parity gates, compatibility claims, rights and Pages activation are unchanged; M2 remains 0/5. This PR needs later independent exact-head acceptance.
