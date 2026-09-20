# SCRIP-CORPUS-044 — Twelve Chairs fail-closed render profile

## Selection

- **Issue:** #175
- **PR:** #176 (Draft; independent review required)
- **Base:** `master@af2f2e8c857ebb024ccac591ad50e61f0c60f3d6`
- **Mode:** corpus / provenance, one bounded renderer-prerequisite unit
- **Reason selected:** no interrupted/review-ready unit was present at orientation time; `STATE_AND_QUEUE` returned to the P2 SCRIP-CORPUS continuation and explicitly named a candidate-specific fail-closed Twelve Chairs Page-markup profile as executable next evidence.

## Produced

- Added `scriptorium.twelve_chairs_render_profile`, which consumes only the committed exact-410 source-free rendering-surface freeze.
- Added `ilf-petrov-twelve-chairs-zif-1928.render-profile.json`, bound to Page-index SHA-256 `c1e3280984e640b8fe739a752ff49a3327633f49b52a635bd2d2d1e6a09f538f` and render-surface freeze SHA-256 `8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23`.
- Frozen profile SHA-256: `88e410311435ab6bcfbd70ab0a2cea73ffe304e3ce2876d241d25ea38cc5d5cd`.
- The profile classifies every reviewed shape and fails closed on additions/removals: **12 tag shapes / 3,488 tokens** and **30 template shapes / 602 invocations**.
- Structural decisions are explicit for comments, `noinclude`, `pagequality`, `section`, simple containers and `<br>`. Template expansion is deliberately not inferred from names: **all 30 template shapes / 602 invocations remain unresolved**, as do **410 `<references/>` tokens**. The **246 `nop`** invocations are explicitly marked inter-page-sensitive.
- Added five standard-library regression tests and `.github/workflows/twelve-chairs-render-profile.yml`, which rebuilds the profile deterministically, compares parsed JSON to the committed artifact, and asserts the downstream gate boundary.
- Updated the public candidate page and `STATE_AND_QUEUE` to expose the decision boundary without claiming a completed renderer.

## Verification boundary

An authored-head dedicated workflow successfully passed profile/provenance tests and deterministic rebuild before the durable-state handoff commit. The final authored head is recorded in the PR conversation together with its exact-head workflow settlement; a later wake must independently re-read that exact head before any Ready/merge decision.

No Page wikitext, template argument values, rendered prose, OCR, PDF/image bytes or literary text are committed by this unit. The profile sets `rendering_profile_frozen=true` specifically for the fail-closed decision table while keeping `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Independent review — 2026-09-20

Exact authored head `0b289b595080b96a693fa3d3a0ca69c423750a43` was reviewed against unchanged base `af2f2e8c857ebb024ccac591ad50e61f0c60f3d6`. The diff had 8 commits / 8 changed files, no inline review threads, and all 18 PR-triggered workflows had settled `success`. Dedicated profile run `35533932225` / job `106139451346` and Pages verify/build run `35533932205` / job `106139451498` both checked out that exact head and succeeded.

The review found two merge blockers and recorded them in PR review `5261712805`:

1. `scriptorium.twelve_chairs_render_profile._validate_surface_identity()` checks only the embedded `freeze_manifest_sha256` value and does not call the existing `twelve_chairs_render_surface_freeze.validate_freeze_manifest()`. As a result, a mutation to an existing surface count/value can retain the stale embedded digest and still be consumed into a newly generated profile. This violates Issue #175's fail-closed-on-surface-change acceptance criterion. Fix requires validating the source freeze before classification plus a regression test that mutates an existing covered value without recomputing the digest and expects failure.
2. Canonical structured provenance is stale on the reviewed head: `ilf-petrov-twelve-chairs-zif-1928.source-graph.json` and `ilf-petrov-twelve-chairs-ru.json` still report `rendering_profile_frozen=false` / renderer-profile work as future evidence even though the public candidate page declares the decision profile frozen. Those structured records must be synchronized while preserving `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, and all composition/body/admission/FantLab/M2 gates closed.

PR #176 remains Draft. No Ready/merge action is admissible until both findings are repaired and a fresh exact-head review settles.

## Benchmark / public movement

- **Benchmark:** no movement; M2 remains **0/5** source-matched works.
- **Public representation:** the dedicated 1928 candidate page exposes the intended fail-closed decision profile, but structured provenance remains inconsistent until the review blocker is repaired.

## Handoff

Repair the two review findings on PR #176, let all affected workflows settle on the new exact head, then perform a new independent review. Do not mark Ready or merge before that review. Literary-body composition remains non-executable while template/reference semantics are unresolved.