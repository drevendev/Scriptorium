# Run receipt — SCRIP-CORPUS-052

Date: 2026-09-21
Mode: corpus / provenance + recovery
Issue: #191 (open)
Pull request: #192 (Draft; independent review required)
Base at selection: `257754861c1ef590d0dc85176563c8e75ec19926`

## Selection

The repository initially had no open pull requests or issues. `STATE_AND_QUEUE.md` had no P1 recovery work and exposed only the P2 `SCRIP-CORPUS continuation` family. SCRIP-CORPUS-051 had independently frozen the exact current Commons PDF identity for Perelman's 1913 first edition while explicitly leaving deterministic page selection/OCR/body and the >=300k gate open. This unit therefore codified the fail-closed promotion boundary before any OCR execution or admission claim.

A later recovery wake re-oriented from Draft PR #192, as required by the selection ladder, and found that its original exact authored head had failing required repository-wide checks. Recovery therefore preempted merge judgement and new corpus production.

## Production

Added source-free contract `scriptorium-perelman-1913-ocr-body-contract-v1`, bound to the SCRIP-CORPUS-051 scan identity:

- byte count `28168847`;
- SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`;
- SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`;
- provider-observed PDF page count `223`.

Canonical source-free contract SHA-256: `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`.

The v1 contract deliberately leaves literary-page selection, rasterizer identity/settings, OCR engine/language-data identity/settings, and all raw/normalized body outputs unbound. It freezes only the future composition semantics: ascending PDF-page order, stripping trailing newlines per selected page, joining pages with two LF characters, UTF-8 raw-body encoding, and `scriptorium-text-v1` normalization. Any real bound extraction profile must use a new independently evidenced contract version.

Added a fail-closed validator, focused regressions and an offline PR workflow. The validator rejects schema/scan drift, premature page or toolchain binding, source-payload keys, non-null body outputs, composition drift, and premature >=300k/calibration/FantLab/M2 promotion. The public candidate page and machine provenance trace expose this defined-but-unbound state.

No PDF bytes, page images, OCR text or literary source prose were committed or uploaded.

## Initial verification

Before the original repository mutation, `python -m unittest tests.test_perelman_ocr_contract -v` passed **7/7** against the exact contract payload and canonical digest. Dedicated hosted workflow run `35654095466` later checked out authored head `1d43935ba62f9d175d2bc981ec2284a302ab0289` and completed successfully.

That dedicated success was not sufficient for merge readiness. Independent settlement inspection found required repository-wide failures on the same exact head:

- `Scriptorium Pages` run `35654095114`, job `106513287146`, failed the standard-library suite after **426 tests** because two existing `tests/test_perelman_provenance_trace.py` assertions still expected the pre-contract status and wording;
- `Perelman 1913 scan identity` run `35654095223`, job `106513287574`, reproduced the same **2 failures in 11 focused tests** and therefore skipped its later network replay/evidence steps.

The failures were concrete stale-test integration regressions rather than evidence that OCR/body gates had advanced.

## Recovery repair

The recovery wake repaired the stale provenance tests instead of merging around failing checks. The updated tests now:

- expect `scan_binary_frozen_ocr_contract_defined_body_unverified` for both immutable-identity and admissibility status;
- verify that the next-evidence text starts after the defined-but-unbound v1 contract rather than after only the binary freeze;
- load and validate the committed OCR/body contract directly;
- bind the structured provenance trace to the exact contract version, path and canonical SHA-256;
- assert that only the frozen scan is bound while page selection, rasterization, OCR and body outputs remain unbound;
- require the public candidate page to expose the canonical contract SHA-256 without source payload.

Independent diff review also found a branch-only accidental transcription error in the retained Road to Nowhere SHA-256 summary. The recovery restores the canonical value `e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`; this does not change that candidate's body identity.

## Gate judgement

Advanced:

- a versioned, source-free OCR/body promotion protocol bound to the exact frozen scan;
- deterministic future body-composition semantics;
- fail-closed tests/CI preventing premature promotion;
- public provenance representation of the new boundary;
- integration coverage tying that public/machine provenance to the actual contract digest and binding state.

Not advanced:

- exact literary-page selection;
- renderer/rasterizer identity or settings;
- OCR engine/language-data identity or settings;
- OCR output or literary-body identity/count/digests;
- >=300,000-character calibration admission;
- work-specific FantLab linguistic-analysis/input identity;
- diagnostics, parity, or M2. M2 remains 0/5.

## Handoff

The recovery wake authored substantive repair changes, so PR #192 remains Draft and is not merged in this wake. Fresh hosted checks must settle on the repaired exact final head, then a later independent wake must review that exact head before Ready/merge. If accepted, a later candidate-specific evidence unit may bind exact literary-page selection and reproducible renderer/OCR identities/settings under a new contract version, then freeze source-free body counts/digests and evaluate the >=300k gate.
