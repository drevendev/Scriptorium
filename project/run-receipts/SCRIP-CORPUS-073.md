# SCRIP-CORPUS-073 run receipt

## Selection

- Mode: corpus / provenance research within the P2 SCRIP-CORPUS continuation.
- Base: `master@7865ab5cfaf3da570eef5f879f42f98ac187f664`.
- Issue: #235.
- Pull request: #236 (Draft; authored this run, independent later review required).
- Reason: SCRIP-CORPUS-072 established that the exact frozen Perelman PDF has no internal `/PageLabels`; canonical state names exact-carrier facsimile evidence as the next admissible mapping route.

## Research evidence

- The current Wikimedia Commons PDF surface was re-checked on 2026-09-23 and still reports 223 pages, 28,168,847 bytes and SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, matching the provider identity already frozen by Scriptorium. The repository's independently established exact-carrier SHA-256 remains `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.
- Commons still identifies the current file revision as 3 September 2021 and notes that pages 193–194 were added; this unit does not use that note to infer carrier-page equivalence or literary selection.
- Manual visual inspection of the 500-pixel Commons PDF preview directly observed only the following carrier pages:
  - page 4: preface surface; no printed page label visibly observed;
  - page 5: apparently blank surface; no printed page label visibly observed;
  - page 6: table-of-contents surface; printed label `V` directly visible;
  - page 8: table-of-contents surface; printed label `VII` directly visible;
  - page 9: front-matter illustration; no printed page label visibly observed.
- Provider page locators are retained in the machine artifact. Preview image bytes are not frozen or committed.
- Carrier page 7 was not retained as an observation and is not inferred to be `VI`. Carrier page 9 is not inferred to be `VIII`, and the numbered-body start is not inferred to be carrier page 10.

## Produced

- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-frontmatter.json` — source-free partial facsimile evidence; physical SHA-256 `12bf560c02b66275a30331cf0274a410041ac916ef21c4ff840d0e55524b7ff8`.
- `tests/test_perelman_pdf_facsimile_frontmatter.py` — freezes artifact bytes, exact carrier identity, directly observed page set, source-free payload boundary and downstream gate closure.
- `corpus/candidates/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-frontmatter.md` — public explanation of the anchors and the fail-closed mapping boundary.
- `project/CHANGELOG.d/SCRIP-CORPUS-073.md`, this receipt and durable state handoff.

## Verification

- Repository-facing evidence was kept source-free: no PDF bytes, preview images, OCR, hidden text or literary prose were committed.
- The authored static artifact digest was computed from canonical UTF-8 JSON bytes as `12bf560c02b66275a30331cf0274a410041ac916ef21c4ff840d0e55524b7ff8` and is asserted by the focused regression.
- Draft PR #236 must be judged only after GitHub checks settle on its final exact head. This authoring run does not self-approve or merge it.

## Decision / gates

- `bibliographic_to_carrier_mapping_complete=false`
- `body_start_carrier_page_proved=false`
- `mapping_may_be_extrapolated_between_observed_anchors=false`
- `literary_page_selection_bound=false`
- `pdf_djvu_page_equivalence_verified=false`
- `canonical_extraction_carrier_selected=false`
- `ocr_correctness_verified=false`
- `literary_body_frozen=false`
- `minimum_300k_proved_from_frozen_body=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `m2_parity_admissible=false`
- M2 remains 0/5.

The next independent review should re-read every changed file, recompute the committed artifact SHA-256, confirm the exact retained anchors against the linked Commons previews and verify all final-head checks. If that review passes, merge with expected-head protection. After merge, a later normal-flow unit may inspect the numbered-body transition and tail/end-matter anchors; it must not infer missing pages from the current partial set.
