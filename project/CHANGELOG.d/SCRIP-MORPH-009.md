# SCRIP-MORPH-009 — Native N-only POS sensitivity

- A new source-free, pinned-provider and frozen-source-bound conditional measurement
  quantifies noun/cardinal, bigram and sentence-position cell exposure for N-only
  rows; mixed N and other unresolved rows are not reclassified.
- Adds positive/negative regressions and a Python 3.9 pinned-native replay
  with a source-free artifact. No new source-text publication.
- Per-cell maxima may not be jointly achievable. Neither noun/cardinal labels
  nor FantLab parity/dictionary identity have been recovered. M2 stays 0/5.
- At authoring exact-head native CI and later-run review are pending.

## 2026-10-25 — Exact bigram minima (v3; authored)

- Fix conditional lower bounds that previously counted only fixed-fixed edges:
  a fixed noun, N-only, fixed cardinal sequence forces a noun-to-cardinal edge.
- Keep prior fixed-only lower and independent-edge upper bounds as separate data;
  verify minimum and maximum against exhaustive short assignments and native CI.
- Native tags, text hashes, production POS mapping, unresolved categories and M2 0/5
  remain unchanged. This does not recover true noun/cardinal labels.
