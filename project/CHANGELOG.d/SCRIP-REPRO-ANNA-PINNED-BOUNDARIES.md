# SCRIP-REPRO-ANNA-PINNED-BOUNDARIES — complete candidate replay (2026-11-07)

- Extend the existing pinned 239-revision Anna Karenina CI diagnostic with optional seven-variant `word_boundary_sensitivity`, reusing its **single** source replay instead of fetching the same public-domain pages twice.
- Fail closed if the normalized identity/character length differs from the frozen manifest or the baseline/decimal-only/Unicode-hyphen counts diverge from current policy; hosted CI also compares those three against the older frozen policy receipt.
- Add opt-in/default, positive one-factor, provenance-mismatch and negative baseline-drift regressions; CI retains only derived counts, source digest and evidence labels. No book prose, paths or unsupported FantLab conclusions enter the artifact.
- **Full-work values NOT_RUN until hosted exact-head CI succeeds**. Previous pinned Anna input matches neither a demonstrated FantLab edition nor a published analyzer-input digest; this is DIAGNOSTIC_ONLY and M2 stays **0/5**. Reader/Pages unchanged.
