# SCRIP-CORPUS-020 — Part 2 resolution review

Date: 2026-09-18
Issue: #109
Pull request: #122
Reviewed head: `05df2c43abf2029a98061ca1226d3d81012f3e9f`
Merged commit: `cd5bfa3eb2b3534e918d6f1e5ca6d396179086fa`

An independent later-run review found no blocking defect in the candidate-specific target-only Part 2 resolver. Before merge, PR #122 was mergeable, 10 commits ahead and 0 behind its current base, with no inline review threads or submitted reviews. All 11 exact-head workflows completed successfully. Dedicated replay run `35313665511` checked out the exact reviewed head, ran all 239 standard-library tests, re-fetched the pinned parent (`oldid=5198033`), target dependency (`oldid=2366546`) and inferred `Шаблон:Poemx1` anchor (`oldid=5142743`), regenerated the source-free Part 2 resolution, and byte-compared it with the committed artifact.

The merged artifact freezes the expanded target dependency at 585,113 characters / 1,059,957 UTF-8 bytes, SHA-256 `a027dfe0d867572f3802050fcfd72b07a43fa6efe539d58035b3af59f49a04d4`, and the candidate-specific resolved parent Part 2 reconstruction at 1,166,949 characters / 2,114,262 UTF-8 bytes, SHA-256 `ab45577f567ce504e24936f73fcdff261780168414e4bccc04bbf8927299d016`.

The review preserves the evidence boundary: these identities are candidate-specific inferred source-graph reconstruction, not proof of the exact historical Russian Wikisource MediaWiki-core or Poem deployment and not a literary-body identity. The Poem reconstruction uses the previously frozen post-unstrip fragment identities; future literary extraction must continue to treat that surface as an inferred reconstruction rather than historical parser-byte parity. FantLab source identity remains unknown and M2 remains 0/5.

PR #122 was marked Ready and squash-merged. The next P0 unit is fail-closed per-part literary-body extraction followed by deterministic `1 -> 2 -> 3 -> 4` composition before any raw or `scriptorium-text-v1` composite literary-body digest is recorded.
