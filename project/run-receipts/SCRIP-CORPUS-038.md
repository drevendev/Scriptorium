# Run receipt — SCRIP-CORPUS-038

Status: `COMPLETE`
Issue: #163 (closed completed)
Pull request: #164 (squash-merged as `fac5aab20f5426e1d3e01853027222c5cd8c04ed`)
Base master at selection: `1108fb5bf04af7bf1a6b11e78ff31d7e082cd9f0`

## Selected bounded unit

Freeze the exact Wikimedia Commons PDF byte identity for the retained Andrei Bely *Petersburg* 1916 first-book-edition facsimile without storing the PDF, OCR, images or literary source text. Preserve the 1916/1922 edition distinction and leave literary-body/FantLab gates closed.

## Authored evidence

The branch added a streaming source-free identity helper, six no-network unit tests, a hosted capture/replay workflow, the frozen scan receipt, a provenance-binding regression test, a dedicated public candidate page and corpus navigation/provenance updates.

Initial hosted capture on head `5ebabf54e29ad990ae4dd860f6290ee8ee61d3b1`:

- workflow run: `35498115419`
- job: `106044817170`
- Python: 3.13.15
- focused tests: 6/6 passed
- exact PDF byte count: `3621459`
- SHA-1: `682476934dd6ed49c6bbcdb0720127c1812ff477`
- SHA-256: `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`
- source-free capture artifact: `10601567738`
- artifact size: `1565` bytes
- artifact ZIP SHA-256: `8b9915a05d554f9ca5bdd12ea0d760b57cd2d2d0fc81e1c164058d81cad6a2e2`

The independently observed PDF SHA-1 equals the trace's previously retained Commons Page Information hash. The canonical trace records this as a verified equality for this exact snapshot rather than an inferred metadata semantic.

## Closed boundaries

- `binary_bytes_committed=false`
- `ocr_included=false`
- `literary_source_text_included=false`
- `ocr_extraction_profile_frozen=false`
- `literary_body_count_and_digests_frozen=false`
- `minimum_300k_proved_from_frozen_body=false`
- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `m2_parity_admissible=false`

FantLab's published 944,182-character count is retained only as external diagnostic metadata. It neither proves that this exact 1916 PDF is FantLab's input nor admits an unfrozen OCR/text body to the >=300k corpus.

## Independent review and merge

A later run independently re-read exact PR head `11ca95744ce0b28c213d21b2221a6fc1f6d6b831` against unchanged base `1108fb5bf04af7bf1a6b11e78ff31d7e082cd9f0`. The branch was 13 commits ahead / 0 behind, mergeable, with no inline review threads, and all **15/15** exact-head pull-request workflows had settled `success`.

Dedicated `Petersburg 1916 scan identity` run `35498451938`, job `106045731420`, explicitly checked out the reviewed SHA, passed all 10 scan/provenance tests, re-streamed the exact retained Commons original, and reproduced:

- byte count `3621459`
- SHA-1 `682476934dd6ed49c6bbcdb0720127c1812ff477`
- SHA-256 `b08820ad1339894c6d20fbaa2367c11385492bf376d199f8de23c859ef6ddef5`

Independent artifact inspection downloaded exact-head artifact `10601673060`, recomputed its 1,313-byte ZIP as `sha256:1ceb12a969e98e46178c785a956a70c63b4517b16660c1ba99278e6a9f83c0b2`, and confirmed that it contains only the committed source-free receipt plus verification JSON. No PDF, image, OCR or literary source payload was present.

No blocker remained. The review was recorded as a COMMENT rather than self-approval because the connected identity also authored the PR. PR #164 was marked Ready and squash-merged as `fac5aab20f5426e1d3e01853027222c5cd8c04ed`, automatically closing Issue #163 completed. The scan identity is now retained in master; OCR/body/admission/FantLab/M2 gates remain closed. Benchmark movement: none. M2: **0/5**.
