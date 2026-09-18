# SCRIP-CORPUS-020 — candidate-specific four-part literary-body extractor

Date: 2026-09-18
Issue: #109
Draft PR: #126

- Added a fail-closed Klim Samgin literary-body reconstruction path that replays all four pinned parent revisions and the pinned Part 2 target dependency without persisting source prose.
- Revalidates and substitutes all thirteen already-frozen plain `poemx1` parameter-2 values: seven direct-parent calls plus six calls inside the Part 2 dependency.
- Applies the existing bounded MediaWiki partial-transclusion semantics to the Part 2 dependency after exact poem-value substitution. The live pinned dependency contains one `noinclude` pair and one `includeonly` pair; no `onlyinclude` controls are reached.
- Removes only the frozen Wikisource scaffolding (`Жизнь Клима Самгина`, `примечания`, categories and the presentation-only `Ко` wrapper), preserves the observed literary headings and literal `nowiki` content, strips editor-note refs, and fails closed on unmodelled template/tag/table/wiki markup.
- Freezes the composition rule in code as Parts `1 -> 2 -> 3 -> 4` joined by exactly two LF characters, but deliberately does not commit the generated source-free body-identity manifest in this authoring run. Independent later-run review must decide whether to capture it.
- Exact-head live replay at `86abd1483ac3f1d2ff1c5dac89715c6ef6b3a798` ran 254 tests, re-fetched the exact source graph, and successfully generated/uploaded source-free candidate evidence in run `35340711309` / job `105585727013` / artifact `10544478043`.
- The observed diagnostic-only composite is 3,810,618 characters / 6,958,930 UTF-8 bytes with raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`; these identities remain uncommitted pending independent review.
- Historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input identity remain unproven. M2 remains 0/5.
