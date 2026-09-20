# SCRIP-CORPUS-042 — Twelve Chairs gap composition membership

## Selection

- **Issue:** #171
- **Draft PR:** #172
- **Base:** `master@50864002a7ae2230124e15455f4a263eb05f743e`
- **Mode:** corpus / provenance, one bounded source-free decision unit
- **Reason selected:** no interrupted/review-ready work or failing-check recovery existed at orientation; the queue explicitly retained SCRIP-CORPUS continuation, and the immediately preceding reviewed gap audit left composition membership for nonempty pages 150/314 unresolved.

## Produced

- Added `scriptorium.twelve_chairs_gap_membership` and deterministic regression coverage.
- Added `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.gap-membership.json`.
- Bound the decision to the existing exact 410-Page sharded identity topology and the reviewed exact-revision gap audit.
- Froze pages 150/151/314/315 as **excluded from the current canonical-route composition surface** because the three frozen part routes do not transclude them.
- Preserved pages 150/314 as `nonempty_body_unclassified`; exclusion is a route-composition decision and does not semantically classify their printed-page content as non-literary. Pages 151/315 remain `no_transcluded_body`.
- Reconciled the dedicated public candidate page, source graph, structured edition trace, changelog fragment and durable queue state.

## Evidence boundary

The literary dependency inventory remains exactly **410** pinned Page revisions. No Page wikitext, OCR, rendered prose, PDF/image bytes or literary source text is committed by this unit. `literary_body_composition_frozen=false`, `page_body_rendering_profile_frozen=false`, `literary_body_count_and_digests_frozen=false`, `minimum_300k_proved=false`, `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`.

## Verification / handoff

The branch was authored from exact base `50864002a7ae2230124e15455f4a263eb05f743e`. The final content/state commit immediately preceding this receipt was `1cfe04c727de0bce5678189d2c0c3f341df64310`; creation of this receipt becomes the final authored head for the run. Draft PR #172 must remain Draft. A later independent wake must resolve and review that exact final head, confirm required CI has settled, re-check the gap-membership and existing Twelve Chairs provenance tests, and only then decide Ready/merge.

## Benchmark / public movement

- **Benchmark:** no movement; M2 remains **0/5** source-matched works.
- **Public representation:** the candidate page now distinguishes audited body presence from Scriptorium composition membership and exposes the source-free membership receipt without implying a frozen literary body.
