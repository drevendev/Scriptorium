# SCRIP-CORPUS-075 run receipt

## Selection

- Mode: corpus / provenance research within the queued P2 SCRIP-CORPUS continuation, followed by the required later-wake review/recovery unit.
- Base: exact `master@a075cec66a18ab5e9cd97a5a117a7bbab4395ae0`.
- Issue: #239 (closed completed after merge).
- Pull request: #240 (independently reviewed at exact head `75cd2928f00dded300028525cd13e869c4789fb0`; squash-merged as `8e3c598c563fb5cff9028006ccbbd4a1cc18dba5`).
- Reason: canonical state explicitly named a bounded interior audit around the PDF history's restored printed pages 193–194 as the next useful Perelman mapping unit after independently reviewed SCRIP-CORPUS-074.

## Exact-carrier render evidence

- The existing Perelman review workflow was extended rather than duplicated. It re-downloads the frozen Commons PDF and fails closed unless it matches **223 pages / 28,168,847 bytes**, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.
- Authoring workflow run `35918820460` completed `success` after rendering the bounded interior window carrier pages 199–206 at 120 dpi and deleting the PDF before artifact upload.
- The authoring one-day review artifact is `10775613969`; independent download recomputed ZIP SHA-256 `d543e7cc0374a8d89d7a820df6fd525438121da38270e62a084d1f8882bbfebd`.
- The retained render manifest SHA-256 is `ad09df0a7583092dc2ddf71af25c0f0d014cf5dfe680d806a2962a9243cef667`.

## Direct observations

Only directly visible printed labels were retained:

- carrier 199 -> printed `190`;
- carrier 200 -> printed `191`;
- carrier 201 -> printed `192`;
- carrier 202 -> printed `193` (restored-page region);
- carrier 203 -> printed `194` (restored-page region);
- carrier 204 -> printed `195`;
- carrier 205 -> printed `196`;
- carrier 206 -> printed `197`.

This proves a locally continuous numbered sequence across the targeted restored-page seam and a directly observed `carrier - printed = 9` relation only inside the audited window 199–206. It does not prove every unobserved interior page and does not authorize a global offset rule.

## Produced

- `.github/workflows/perelman-pdf-facsimile-review.yml` — extended exact-carrier review workflow with the bounded interior window and future interior regression replay.
- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-interior.json` — canonical source-free machine evidence, physical SHA-256 `b19be5e8b3fe83546dd65a73770b91f71124b13c709de8142ead29cb78fbc319`.
- `corpus/candidates/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-interior.md` — public companion.
- `tests/test_perelman_pdf_facsimile_interior.py` — freezes artifact bytes, exact carrier identity, all eight direct anchors, restored-page binding, local-only offset scope and downstream gate closure.
- `project/CHANGELOG.d/SCRIP-CORPUS-075.md`, this receipt, and canonical state handoff.

## Independent review / verification

- Review `5297230518` re-read all 7 changed files and Issue #239 on exact PR head `75cd2928f00dded300028525cd13e869c4789fb0` against unchanged `master@a075cec66a18ab5e9cd97a5a117a7bbab4395ae0`; no open review thread or blocker was found.
- All **23/23** PR-triggered workflow runs returned for the exact reviewed head completed `success`.
- Dedicated exact-head run `35919567256` explicitly checked out `75cd2928f00dded300028525cd13e869c4789fb0`, reverified the frozen PDF, rendered transition/interior/tail review pages, replayed retained source-free regressions, deleted the PDF before upload, and produced one-day artifact `10776776917` with GitHub digest `sha256:df3fd2abb535fb0b6e1d7c13eb622dfef054671748492cba3d7a0d054a085480`.
- Independent download recomputed that exact ZIP SHA-256 and verified every rendered JPEG against `rendered-pages.sha256`. Visual inspection of interior pages confirmed `199–206 -> 190–197`, specifically `202 -> 193` and `203 -> 194`, with no evidence supporting a broader extrapolation.
- PR #240 was marked Ready and squash-merged with expected-head protection at 2026-09-23T21:53:52Z as `8e3c598c563fb5cff9028006ccbbd4a1cc18dba5`, automatically closing Issue #239 completed.

## Decision / gates

- `restored_printed_pages_directly_observed=true`: printed 193->carrier 202 and printed 194->carrier 203.
- `local_window_continuity_directly_observed=true` for carrier 199–206 / printed 190–197.
- `local_carrier_minus_printed_offset_observed=9`, scoped only to that audited window.
- `global_carrier_minus_printed_offset_asserted=false`.
- `bibliographic_to_carrier_mapping_complete=false`.
- `complete_numbered_body_range_proved=false`.
- `mapping_may_be_extrapolated_between_observed_anchors=false`.
- `literary_page_selection_bound=false`.
- `pdf_djvu_page_equivalence_verified=false`.
- `canonical_extraction_carrier_selected=false`.
- `ocr_correctness_verified=false`.
- `literary_body_frozen=false`.
- `minimum_300k_proved_from_frozen_body=false`.
- `fantlab_source_edition_match=unknown`.
- `diagnostic_ready=false`.
- `m2_parity_admissible=false`; M2 remains 0/5.

The local +9 relation is now independently reviewed for the bounded 199–206 window only. Any later complete-map claim still requires additional direct evidence or a separately justified proof; the observed relation must not be interpolated across unobserved pages by default.

SCRIP-CORPUS-075 is complete. Normal-flow P2 corpus/provenance selection may resume.
