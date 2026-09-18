# SCRIP-CORPUS-020 — canonical Klim Samgin literary-body identity capture

Date: 2026-09-18
Issue: #109
Draft PR: #127

- Recovered the source-free manifest emitted by the independently reviewed exact-head replay for PR #126 (`35340846781`, job `105586149163`, artifact `10545296253`).
- Verified the downloaded artifact ZIP digest as `717177464f00e51915cd65d661cb428d22210bb1f7b5055c4a813f0777ae6193` and the contained canonical manifest file SHA-256 as `8057605ce3d8f547c7091647f5315662b1d8d9c04b94b7b16f7fbacf80b7499f` before committing it.
- Captured source-free per-part literary-body identities: Part 1 `964,215` chars / `1,744,650` bytes / SHA-256 `1a41cef4...`; Part 2 `1,164,870` / `2,111,745` / `75896b6a...`; Part 3 `680,940` / `1,234,441` / `7dc60303...`; Part 4 `1,000,587` / `1,868,088` / `237b2119...`.
- Captured ordered composition `1 -> 2 -> 3 -> 4` with separator `\n\n` and composite identity `3,810,618` chars / `6,958,930` bytes, raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`.
- Added a regression that validates the committed manifest remains source-free, inferred-only, FantLab-source-unknown, gate-closed, and raw/normalized digest-consistent.
- Historical Russian Wikisource MediaWiki-core/Poem deployment equivalence remains unproven; FantLab analyzer-input identity remains unknown. M2 remains 0/5.
- Draft PR #127 is intentionally left for independent later-run review; its exact-head dedicated workflow must regenerate and byte-compare the committed manifest before merge.
