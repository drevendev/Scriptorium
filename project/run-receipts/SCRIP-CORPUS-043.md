# SCRIP-CORPUS-043 — Twelve Chairs exact-410 markup surface

## Selection

- **Issue:** #173
- **PR:** #174
- **Base:** `master@3fea17457b295f5307bc5a4d2e4635ffb7a81ce5`
- **Final authored head:** `3784a7e3380bb9a9e5dd7a380d6f38fc9497bab7`
- **Mode:** corpus / provenance, one bounded source-free renderer-prerequisite unit followed by an independent later-wake review unit
- **Reason selected:** the authored wake found no recovery/review work and selected the queued SCRIP-CORPUS continuation. The later review wake was preemptively selected by `STATE_AND_QUEUE` because PR #174 was `REVIEW_PENDING`.

## Produced

- Added `scriptorium.twelve_chairs_render_surface` to replay the 410 exact pinned Page revisions and reduce transient Page wikitext to source-free construct shapes/counts and per-Page cryptographic receipts.
- Reused the already tested structural scanner semantics while keeping Twelve Chairs candidate/family/topology validation explicit.
- Added `scriptorium.twelve_chairs_render_surface_freeze` plus a compact durable source-free manifest at `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-surface.json`.
- Added deterministic regression coverage and `.github/workflows/twelve-chairs-render-surface.yml`, which replays the exact revisions, rebuilds the compact freeze and compares it byte-for-byte to the committed manifest.
- Updated the public Twelve Chairs candidate page and structured provenance without promoting renderer/body/parity claims.

## Final exact-head evidence

Independent review compared exact head `3784a7e3380bb9a9e5dd7a380d6f38fc9497bab7` to unchanged base `3fea17457b295f5307bc5a4d2e4635ffb7a81ce5`: **16 commits ahead / 0 behind**, **13 changed files**, no review threads, and no blocking findings.

All **17 PR-triggered workflows** on the final head settled `success`. Dedicated workflow `35527922325`, job `106123230589`, checked out the exact reviewed SHA and passed:

- 14 dedicated source-free surface/freeze/provenance contract tests;
- replay of all 410 exact pinned Page revisions with title/timestamp/MediaWiki SHA-1 verification before transient content inspection;
- byte-for-byte rebuild comparison of the durable compact freeze;
- downstream gate-boundary assertions;
- source-free artifact upload.

The Scriptorium Pages workflow `35527922295`, job `106123230621`, also checked out the exact reviewed SHA and ran the complete Python 3.13 standard-library suite: **362 tests, all OK**, followed by a deterministic static-site rebuild comparison.

Independent artifact verification downloaded artifact `10610353546` and reproduced:

- ZIP: **35,265 bytes**, SHA-256 `67ed39ab6b3257d59fdd7586aa5de3b49b15a77d219879a29d986f60bc0542cd`;
- `ilf-petrov-twelve-chairs-zif-1928.render-surface.full.json`: **168,635 bytes**, SHA-256 `ff076b56895edd5eabb1d39669ad9274691baf8ffa224e6e484961cda41ea4cd`;
- `ilf-petrov-twelve-chairs-zif-1928.render-surface.json`: **5,205 bytes**, SHA-256 `25d874b9b4dc79e63639351ebc30dc674efe4227b81f5fc2f3eed2bc183c3c27`.

The full audit contains exactly **410** Page receipts, each limited to source-free identity/digest/count fields. The compact freeze binds:

- source Page-index SHA-256 `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f`;
- all 410 transient source-free Page receipts by SHA-256 `2d4483b7296cfcc18288816f8d4c3bde2e71750808e1d57be932768a1e82c6f2`;
- freeze manifest SHA-256 `8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23`.

The earlier authored intermediate head that failed the `cmp` step had semantically equivalent JSON with noncanonical indentation. The durable freeze was regenerated through the canonical serializer; final exact-head replay and byte comparison are green.

## Evidence boundary

The reviewed dependency inventory remains exactly **410** pages; gap pages 150/151/314/315 remain outside it. No Page wikitext, template argument values, OCR, rendered prose, PDF/image bytes or literary source text is committed. The surface inventory is a renderer prerequisite, not renderer equivalence: `rendering_profile_frozen=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Review / merge

The later wake recorded review as **COMMENT**, not self-approval. With the head/base unchanged and all exact-head evidence green, PR #174 was marked Ready and squash-merged as `096d551b4f55ddfe3e76d61f0d3e067c40e9502d`. The `Closes #173` linkage closed Issue #173 with reason `completed`.

## Benchmark / public movement

- **Benchmark:** no movement; M2 remains **0/5** source-matched works.
- **Public representation:** the dedicated 1928 candidate page now exposes, on master, the independently reviewed exact-410 source-free markup surface and explicitly distinguishes construct inventory from rendering semantics/body identity.
