# 2026-11-07 — SCRIP-REPRO-010 FantLab reference availability (PR candidate)

- Fix a researcher-visible ambiguity in the retained 171-field report: a missing
  FantLab **expected** value is UNKNOWN, whereas an absent Scriptorium
  **actual** is NOT_RUN or UNRESOLVED_NO_ACTUAL. Neither is zero.
- Markdown now counts retained published FantLab references and both-numeric
  diagnostic pairs separately from locally measured metric values, exposing why
  24 local values do not mean 24 public-reference comparisons.
- CSV preserves the existing empty numeric cells and versioned v1 JSON shape;
  additive `reference_availability` / `actual_availability` columns make
  missing-evidence reasons explicit to downstream consumers.
- Add tests for two-reference books, reference-unavailable measured fields,
  unmeasured actuals and a synthetic measured numeric zero. Update CLI docs,
  README and the single canonical queue.
- No text reprocessing, new corpus admission, new source identity, rounding
  inference, compatibility status promotion or Pages deployment. M2 stays 0/5.
- Require later independent exact-head CI/review before merge.
