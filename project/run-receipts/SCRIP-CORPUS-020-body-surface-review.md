# Run receipt — SCRIP-CORPUS-020 body extraction surface review

- Date: 2026-09-18
- Unit: SCRIP-CORPUS-020
- Issue: #109
- Pull request: #123
- Reviewed exact head: `fb5e787027e9b156594bb217845652452d945017`
- Merge base before review: `78f168b86c6b7563a5f37f164b29234ddc4fc5f1`
- Merge result: squash commit `c5b527f3390ae6aec5cfc3716d67da6af8311aa4`
- Review result: no blocking defect; marked Ready and merged

## Verification

- Immediately before merge, PR #123 was mergeable and 9 commits ahead / 0 behind current `master`.
- No inline review threads or prior submitted reviews were present before this later-run review.
- All 12 pull-request workflows associated with exact head `fb5e787027e9b156594bb217845652452d945017` completed successfully.
- Dedicated workflow run `35317967589`, job `105513730940`, checked out the exact reviewed head and completed the standard-library suite, exact pinned-source capture, source-free regeneration and byte comparison successfully.
- The four pinned parent revisions remain oldids `5733765`, `5198033`, `5138882`, `5724453`.
- Direct parent `poemx1` inventory is 5 / 2 / 0 / 0. The two Part 2 calls at offsets `25519..25540` and `25568..26321` are outside the frozen target-only `#lst` span `581758..581810`, so target substitution necessarily preserves both.
- The merged artifact stores only source-free structural names, counts, offsets and cryptographic identities; no literary prose is committed.

## Evidence boundary

This merge freezes only the pre-extraction structural surface. It does not establish a literary-body identity, deterministic four-part composition, historical Russian Wikisource MediaWiki/Poem deployment equivalence, or FantLab analyzer-input identity. The previously merged Part 2 resolution remains candidate-specific inferred target-substitution/source-graph evidence, not historical parser-byte parity. M2 remains 0/5.

## Continuation

Keep Issue #109 open. Next implement fail-closed literary extraction for Parts 1–4 against the frozen structural surface, explicitly handling all seven direct parent `poemx1` calls, then define deterministic ordered `1 -> 2 -> 3 -> 4` composition before recording source-free raw and `scriptorium-text-v1` composite literary-body digests.
