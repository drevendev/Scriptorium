# SCRIP-CORPUS-052 — define Perelman OCR/body promotion contract

- Selected the next P2 corpus/provenance continuation after SCRIP-CORPUS-051 completed, keeping all higher-priority recovery/review rows empty.
- Opened Issue #191 from `master@257754861c1ef590d0dc85176563c8e75ec19926`.
- Added source-free contract `scriptorium-perelman-1913-ocr-body-contract-v1`, cryptographically bound to the independently frozen 28,168,847-byte scan identity from SCRIP-CORPUS-051. Canonical contract SHA-256: `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`.
- The v1 contract deliberately leaves literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all body outputs unbound/null. A later bound extraction profile must use a new independently evidenced contract version.
- Froze only the deterministic future composition policy: ascending PDF-page order, per-page trailing-newline stripping, two-LF page joining, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization.
- Added a fail-closed validator and 7 focused regressions covering scan-identity drift, premature page/toolchain binding, premature body/gate promotion, source-payload leakage, and composition drift. The same focused suite passed locally before repository mutation.
- Added an offline PR workflow that validates the source-free contract and canonical digest without downloading, storing, or uploading scan bytes, page images, OCR text, or literary source prose.
- Updated the public candidate page and machine provenance trace to expose the defined-but-unbound promotion boundary. OCR/body/>=300k/FantLab/diagnostic/M2 gates remain closed; M2 remains **0/5**.
