# SCRIP-CORPUS-074 run receipt

## Selection

- Mode: corpus / provenance research within the queued P2 SCRIP-CORPUS continuation.
- Base: `master@2fe76aac43e65d4d8d089901fc8842e0713970f4`.
- Issue: #237.
- Draft pull request: #238.
- Reason: canonical state explicitly named the Perelman numbered-body transition and tail/end-matter exact-carrier facsimile anchors as the next admissible mapping unit after SCRIP-CORPUS-073.

## Exact-carrier render evidence

- The review workflow re-downloaded the frozen Commons PDF and failed closed unless it matched **223 pages / 28,168,847 bytes**, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.
- Authoring workflow run `35905965911` checked out exact head `1b4b929b3e2d5816edf49dfdf46b22e8bd6ae4fa` and completed `success`.
- Ubuntu 24.04.5 installed `poppler-utils 24.02.0-1ubuntu9.9`; `pdftoppm` reported version `24.02.0`.
- The workflow rendered only carrier pages 9–13 and 217–223 at 120 dpi JPEG, removed the PDF, retained a SHA-256 manifest, and uploaded a one-day transient artifact (`10771380564`, ZIP digest `sha256:ae4ac27bca4d1e2ffc0d75df3b9dab155d7a946a86b70b9a84b60894b4767fed`).
- The rendered-page manifest itself is bound by SHA-256 `dedd68c23385b457e9630404022757b1f5a6a4bc5cfb6e74c364e93c28470fec`.

## Direct observations

Only directly visible labels/surfaces were retained:

- carrier 9: front-matter illustration; no printed label visible;
- carrier 10: Chapter I body start; printed `1`;
- carrier 11: body text; printed `2`;
- carrier 12: body text with diagrams; printed `3`;
- carrier 13: body text with diagram; printed `4`;
- carrier 217: body text with figure; printed `208`;
- carrier 218: body text with figure; printed `209`;
- carrier 219: body text; printed `210`;
- carrier 220: body text; printed `211`;
- carrier 221: unnumbered concluding body text with an end ornament; no printed label visible;
- carrier 222: publisher advertisement; no printed label visible;
- carrier 223: publisher advertisement; no printed page label visible. A handwritten/stamped `30356` is visible and explicitly not treated as a page label.

## Produced

- `.github/workflows/perelman-pdf-facsimile-review.yml` — exact-carrier hash verification plus bounded transient render/review artifact.
- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-transition-tail.json` — canonical source-free machine evidence; physical SHA-256 `d518b8f3a00511cf3b7c0199923705c0df9339004be0d759198a5f72cb5a79e5`.
- `tests/test_perelman_pdf_facsimile_transition_tail.py` — freezes artifact bytes, carrier identity, exact observed page set, narrow boundary advancement, source-free constraints and downstream gate closure.
- `corpus/candidates/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-transition-tail.md` — public companion.
- `project/CHANGELOG.d/SCRIP-CORPUS-074.md`, this receipt, and canonical state handoff.

## Decision / gates

- `body_start_carrier_page_proved=true`, page 10.
- `numbered_body_end_carrier_page_proved=true`, page 220 / printed 211.
- `tail_boundary_directly_observed=true`: page 221 is unnumbered concluding body text; pages 222–223 are advertisements.
- `bibliographic_to_carrier_mapping_complete=false`.
- `complete_numbered_body_range_proved=false`.
- `mapping_may_be_extrapolated_between_observed_anchors=false`.
- `literary_body_end_carrier_page_proved=false` and `literary_page_selection_bound=false`.
- `pdf_djvu_page_equivalence_verified=false`.
- `canonical_extraction_carrier_selected=false`.
- `ocr_correctness_verified=false`.
- `literary_body_frozen=false`.
- `minimum_300k_proved_from_frozen_body=false`.
- `fantlab_source_edition_match=unknown`.
- `diagnostic_ready=false`.
- `m2_parity_admissible=false`; M2 remains 0/5.

The direct endpoints happen to be compatible with a simple offset across the numbered body, but this run deliberately does not infer the unobserved interior. A later independently reviewed unit should audit internal anchors, especially around the PDF history's later-added printed pages 193–194, before binding a complete carrier map or extraction contract.

Draft PR #238 remains REVIEW_PENDING. The exact final authored handoff head and exact-head workflow settlement are recorded in the PR conversation after durable-state writes complete.
