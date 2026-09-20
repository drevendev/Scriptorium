# SCRIP-CORPUS-043 — Twelve Chairs exact-410 markup surface

## Selection

- **Issue:** #173
- **Draft PR:** #174
- **Base:** `master@3fea17457b295f5307bc5a4d2e4635ffb7a81ce5`
- **Mode:** corpus / provenance, one bounded source-free renderer-prerequisite unit
- **Reason selected:** orientation found no open/review-ready PRs, no open issues and no failing recovery unit. The canonical queue retained SCRIP-CORPUS continuation, while the completed SCRIP-CORPUS-042 handoff explicitly identified a candidate-specific fail-closed Page-markup rendering/extraction path over the reviewed 410-page dependency surface as executable next work.

## Produced

- Added `scriptorium.twelve_chairs_render_surface` to replay the 410 exact pinned Page revisions and reduce transient Page wikitext to source-free construct shapes/counts and per-Page cryptographic receipts.
- Reused the already tested structural scanner semantics while keeping Twelve Chairs candidate/family/topology validation explicit.
- Added `scriptorium.twelve_chairs_render_surface_freeze` plus a compact durable source-free manifest at `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.render-surface.json`.
- Added deterministic regression coverage and `.github/workflows/twelve-chairs-render-surface.yml`, which replays the exact revisions, rebuilds the compact freeze and compares it byte-for-byte to the committed manifest.
- Updated the public Twelve Chairs candidate page, changelog fragment and durable state.

## Hosted evidence

The first hosted exact-revision audit ran as workflow `35527395084`, job `106121837144`, on authored head `ee1c912eacf9377a3085f4d1e2cf057d2bf07e9b`; every step succeeded, including contract tests, 410 exact Page revision replay, markup audit and source/gate boundary assertions. Artifact `10609958469` is a 33,926-byte ZIP with SHA-256 `ee26cf53526f352eadf5c8ce612b3befda6e82694e47ac5dfda3f1f5f4e74af9`; its full source-free audit JSON is 168,635 bytes with SHA-256 `ff076b56895edd5eabb1d39669ad9274691baf8ffa224e6e484961cda41ea4cd`, and `audit_sha256=5c9acbebf7d5e544edc22c6d95dc46fdb83afca757262083f84a68f64f1e3d75`.

The compact freeze binds:

- source Page-index SHA-256 `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f`;
- all 410 transient source-free Page receipts by SHA-256 `2d4483b7296cfcc18288816f8d4c3bde2e71750808e1d57be932768a1e82c6f2`;
- freeze manifest SHA-256 `8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23`.

The initial hosted run predates the compact-freeze comparison commits; therefore the final PR head still requires exact-head CI settlement and independent review before Ready/merge.

## Evidence boundary

The reviewed dependency inventory remains exactly **410** pages; gap pages 150/151/314/315 remain outside it. No Page wikitext, template argument values, OCR, rendered prose, PDF/image bytes or literary source text is committed. The surface inventory is a renderer prerequisite, not renderer equivalence: `rendering_profile_frozen=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Verification / handoff

The authored branch remains Draft PR #174. A later independent wake must review the exact final head against base `3fea17457b295f5307bc5a4d2e4635ffb7a81ce5`, confirm the dedicated exact-410 replay/freeze workflow and required repository workflows are settled and successful, inspect the compact freeze/public boundary, and only then decide Ready/merge. This wake must not self-approve the substantial change it authored.

## Benchmark / public movement

- **Benchmark:** no movement; M2 remains **0/5** source-matched works.
- **Public representation:** the dedicated 1928 candidate page now exposes the exact-410 source-free markup surface and explicitly distinguishes inventory from rendering semantics/body identity.
