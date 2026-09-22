# Run receipt — SCRIP-CORPUS-056

- Unit: `SCRIP-CORPUS-056`
- Issue: #199 (closed completed)
- Pull request: #200 (independently reviewed; squash-merged)
- Base: `master@3429745d42ee57a3112d7a3c940ee1d2f3ff30f9`
- Authored head: `a658f0dcdb548145294bb26467d4ef66a95bc413`
- Merge commit: `d379830b3c22402e90c3fad71cf87688d129c0ed`
- Review: `5274921660`
- Authored branch: `scrip-corpus-056-petersburg-ocr-contract`
- Selection: no P0/P1 work existed at authoring orientation; selected the explicit P2 Petersburg candidate-specific OCR/provenance continuation. The next wake correctly preempted normal flow for independent P1 review/merge recovery.

## Produced

Defined source-free contract `scriptorium-petersburg-1916-ocr-body-contract-v1` for the already frozen 632-page 1916 first-book-edition PDF. The contract is bound to 3,621,459 bytes, SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`, SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`; canonical contract SHA-256 is `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`.

Only deterministic future composition semantics are defined. Literary-page selection, rasterization, OCR engine/language data/settings, raw/normalized body outputs, >=300k admission, FantLab analyzer-input identity, diagnostics and M2 remain unbound/closed. No PDF bytes, page images, OCR or literary prose were committed.

Added the fail-closed validator, 7 focused regressions, dedicated offline PR workflow, synchronized public candidate/provenance records, changelog fragment and durable project state.

## Verification

The authored run exercised the focused contract suite against the exact v1 JSON shape and recorded the canonical digest. The later independent wake re-read all 10 changed files on exact head `a658f0dcdb548145294bb26467d4ef66a95bc413` against unchanged base `3429745d42ee57a3112d7a3c940ee1d2f3ff30f9`, found no merge blocker or open review thread, and submitted COMMENT review `5274921660` rather than self-approving the authored PR.

All 16 PR-triggered workflow runs on that exact head settled `success`. The dedicated `Petersburg 1916 OCR promotion contract` workflow validated the source-free boundary and canonical digest; the pinned-pylem workflow's three jobs all completed successfully, including the complete standard-library suite and Anna sidecar replay.

PR #200 was marked Ready and squash-merged with expected-head protection as `d379830b3c22402e90c3fad71cf87688d129c0ed`, automatically closing Issue #199 as completed. Post-merge state/changelog/receipt reconciliation is mechanical bookkeeping only and does not alter analyzer semantics.

## Benchmark/public movement

Benchmark movement: none; M2 remains **0/5**. Public representation now canonically exposes an inspectable, source-free, versioned promotion boundary for Petersburg without implying that OCR/body or FantLab parity evidence already exists.
