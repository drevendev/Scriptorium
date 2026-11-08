# 2026-11-08 — Contextual metric definition links (PR candidate)

- Root Reader interactive single-book rows, paired rows and selected chart heading link to the exact Russian definition in the already-merged 29-metric glossary. URLs encode IDs; DOM text nodes and descriptive accessible names avoid HTML interpolation.
- Both source-backed, no-JavaScript tables retain exact observations and offer direct access to the full glossary; no data, source text, exported metrics or scientific gates change.
- Focused Node regression covers all 29 targets and a malicious-looking ID; Python structural regression and Pages CI step cover integration. Hosted CI/merge/live browser acceptance remain separate.
- Reconcile merged #468 in the compact queue; #283 remains open until actual browser/mobile/print acceptance. M2 remains 0/5.
