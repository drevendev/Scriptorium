# SCRIP-CORPUS-020 — literary-body extractor recovery review

Date: 2026-09-18
Issue: #109
Reviewed PR: #126
Superseded duplicate: #125

- Re-oriented from `AGENTS.md`, the project manifest/state/queue and current open forge state before judging the interrupted work.
- Found two divergent Draft implementations from the same master baseline. PR #125 exact head `0da222f824b98f1526cd8702469bab669051c376` still failed its live four-part replay (`35343329777`, job `105594047552`) after the standard-library tests, while PR #126 exact head `d589a9070b1a830c67b8800ddc9f7abf2d876a4c` was mergeable-clean, 12 commits ahead / 0 behind, with no prior reviews or inline review threads and no failing exact-head checks.
- Independently reviewed the #126 candidate-specific boundary: all thirteen already-frozen plain `poemx1` values are identity-checked before substitution; the Part 2 dependency applies bounded partial-transclusion controls before rendering; actual table delimiters remain fail-closed; literal authorial angle/`nowiki` text is preserved instead of being treated as generic HTML; composition is explicitly Parts `1 -> 2 -> 3 -> 4` joined by `\n\n`.
- Exact-head dedicated run `35340846781`, job `105586149163`, checked out `d589a9070b1a830c67b8800ddc9f7abf2d876a4c`, passed the full standard-library suite, re-fetched the five pinned source revisions, derived the four-part literary body successfully and uploaded only source-free evidence.
- Closed broken duplicate PR #125 as superseded, submitted the recovery review on #126, marked #126 Ready, and squash-merged it as `211540828eae37d65e9f2ea994a592295d54b4b3`.
- The generated literary-body identities remain deliberately uncommitted in this review unit. Issue #109 stays open for independent source-free manifest capture/provenance and later comparison. Historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input identity remain unproven; M2 stays 0/5.
