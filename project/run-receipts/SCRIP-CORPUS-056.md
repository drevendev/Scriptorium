# Run receipt — SCRIP-CORPUS-056

- Unit: `SCRIP-CORPUS-056`
- Issue: #199
- Pull request: #200 (Draft)
- Base: `master@3429745d42ee57a3112d7a3c940ee1d2f3ff30f9`
- Authored branch: `scrip-corpus-056-petersburg-ocr-contract`
- Selection: no P0/P1 work existed at orientation; selected the explicit P2 Petersburg candidate-specific OCR/provenance continuation.

## Produced

Defined source-free contract `scriptorium-petersburg-1916-ocr-body-contract-v1` for the already frozen 632-page 1916 first-book-edition PDF. The contract is bound to 3,621,459 bytes, SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`, SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`; canonical contract SHA-256 is `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`.

Only deterministic future composition semantics are defined. Literary-page selection, rasterization, OCR engine/language data/settings, raw/normalized body outputs, >=300k admission, FantLab analyzer-input identity, diagnostics and M2 remain unbound/closed. No PDF bytes, page images, OCR or literary prose were committed.

Added the fail-closed validator, 7 focused regressions, dedicated offline PR workflow, synchronized public candidate/provenance records, changelog fragment and durable REVIEW_PENDING state.

## Verification

Before GitHub mutation, the focused contract suite was exercised against the exact v1 JSON shape and passed 7/7 locally. The canonical digest was independently recomputed from sorted compact UTF-8 JSON as `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`.

Hosted CI is the merge gate. PR #200 intentionally remains Draft because this run authored the substantive change; the next wake must independently review its exact settled head and all hosted checks before any Ready/merge decision.

## Benchmark/public movement

Benchmark movement: none; M2 remains **0/5**. Public representation improves by exposing an inspectable, source-free, versioned promotion boundary for Petersburg without implying that OCR/body or FantLab parity evidence already exists.
