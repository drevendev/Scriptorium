# SCRIP-CORPUS-056 — define Petersburg 1916 OCR/body promotion contract

- Selected the executable P2 corpus/provenance continuation after confirming no open PR/recovery work and no open issues on `master@3429745d42ee57a3112d7a3c940ee1d2f3ff30f9`.
- Opened Issue #199 and Draft PR #200 from the exact master head.
- Added source-free contract `scriptorium-petersburg-1916-ocr-body-contract-v1`, cryptographically bound to the independently frozen 632-page, 3,621,459-byte 1916 first-book-edition PDF identity from SCRIP-CORPUS-038. Canonical contract SHA-256: `d338d8dc4d800b0fe28a848e383265ba9a0e720e75962f7f9e5733ad727a20d2`.
- The v1 contract deliberately leaves exact literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all raw/normalized body outputs unbound/null. Any bound extraction profile must use a new independently evidenced contract version.
- Defined only deterministic future composition semantics: ascending PDF-page order, stripping trailing newlines per selected page, joining pages with two LF characters, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization.
- Added a fail-closed validator plus 7 focused regressions covering scan-identity drift, silent page/toolchain binding, premature body/gate promotion, source-payload leakage, and composition drift.
- Added an offline pull-request workflow that validates the contract and canonical digest without downloading or persisting the PDF, page images, OCR, or literary prose.
- Updated the Petersburg public candidate/provenance surfaces to expose the defined-but-unbound contract while keeping >=300k corpus admission, FantLab analyzer-input identity, diagnostics, parity and M2 closed. M2 remains **0/5**.
- Independent later review `5274921660` re-read all 10 changed files on exact head `a658f0dcdb548145294bb26467d4ef66a95bc413` against unchanged base `3429745d42ee57a3112d7a3c940ee1d2f3ff30f9`, found no merge blocker or open review thread, and confirmed all 16 PR-triggered workflow runs settled `success`, including the dedicated Petersburg OCR contract workflow and all three pinned-pylem jobs.
- PR #200 was marked Ready and squash-merged with expected-head protection as `d379830b3c22402e90c3fad71cf87688d129c0ed`, automatically closing Issue #199 completed.
