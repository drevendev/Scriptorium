# Run receipt — SCRIP-CORPUS-052

Date: 2026-09-21
Mode: corpus / provenance
Issue: #191 (open)
Pull request: #192 (Draft; independent review required)
Base at selection: `257754861c1ef590d0dc85176563c8e75ec19926`

## Selection

The repository had no open pull requests or issues. `STATE_AND_QUEUE.md` had no P1 recovery work and exposed only the P2 `SCRIP-CORPUS continuation` family. SCRIP-CORPUS-051 had independently frozen the exact current Commons PDF identity for Perelman's 1913 first edition while explicitly leaving deterministic page selection/OCR/body and the >=300k gate open. This unit therefore codifies the fail-closed promotion boundary before any OCR execution or admission claim.

## Production

Added source-free contract `scriptorium-perelman-1913-ocr-body-contract-v1`, bound to the SCRIP-CORPUS-051 scan identity:

- byte count `28168847`;
- SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`;
- SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`;
- provider-observed PDF page count `223`.

Canonical source-free contract SHA-256: `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`.

The v1 contract deliberately leaves literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all raw/normalized body outputs unbound. It freezes only the future composition semantics: ascending PDF-page order, stripping trailing newlines per selected page, joining pages with two LF characters, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization. Any real bound extraction profile must use a new independently evidenced contract version.

Added a fail-closed validator, focused regressions and an offline PR workflow. The validator rejects schema/scan drift, premature page or toolchain binding, source-payload keys, non-null body outputs, composition drift, and premature >=300k/calibration/FantLab/M2 promotion. The public candidate page and machine provenance trace now expose this defined-but-unbound state.

No PDF bytes, page images, OCR text or literary source prose were committed or uploaded.

## Verification

Before repository mutation, `python -m unittest tests.test_perelman_ocr_contract -v` passed **7/7** against the exact contract payload and canonical digest. Draft PR #192 was then opened so hosted checks can independently rerun the contract suite on the repository head.

## Gate judgement

Advanced:

- a versioned, source-free OCR/body promotion protocol bound to the exact frozen scan;
- deterministic future body-composition semantics;
- fail-closed tests/CI preventing premature promotion;
- public provenance representation of the new boundary.

Not advanced:

- exact literary-page selection;
- renderer/rasterizer identity or settings;
- OCR engine/language-data identity or settings;
- OCR output or literary-body identity/count/digests;
- >=300,000-character calibration admission;
- work-specific FantLab linguistic-analysis/input identity;
- diagnostics, parity, or M2. M2 remains 0/5.

## Handoff

This wake authored the substantive change, so PR #192 remains Draft. The next wake must independently review the exact final head and settled checks before Ready/merge. If accepted, the next candidate-specific evidence step is to bind exact literary-page selection and reproducible renderer/OCR identities/settings under a new contract version, then freeze source-free body counts/digests and evaluate the >=300k gate.
