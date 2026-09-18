# SCRIP-CORPUS-020 — body extraction surface review

- Independently reviewed exact PR #123 head `fb5e787027e9b156594bb217845652452d945017` after the authored run.
- Confirmed the PR was mergeable, 9 commits ahead / 0 behind current master, with no blocking review threads and all 12 exact-head pull-request workflows successful.
- Confirmed dedicated replay run `35317967589` / job `105513730940` checked out the exact head and completed source replay, full standard-library tests, source-free regeneration and byte comparison.
- Preserved the claim boundary: the merged structural surface proves that seven direct parent `poemx1` calls remain extraction inputs (5 / 2 / 0 / 0 across Parts 1–4), including two Part 2 calls outside the target-only `#lst` span; it does not freeze any literary-body or composite identity and does not prove historical MediaWiki/Poem deployment equivalence.
- Marked PR #123 Ready and squash-merged it as `c5b527f3390ae6aec5cfc3716d67da6af8311aa4`.
- Issue #109 remains open; the next P0 is fail-closed per-part literary extraction against the frozen surface followed by deterministic `1 -> 2 -> 3 -> 4` composition. M2 remains 0/5.
