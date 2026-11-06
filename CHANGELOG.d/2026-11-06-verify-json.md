# 2026-11-06 — Machine-readable local verification

- Add `scriptorium verify ... --json`: emit one deterministic source-free PASS
  record only after the full 29-metric, profile and source-hash replay succeeds.
- Distinguish EPUB archive receipt verification (`VERIFIED`) from a report replay
  without a receipt (`NOT_CHECKED`) and plain UTF-8 (`NOT_APPLICABLE`).
- Leave errors nonzero on stderr, without a success JSON record. Reject source
  content/path disclosure in positive and tampered-input regressions.
- This is current-engine replay evidence, **not** an authenticated revision,
  edition identity, legal grant or FantLab parity. M2 remains 0/5.
