# Private comparison — disjoint punctuation-event budget (2026-11-08)

- `scriptorium compare` now refuses imported JSON reports claiming more word-token and punctuation events than the declared normalized-character body can physically contain, even when each punctuation row has a valid raw count and a recomputed per-1,000-word rate.
- Positive dense-text, compound-punctuation, punctuation-only and empty-input cases remain valid; fabricated single-/multi-row totals are regression tested against the actual analyzer output.
- The check is a necessary internal consistency condition, not source-hash authentication, a FantLab word-boundary rule, or evidence of M2 parity. Core 29 inferred/extension metrics, pinned corpus measurements, data/rights and Pages are unchanged.
