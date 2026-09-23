# SCRIP-CORPUS-071 run receipt

## Selection

- Mode: corpus / provenance research within the P2 SCRIP-CORPUS continuation.
- Base: `master@af10a32a98030c4a82a9c0f36b0e612024bc670b`.
- Issue: #231 (closed completed after merge).
- Pull request: #232 (independently reviewed; squash-merged).
- Reason: Perelman 1913 is a retained public-domain popular-science candidate whose next extraction gate requires exact page-label/facsimile mapping. SCRIP-CORPUS-061 already proved that bibliographic page-count arithmetic is insufficient, so the current first-party Wikisource/Commons index surface materially changes which mapping route is executable.

## Research observation

- Re-read the current Wikimedia Commons PDF and DjVu file surfaces on 2026-09-23.
- The PDF surface currently carries category `PDF files in Russian without index page in Russian Wikisource`.
- The DjVu surface currently carries category `DjVu files in Russian without index page in Russian Wikisource`.
- This is dated current-surface evidence only. It does not prove historical absence of a Russian Wikisource Index page or prevent one from being created later.

## Produced

- Added source-free machine evidence `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.wikisource-index-surface.json`.
- Canonical payload SHA-256 excluding the self-digest field: `46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77`.
- The machine artifact is bound to the already frozen PDF SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61` / 223 pages and DjVu SHA-256 `f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462` / 218 pages.
- Added public companion `corpus/candidates/perelman-entertaining-physics-book1-1913-ru-wikisource-index-surface.md`.
- Added this receipt and changelog fragment; final review/merge bookkeeping is durable in repository state, Issue #231 and PR #232.

## Verification

- Authored-unit verification independently recomputed the canonical payload digest from the source-free object with the `canonical_payload_sha256` field removed, sorted JSON keys, UTF-8 and compact separators; it matched `46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77`.
- Independent exact-head review `5292600215` later re-read all 5 changed files at `c10dd031d375d22d13ccad116f38429d4a5bafce` against unchanged `master@af10a32a98030c4a82a9c0f36b0e612024bc670b` and found no merge blocker or open review thread.
- The review independently recomputed the canonical payload SHA-256 as `46803a34fb018f204588f798aca9b928393c37b54518f8adba36b790d6c33d77` and freshly re-checked both first-party Commons surfaces; the same current categories remained visible.
- GitHub returned 5 PR-triggered workflow runs for exact head `c10dd031d375d22d13ccad116f38429d4a5bafce`; all 5 completed with `success`.
- PR #232 was marked Ready and squash-merged with expected-head protection as `dc7a24d6a92a340afe6e6fcec037d8f53b44c96a`, automatically closing Issue #231 as completed.

## Decision / gates

- A current Russian Wikisource ProofreadPage Index/page-label surface is not established for either frozen carrier and must not be assumed.
- Page-count arithmetic remains rejected as a carrier-page selector.
- Next evidence: exact-carrier facsimile/internal page labels, or a directly identified first-party Index surface if one later exists.
- `pdf_djvu_page_equivalence_verified=false`
- `literary_page_selection_bound=false`
- `canonical_extraction_carrier_selected=false`
- `ocr_correctness_verified=false`
- `literary_body_frozen=false`
- `minimum_300k_proved_from_frozen_body=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `m2_parity_admissible=false`
- M2 remains 0/5.

SCRIP-CORPUS-071 is complete and independently reviewed. `STATE_REVISION=256`; normal-flow selection resumes from the P2 SCRIP-CORPUS continuation.
