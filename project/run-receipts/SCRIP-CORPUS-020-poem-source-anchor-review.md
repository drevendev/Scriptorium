# Run receipt — SCRIP-CORPUS-020 Poem source-anchor review

- Date: 2026-09-18
- Issue: #109
- PR: #118 (merged)
- Base at review: `master@b4db400fd93ce3950d7503c7c923a5733799b8e3`
- Reviewed exact head: `cf0ce2e541327b8615c0ec0f119106433ab830ad`
- Merged commit: `00444df54f37f8a18cf66714b78dbd6f9442cf89`
- Mode: independent review / provenance

## Selected bounded unit

Perform the required later-run judgement of PR #118, independently verify the inferred upstream Poem-extension source anchor and its source-free evidence boundary, and merge only if the exact reviewed head and hosted replay remain clean.

## Review evidence

1. PR #118 was mergeable, 7 commits ahead / 0 behind current `master`, changed only the seven expected bounded-unit files, and had no inline review threads.
2. All eight exact-head pull-request workflows completed successfully. Dedicated run `35288948155` checked out exact head `cf0ce2e541327b8615c0ec0f119106433ab830ad`, ran the complete standard-library suite (227 tests), re-fetched the pinned upstream Poem source, regenerated the source-free manifest, uploaded it, and byte-compared it to the committed artifact.
3. Independent upstream path-history verification against `wikimedia/mediawiki-extensions-Poem` with the cutoff `2024-11-26T11:16:35Z` returned commit `03b3694613e23efa1254d8bbbb98121efaef2cb0` (`2024-10-20T09:15:42Z`) as the first/latest observed `includes/Poem.php` path commit not later than the cutoff.
4. Independent exact-file verification at that commit confirmed Git blob SHA-1 `a362a50d6e139b03a6afd5c24ce7a0923d68ee13`. The dedicated hosted replay independently revalidated source SHA-256 `86e853c6c41e94356d57824492f32407b916b890ccdfe31c38a081070fb5313c` and the source-free bounded semantic inventory.
5. Code/artifact review found the evidence boundary appropriately fail-closed: the artifact is explicitly `inferred_reconstruction_anchor`; it does not claim which Poem extension commit Russian Wikisource deployed, does not claim MediaWiki-core recursive-parse reproduction, does not freeze rendered Part 2 bytes, and does not promote FantLab source identity or M2 progress.

## Result / boundary

No blocking defect was found. A COMMENT review was submitted against the exact head, PR #118 was marked Ready, and it was squash-merged as `00444df54f37f8a18cf66714b78dbd6f9442cf89` without closing Issue #109.

The merge freezes only an upstream implementation candidate and bounded source semantics. Actual Russian Wikisource deployment equivalence and historical render equivalence remain unproven. M2 remains 0/5 source-matched works.

Next action: continue Issue #109 by freezing the concrete reached `#tag:poem` argument/attribute surface for the six exact calls, then reproduce only the MediaWiki-core recursive-parse behavior material to those plain values before resolving Part 2 bytes or the four-part literary-body composite.
