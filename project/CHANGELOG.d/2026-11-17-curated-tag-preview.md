# 2026-11-17 — curated tags, source-free private profile preview (#563)

- Added a versioned, explicitly supplied taxonomy/rights/annotation catalog and offline `scriptorium tags` command over existing measured-edition JSON. No source text or word-form data is loaded or published.
- Fail-closed checks bind edition, translator, work ID, full-length measured count, source SHA-256, metric profile, rights evidence, tag authority and certainty. Duplicate body/work claims and mixed profiles are refused.
- For explicitly confirmed annotations only, emit reproducible per-tag counts and observed mean, between-work dispersion, min/max and missingness with explicit units and null for unknown/single/zero samples.
- Outputs unconditionally state `public_release_ready=false` and `rights_independently_verified=false`: the CLI does not independently authenticate curator assertions or permit a tag profile onto Pages.
- Added 11 direct positive/negative local regression tests and methodology. No new public tags or corpus admissions; M2 remains 0/5. Await exact-head hosted checks and later-run acceptance.
