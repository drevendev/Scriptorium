# 2026-11-08 — Bound imported UASZ windows by active vocabulary

- The imported private comparison validator now rejects a rolling-window distinct-dictionary-word average greater than the document's measured active dictionary vocabulary, even when that average is below the supplied external dictionary's lexeme count.
- A genuine 3,000-word, two-lexeme report remains valid; forged global dictionary/nondictionary partitions now fail comparison. No profiles, raw texts, corpus entries, published numeric results or FantLab tolerance rules change.
- The already-merged #464 punctuation-budget improvement is reconciled into the single canonical queue. Hosted exact-head CI and later independent PR acceptance are separate; M2 remains 0/5.
