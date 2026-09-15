## 2026-09-15 — Pinned AOT literature homonym-weight signal candidate

- Opened Issue #60 for `SCRIP-MORPH-006` after SCRIP-MORPH-005 merged and no recovery/review-ready work remained.
- Selected the largest mutually exclusive unresolved M005 reason, `direct_cross_bucket_ambiguity` (59,254 frozen Anna Karenina token rows), for an evidence-producing investigation that does not change production POS resolution.
- Pinned-source review established that pylem 0.0.18 exposes `LemmaInfo.predicted`, `word_weight` and `homonym_weight`. At pinned `morph_dict@4c5e9b6d048d1ba74e02988593b23fb0cbc87772`, `CLemmatizer::LoadDictionariesFromPath` implicitly loads `l`-prefixed homonym statistics for literature and enables statistic-backed analysis weights by default. This is provider provenance, not evidence that FantLab used the same weights or dictionary.
- Added `scriptorium-pylem-candidate-metadata-v1` as source-free sidecar metadata aligned one-for-one with the existing ordered runtime POS candidates. Lemmas, token text, morphology-feature sets and predictor source are not retained in uploaded diagnostics.
- Added `scriptorium-pylem-homonym-weight-diagnostic-v1`, which validates the canonical base transport first, hashes the validated candidate-metadata matrix, and measures weight availability, unique-vs-tied maximum bucket signals, all-zero rows, prediction presence and bucket-signature aggregates only for rows already classified as direct cross-bucket ambiguity.
- The diagnostic does not feed a selected bucket into `scriptorium-pos-v1`; FantLab homonym selection and dictionary identity remain unresolved, as do runtime `N`, extra-category folding and service-word aggregation.
- Added focused fail-closed tests for metadata alignment/type drift, same-bucket duplicate handling, frozen-manifest identity and no-source-prose output boundaries.
- Hosted full-work evidence and exact-head review remain required before merge. M2 remains 0/5 source-matched works.
