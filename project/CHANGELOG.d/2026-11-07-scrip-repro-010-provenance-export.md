# 2026-11-07 — SCRIP-REPRO-010 source-bound export (PR candidate)

- Join all five existing frozen readiness witnesses into the retained-metric
  JSON, Markdown and CSV report without changing the 171 diagnostic field rows.
  Expose rights, edition/translator, frozen body length, source/normalized SHA-256,
  trace and dated reference alongside exact expected/actual/delta.
- Keep supplemental Resurrection separately scoped, with missing five-work
  provenance explicitly UNKNOWN/NOT_RUN instead of borrowing a core edition.
- Add source-free deterministic regression and spreadsheet-formula safety tests.
  No FantLab input identities, rounding rules or scientific M2 gates change.
- Authored feature requires later fresh exact-head acceptance; branch CI is not
  proof of live Pages publication.
