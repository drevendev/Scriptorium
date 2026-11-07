# 2026-11-07 — Reference input binding for benchmark integer outcomes

- Harden the existing Python FantLab benchmark: `--edition-match exact` and other caller-supplied labels no longer suffice for integer PASS/FAIL. An independently captured reference-side `source_text.edition_matched=true` and exact `raw_sha256` matching the supplied bytes are also required.
- Missing reference-side binding keeps numeric results diagnostic/UNRESOLVED; malformed, incomplete or contradictory exact-input claims fail before literary-text analysis.
- This is a consistency check, not proof of the reference witness's authenticity or FantLab input identity. Existing `work488` stays unmatched and M2 remains 0/5. No corpus/text/rounding, JSON v1 or Pages changes.
- Tests cover a synthetic positive witness, source-matched integer mismatch, unbound exact assertions and multiple forged witnesses. Later exact-head CI and independent PR acceptance required.
