# SCRIP-CORPUS-013 — The Twelve Chairs edition-family trace

Date: 2026-09-16
Issue: #95
PR: #96
Merged commit: `76d4c3a5b44ad1ad13d2c6869ad68f280eff0b2a`
Reviewed head: `ee9799b6457a21502bfaac677ae91af1359ee409`

## Independent review

A later run independently reviewed the exact PR head before merge. The base remained `52dc8fbc4b4782b1e7980c09ee420ddd2fd75cc6`; the branch was 4 commits ahead / 0 behind and contained exactly three source-free additions: the public candidate note, machine-readable source-edition trace, and authored-run receipt. No inline review threads were present.

Fresh evidence review reconfirmed FantLab work `182817` at 572,654 characters / 80,203 words on 17 September 2022 and preserved FantLab's explicit warning that a two-author work mixes styles and cannot yield exact author-recognition results. Russian Wikisource reconfirmed the later GIKhL 1961 / 1938-derived editorial family with 40 chapters and a separate Zemlya i Fabrika 1928 first standalone edition with 41 chapters. The structural difference is retained only as evidence that the public routes require distinct text-family identities; it is not a byte-level diff and neither route is claimed to be FantLab's analyzer input.

The 1928 facsimile surface currently reports 424 pages / 74.37 MB and points to the Russian National Electronic Library. Scriptorium has not frozen the scan bytes, so no binary identity, OCR identity, or page-to-text mapping is claimed.

## Verification

Exact-head `Scriptorium Pages` run `35118672960` completed successfully. The standard-library suite, canonical static build, deterministic rebuild verification, and artifact upload all passed; PR deployment was correctly skipped. The morphology-provider workflow did not trigger for this corpus-only scope, so no provider result is claimed.

## Merge decision

No blocking defect was found. PR #96 was squash-merged as `76d4c3a5b44ad1ad13d2c6869ad68f280eff0b2a`, closing Issue #95 as completed.

Benchmark movement: none. `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, diagnostics remain disabled, and M2 remains **0/5 source-matched works**.
