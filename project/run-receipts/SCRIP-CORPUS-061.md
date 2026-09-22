# Run receipt — SCRIP-CORPUS-061

- **Unit:** SCRIP-CORPUS-061 — Perelman 1913 bibliographic pagination evidence
- **Issue:** #209 (closed completed on merge)
- **Pull request:** #210 (independently reviewed; squash-merged as `529678fb90f426f11857c952b630bfbc5200098e`)
- **Base:** `master@a73d4c230981c3d1e3af9e7694d28161e2ac8c97`
- **Reviewed head:** `d12130ff3d500f0ebb94edc6df87ec77ab2111d2`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This unit advances the retained early-20th-century popular-science candidate *Entertaining Physics, Book 1* (1913) by freezing source-free bibliographic pagination evidence before selecting literary carrier pages.

The machine-readable `scriptorium-perelman-1913-pagination-evidence-v1` artifact is bound to the already frozen 223-page PDF and 218-page DjVu identities. It records two deliberately distinct metadata surfaces:

- Russian State Library catalogue: **`VIII, 211, [1] с.`** for the 1913 P. P. Soikin Book 1;
- Google Books / Google Play Books: **212 pages** for the same 1913 Soikin title.

The unit changes the selection decision rather than merely collecting links: it rejects the inference `218 DjVu carrier pages - 212 displayed book pages = 6 non-literary carrier pages`. The RSL collation itself separates Roman-numbered preliminary pages, numbered pages and a bracketed unnumbered page, and neither bibliographic source maps those labels onto exact Commons carrier pages.

## Verification contract

- Focused standard-library regressions require the committed JSON to match the deterministic builder byte-for-byte.
- Validation pins both existing carrier identities and both bibliographic observations.
- Validation rejects page-count arithmetic as a literary-page selector, source-text/page-image payloads, carrier identity drift, bibliographic drift, literary-page/body promotion, >=300k admission, FantLab source matching and M2 promotion.
- A dedicated read-only PR workflow runs the focused checks on the pull-request head. Ordinary repository PR workflows remain part of the exact-head handoff.

No book text, page image, PDF/DjVu bytes or extracted hidden text is added by this unit.

## Independent review and merge

Independent review `5281085162` re-read all 8 changed files on exact head `d12130ff3d500f0ebb94edc6df87ec77ab2111d2` against unchanged `master@a73d4c230981c3d1e3af9e7694d28161e2ac8c97`, inspected the issue/handoff and found no open review thread or merge blocker. Fresh source verification independently reconfirmed the RSL `VIII, 211, [1] с.` collation and the Google Play Books 212-page display for the January 1913 Soikin title.

All **22/22** pull-request-triggered workflow runs associated with the reviewed head completed with `success`, including dedicated `Perelman 1913 pagination evidence` run `35750921690`. The PR was then marked Ready and squash-merged with expected-head protection as `529678fb90f426f11857c952b630bfbc5200098e`, automatically closing Issue #209 with state reason `completed`.

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

SCRIP-CORPUS-061 is complete. The next candidate-specific evidence step, when selected by normal-flow priority, is an exact facsimile/page-label mapping on a deliberately chosen frozen carrier. Page-count arithmetic remains inadmissible as a carrier-page selector.