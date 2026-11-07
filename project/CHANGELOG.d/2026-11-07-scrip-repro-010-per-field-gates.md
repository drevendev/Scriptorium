# 2026-11-07 — SCRIP-REPRO-010 per-field evidence gates (PR candidate)

- Add deterministic source/rounding/reference/local/extension blocker codes in
  the retained 171-field CSV and Markdown report, making missing evidence
  inspectable per metric without inventing source matching or PASS statuses.
- Reject synthetic promotion of source identity, display rounding or comparison
  results, and inconsistent expected/actual/delta availability.
- Preserve JSON v1, prior numeric CSV fields, pinned inputs and source privacy.
  Add real-coverage and negative regressions; update docs, README and queue.
- Does not rerun literary analysis, establish FantLab identity or advance M2 (0/5).
- Independent exact-head CI/review required before merge.
