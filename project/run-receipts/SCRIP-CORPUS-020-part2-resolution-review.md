# Run receipt — SCRIP-CORPUS-020 Part 2 resolution review

- Date: 2026-09-18
- Unit: SCRIP-CORPUS-020
- Issue: #109
- Pull request: #122
- Reviewed exact head: `05df2c43abf2029a98061ca1226d3d81012f3e9f`
- Merge base before review: `957266307475fc4859167bf395739202a5d3df75`
- Merge result: squash commit `cd5bfa3eb2b3534e918d6f1e5ca6d396179086fa`
- Review result: no blocking defect; marked Ready and merged

## Verification

- PR was mergeable and 10 commits ahead / 0 behind the current base immediately before merge.
- No inline review threads or submitted reviews were present.
- All 11 workflows associated with the exact reviewed head completed successfully.
- Dedicated workflow run `35313665511`, job `105500652173`, checked out exact head `05df2c43abf2029a98061ca1226d3d81012f3e9f`.
- The standard-library suite completed 239 tests successfully.
- The replay re-fetched exact pinned source revisions and rebuilt the source-free artifact.
- Byte-for-byte comparison of the regenerated and committed Part 2 resolution artifact succeeded.
- Expanded dependency identity: 585,113 characters / 1,059,957 UTF-8 bytes / SHA-256 `a027dfe0d867572f3802050fcfd72b07a43fa6efe539d58035b3af59f49a04d4`.
- Candidate-specific resolved parent Part 2 reconstruction: 1,166,949 characters / 2,114,262 UTF-8 bytes / SHA-256 `ab45577f567ce504e24936f73fcdff261780168414e4bccc04bbf8927299d016`.
- The expanded dependency has zero remaining `poemx1` calls and zero `{{` / `}}` expansion delimiters.

## Evidence boundary

The merge does not establish historical Russian Wikisource MediaWiki-core or Poem deployment equivalence. The resolved Part 2 identity is a candidate-specific inferred source-graph reconstruction and is not yet a literary-body identity or FantLab analyzer-input identity. The frozen Poem layer represents the bounded post-unstrip reconstruction already recorded by the prerequisite evidence, so later extraction must not promote it to historical parser-byte parity. M2 remains 0/5.

## Continuation

Keep Issue #109 open. Next resolve fail-closed literary extraction for Parts 1–4 and deterministic ordered composition `1 -> 2 -> 3 -> 4`; only then record source-free raw and `scriptorium-text-v1` composite literary-body identities.
