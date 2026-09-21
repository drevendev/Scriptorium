# SCRIP-CORPUS-052 — define Perelman OCR/body promotion contract

- Selected the next P2 corpus/provenance continuation after SCRIP-CORPUS-051 completed, keeping all higher-priority recovery/review rows empty.
- Opened Issue #191 from `master@257754861c1ef590d0dc85176563c8e75ec19926`.
- Added source-free contract `scriptorium-perelman-1913-ocr-body-contract-v1`, cryptographically bound to the independently frozen 28,168,847-byte scan identity from SCRIP-CORPUS-051. Canonical contract SHA-256: `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`.
- The v1 contract deliberately leaves literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all body outputs unbound/null. A later bound extraction profile must use a new independently evidenced contract version.
- Froze only the deterministic future composition policy: ascending PDF-page order, per-page trailing-newline stripping, two-LF page joining, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization.
- Added a fail-closed validator and 7 focused regressions covering scan-identity drift, premature page/toolchain binding, premature body/gate promotion, source-payload leakage, and composition drift. The same focused suite passed locally before repository mutation.
- Added an offline PR workflow that validates the source-free contract and canonical digest without downloading, storing, or uploading scan bytes, page images, OCR text, or literary source prose.
- Updated the public candidate page and machine provenance trace to expose the defined-but-unbound promotion boundary. OCR/body/>=300k/FantLab/diagnostic/M2 gates remain closed; M2 remains **0/5**.
- Independent recovery review of authored head `1d43935ba62f9d175d2bc981ec2284a302ab0289` found required hosted CI failures: Pages ran 426 tests and the Perelman scan workflow ran 11 focused tests; both exposed the same two stale provenance assertions after the new contract-defined status and next-evidence wording landed.
- Repaired `tests/test_perelman_provenance_trace.py` to validate the new status and next-evidence boundary and strengthened it to bind the machine provenance trace to the actual v1 contract version, path, canonical SHA-256 and unbound binding flags.
- Corrected an unrelated branch-only transcription regression in the retained Road to Nowhere SHA-256 summary, restoring canonical digest `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`.
- Independent exact-head review `5272577616` re-read repaired head `742f19c88fffac29974f31cc21cdebb1390f7255` against unchanged base `257754861c1ef590d0dc85176563c8e75ec19926`, reviewed all 10 changed files, found no remaining merge blocker, and confirmed there were no open review threads.
- All 16 PR-triggered workflows on the exact reviewed head settled `success`; dedicated OCR-contract run `35659674619`, Pages run `35659674823`, and Perelman scan replay all completed successfully on that SHA.
- PR #192 was marked Ready and squash-merged as `20ec3654240efdfc6105f8a65eb156380140a4ff`, closing Issue #191 completed. OCR/body/>=300k/FantLab/diagnostic/M2 gates remain closed; M2 remains **0/5**.
