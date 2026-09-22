# Run receipt — SCRIP-CORPUS-059

- **Unit:** SCRIP-CORPUS-059 — Perelman 1913 DjVu hidden-text inspection
- **Issue:** #205 (open)
- **Pull request:** #206 (Draft; independent later review required)
- **Base:** `master@de7152af6cc8fab3cb34f46e432feb6b1d3b0ab1`
- **Authored semantic handoff head before this receipt:** `9a50394106486141647fd1241cb1dbc8518c61e7`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This unit advances the retained early-20th-century popular-science candidate *Entertaining Physics, Book 1* (1913) by inspecting the hidden-text layer in its already frozen Commons DjVu companion. It adds `scriptorium-perelman-1913-djvu-hidden-text-v1`, focused regressions, a dedicated hosted replay workflow, a canonical source-free diagnostic, synchronized aggregate provenance and candidate documentation, changelog/state updates, and this receipt.

The extraction path deliberately remains evidence-only. It re-verifies the exact 2,982,171-byte DjVu carrier / SHA-1 `05c29d01c5dde91bfcfbb6b7ea7f0ea3dba43a12` / SHA-256 `f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462` before running Ubuntu 24.04 `djvulibre-bin` 3.5.28-2ubuntu0.24.04.2 / `djvutxt`. DjVu bytes and extracted hidden text are transient only and are not committed or uploaded as evidence.

## Hosted capture evidence

Initial capture run `35723749909` at authored head `b02426746f41b09f3f06c847b39ec98d08d3c042` completed `success`. Its focused tests, exact-carrier retrieval/identity verification, hidden-text extraction, closed-gate validation and source-free artifact upload all passed. Artifact `10691914472` was 1,152 bytes with GitHub archive digest SHA-256 `f676def2aab3f502a2c46328d40781347d840dac070ed6a1184cfb6c01735753` and contains only the source-free diagnostic JSON.

The hosted observation is now frozen in `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.djvu-text-layer.json`. The dedicated workflow was then tightened to regenerate that diagnostic from the exact carrier and require byte-for-byte equality with the committed JSON on every relevant PR head.

After synchronizing the aggregate provenance trace and public page, exact-head DjVu-identity run `35724498267` exposed one stale wording assertion in `test_public_candidate_page_exposes_identities_without_source_payload`: it expected the old phrase `does **not** change` while the revised page states that the DjVu evidence `do **not** change the contract's canonical PDF extraction carrier`. All other 13 tests in that job passed. The assertion was repaired to test the current semantic boundary rather than obsolete grammar; no carrier, diagnostic or gate evidence changed. Final exact-head workflows must re-run before review handoff is considered settled.

## Diagnostic observations

The exact frozen DjVu yields:

- all-pages hidden-text UTF-8 bytes: **583,825**;
- all-pages Unicode characters: **326,992**;
- `scriptorium-text-v1` normalized characters: **326,992**;
- raw UTF-8 SHA-256: **`4c9235a78b40ea4737ec4463c1e772727cb31198509d05a24472e8d9075319b8`**;
- normalized UTF-8 SHA-256: **`4c9235a78b40ea4737ec4463c1e772727cb31198509d05a24472e8d9075319b8`**;
- DjVu pages with non-empty `djvutxt` output: **218/218**;
- pages without output: **none**;
- SHA-256 of the exact 218-element per-page UTF-8 byte-count vector: **`1ee1043c36f31cfd7d5a5595a67796d7d27112e984eaeddc51b3c48a268953bd`**.

These values describe the entire carrier text layer, not a selected literary body. Front/back matter or apparatus may be included and OCR correctness has not been established. The existing source-free OCR/body promotion contract remains bound to the PDF carrier; this unit does not change the canonical extraction carrier.

## Gates / handoff

- `page_equivalence_to_pdf_verified=false`
- `literary_page_selection_frozen=false`
- `canonical_ocr_extraction_carrier_changed=false`
- `literary_body_count_and_digests_frozen=false`
- `minimum_300k_proved_from_frozen_body=false`
- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5**.

Draft PR #206 must be judged by a later independent wake at its exact final head. That review should inspect every changed file/thread, confirm the unchanged base, require all exact-head hosted workflows to settle successfully, and only then decide Ready/merge. The next candidate-specific promotion step after this PR is separate: deliberately select/bind a carrier and exact literary pages under a new independently evidenced contract version before any >=300k admission claim.
