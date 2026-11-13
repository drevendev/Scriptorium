# 2026-11-13 — Trusov seam sensitivity baseline integrity (PR candidate)

- Fix a concrete evidence error in the existing 145-Page **incomplete** Trusov sensitivity experiment: retained one-LF text hashes were checked, but tampered 29-row baseline values could still become false signed deltas.
- Recompute the exact one-LF baseline metrics from the same transient, source-verified Page text before accepting values, unavailable/null statuses, units, compatibility labels, metric profiles and numeric counts. Refuse mismatches rather than propagate a fabricated result.
- Add negative regression cases for a modified character count, dictionary-unbound NULL changed to zero, a forged unit and an inconsistent aggregate; retain the existing positive deterministic replay test. No second network fetch and no source text stored.
- This checks **internal diagnostic consistency**, not provenance authenticity, historical rendering or full body coverage. Existing measured-edition count is 11; incomplete Pages 3–147 and M2 0/5 are unchanged.
