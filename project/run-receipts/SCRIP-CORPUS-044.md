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
- The profile classifies every reviewed shape: **12 tag shapes / 3,488 tokens** and **30 template shapes / 602 invocations**.
- Structural decisions are explicit for comments, `noinclude`, `pagequality`, `section`, simple containers and `<br>`. Template expansion is deliberately not inferred from names: **all 30 template shapes / 602 invocations remain unresolved**, as do **410 `<references/>` tokens**. The **246 `nop`** invocations are explicitly marked inter-page-sensitive.
- Added standard-library regression tests and `.github/workflows/twelve-chairs-render-profile.yml`, which rebuilds the profile deterministically, compares parsed JSON to the committed artifact, and asserts the downstream gate boundary.
- Updated the public candidate page to expose the decision boundary without claiming a completed renderer.

## Verification boundary

No Page wikitext, template argument values, rendered prose, OCR, PDF/image bytes or literary text are committed by this unit. The profile sets `rendering_profile_frozen=true` specifically for the fail-closed decision table while keeping `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, `inter_page_composition_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, and `m2_parity_admissible=false`.

## Independent review — 2026-09-20

Exact authored head `0b289b595080b96a693fa3d3a0ca69c423750a43` was reviewed against unchanged base `af2f2e8c857ebb024ccac591ad50e61f0c60f3d6`. The diff had 8 commits / 8 changed files, no inline review threads, and all 18 PR-triggered workflows had settled `success`. Dedicated profile run `35533932225` / job `106139451346` and Pages verify/build run `35533932205` / job `106139451498` both checked out that exact head and succeeded.

The review found two merge blockers and recorded them in PR review `5261712805`:

1. `scriptorium.twelve_chairs_render_profile._validate_surface_identity()` checked only the embedded `freeze_manifest_sha256` value and did not call the existing `twelve_chairs_render_surface_freeze.validate_freeze_manifest()`. A mutation to an existing surface count/value could therefore retain the stale embedded digest and still be consumed into a newly generated profile.
2. Canonical structured provenance was stale: `ilf-petrov-twelve-chairs-zif-1928.source-graph.json` and `ilf-petrov-twelve-chairs-ru.json` still reported the render profile as unfrozen/future work even though the public candidate page declared the decision profile frozen.

## Recovery repair — 2026-09-20/21

This run repaired both review blockers on the existing Draft PR rather than selecting new work.

- `_validate_surface_identity()` now calls `validate_freeze_manifest(surface)` before checking the expected candidate-specific identity. The committed render-surface object's canonical self-digest is therefore verified before any tag/template classification is consumed.
- Added a regression that changes an existing frozen tag-shape count without recomputing `freeze_manifest_sha256` and requires `rendering-surface freeze digest drift`; the existing added/removed-shape tests now also prove the cryptographic freeze boundary triggers first.
- Synchronized `ilf-petrov-twelve-chairs-zif-1928.source-graph.json` and `ilf-petrov-twelve-chairs-ru.json` with `render-profile.json`. Both now bind the current profile SHA-256 `88e410311435ab6bcfbd70ab0a2cea73ffe304e3ce2876d241d25ea38cc5d5cd` to source-surface freeze SHA-256 `8a4f04238c68c40e59464e76a7911f0bee9488e09daab9f8772b1af970768d23`, report `rendering_profile_frozen=true`, and retain `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, `rendering_equivalence_claimed=false`, composition/body/admission/FantLab/M2 gates closed.
- Historical render-surface capture status is represented separately as `rendering_profile_frozen_at_surface_capture=false`; it is not used as the current profile state.
- Extended provenance tests to require the profile manifest, SHA binding and current profile/renderer boundary in both structured records.

PR #176 remains Draft after these authored repairs. A fresh exact-head independent review is still required before Ready/merge; this repair run does not self-approve the substantive change.

## Benchmark / public movement

- **Benchmark:** no movement; M2 remains **0/5** source-matched works.
- **Public representation:** public prose and canonical structured provenance now agree that the fail-closed decision profile is frozen while renderer semantics, literary body, >=300k admission and FantLab identity remain unproven.

## Handoff

Wait for all PR-triggered workflows on the repaired final exact head to settle, then independently re-read the complete diff and verify the two prior blockers are closed. If clean, record review as COMMENT rather than self-approval and only then decide Ready/merge. Literary-body composition remains non-executable while template/reference semantics are unresolved.
