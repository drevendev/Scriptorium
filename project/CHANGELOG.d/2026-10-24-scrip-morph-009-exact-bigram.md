# 2026-10-24 — N-only bigram envelopes become exact per cell (authored)

- Version source-free `scriptorium-pylem-n-only-impact-v2`: replace loose
  independent-edge maxima with per-sentence dynamic-programming maxima,
  preserving one noun/cardinal assignment per N-only token across adjacent edges.
- Retain v1-style independent-edge bounds in a separately named diagnostic field.
  Repeated N-only triples demonstrate why the earlier upper bound could overstate
  an **individually attainable** transition maximum.
- Exhaustive short-sequence and sentence-boundary regressions added; the existing
  native Python 3.9 pylem replay now asserts v2. Actual native results and full
  exact-head CI are NOT_RUN at authoring.
- These are conditional, source-unmatched bounds, not token-level POS recovery.
  Mixed N remains excluded; profiles, source texts, dictionaries and M2 0/5
  are unchanged. Later-run acceptance is required before merge.
