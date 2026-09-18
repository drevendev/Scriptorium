# Run receipt — SCRIP-CORPUS-020 literary-body extractor recovery review

Date: 2026-09-18
Issue: #109
Reviewed PR: #126
Merged head: `d589a9070b1a830c67b8800ddc9f7abf2d876a4c`
Squash merge: `211540828eae37d65e9f2ea994a592295d54b4b3`
Superseded duplicate: #125

## Selected bounded unit

Recover the interrupted duplicate-PR state before taking new queue work, independently judge the healthy literary-body extractor implementation, retire the broken duplicate, and reconcile the canonical project state without capturing new literary-body identities in the same review unit.

## Recovery findings

- PR #125 (`scrip-corpus-020-klim-literary-body`) and PR #126 (`scrip-corpus-020-literary-body-extractor`) diverged from master `99b4016f8e53c06bf694bc1e6c282560c01b056e`.
- #125 exact head `0da222f824b98f1526cd8702469bab669051c376` remained red: its dedicated run `35343329777` / job `105594047552` passed the standard-library suite but failed while re-fetching the exact source graph and freezing the literary composite. A temporary repair workflow was also red.
- #126 exact head `d589a9070b1a830c67b8800ddc9f7abf2d876a4c` was mergeable-clean, 12 commits ahead / 0 behind master, with six changed files, no prior submitted reviews and no inline review comments.
- The #126 exact-head check set contained no failures. Dedicated run `35340846781` / job `105586149163` checked out the exact reviewed SHA, passed the full standard-library test suite, re-fetched all five pinned revisions, derived the four-part body successfully and uploaded the generated source-free evidence.

## Independent judgement

No blocking defect was found in #126. The reviewed implementation is intentionally candidate-specific and fail-closed: it revalidates the frozen source/`poemx1` identities, applies bounded Part 2 partial-transclusion semantics, rejects remaining unsupported active markup, preserves observed literal authorial angle/`nowiki` text, and fixes composition to Parts `1 -> 2 -> 3 -> 4` with `\n\n` separators. It does not commit the generated body manifest or promote FantLab/source-equivalence claims.

The broken duplicate #125 was commented and closed as superseded. A review comment anchored to #126 exact head was submitted, #126 was marked Ready, then squash-merged with expected-head protection as `211540828eae37d65e9f2ea994a592295d54b4b3`.

## Gate / continuation

The source-free body identities observed during the authoring replay remain diagnostic and uncommitted by design. Issue #109 remains open. The next P0 unit is independent capture/replay of the canonical source-free four-part literary-body manifest and corresponding public provenance, followed only later by FantLab field-by-field comparison. Historical Russian Wikisource MediaWiki-core/Poem deployment equivalence and FantLab analyzer-input identity remain unresolved. M2 remains 0/5.
