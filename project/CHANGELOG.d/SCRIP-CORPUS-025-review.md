# SCRIP-CORPUS-025 — independent review and merge

Date: 2026-09-19
Issue: #137
PR: #138

- Independently reviewed exact PR head `48a8dcb96f35fe20b790fb02674885220f5df868` in a later wake; the branch was mergeable, 8 commits ahead / 0 behind `master`, with no inline review threads.
- All 13 pull-request workflow runs associated with that exact head completed successfully.
- Candidate-specific run `35419930230`, job `105835545747`, checked out the exact head, ran 267 standard-library tests, re-fetched exact Russian Wikisource revision `5304880`, byte-compared the observed source-free manifest with the committed manifest, replayed it successfully, and verified the fail-closed capture scope.
- The same run uploaded only two source-free JSON evidence files in artifact `10577845809`; artifact ZIP SHA-256 `8c49584dbf41868f2d2861543e4d0b1e08603d1f4cc83f8f0052230e26aa19d6`.
- Public and structured provenance continue to separate frozen revision-wikitext identity from unfrozen literary-body extraction and >=300k corpus admission. FantLab source match remains unknown and M2 remains 0/5.
- Marked PR #138 Ready and squash-merged it as `c38aebb0a560be1a4e2713043aff407241d710b9`; Issue #137 closed automatically as completed.
