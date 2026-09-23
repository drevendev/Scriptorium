# SCRIP-CORPUS-072 run receipt

## Selection

- Mode: corpus / provenance research within the P2 SCRIP-CORPUS continuation.
- Base: `master@4b50ea3c39181ff8f1fd4a1fadc9d04a09237e67`.
- Issue: #233 (open).
- Pull request: #234 (Draft; independent later review required).
- Reason: the retained Perelman 1913 public-domain popular-science candidate had no admissible page mapping from bibliographic counts or current Russian Wikisource Index evidence. The next explicit repository-state route was exact-carrier facsimile/internal page-label evidence.

## Current research / tooling evidence

- qpdf's documented JSON contract exposes a top-level `pagelabels` array of `{index,label}` entries, and `--json-key=pagelabels` can isolate that surface.
- Ubuntu 24.04 currently packages qpdf 11.9.0; hosted CI pins package `qpdf=11.9.0-1.1ubuntu0.1`.
- The probe first verifies the exact frozen PDF identity: 28,168,847 bytes, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`.
- On that exact 223-page carrier, qpdf reports an empty `pagelabels` array: zero internal page-label entries.

## Produced

- `scriptorium/perelman_pdf_page_labels.py` — exact-carrier identity verification, bounded qpdf `pagelabels` capture, source-free canonical evidence and fail-closed validation.
- `tests/test_perelman_pdf_page_labels.py` — qpdf JSON shape/order/range tests, exact-carrier boundary tests, closed-gate/source-payload tests, and byte-for-byte committed-artifact regression.
- `.github/workflows/perelman-pdf-page-labels.yml` — pinned hosted replay that transiently retrieves the exact PDF, deletes it after inspection, regenerates the source-free evidence and requires byte equality with the committed artifact.
- `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-page-labels.json` — canonical source-free zero-label evidence; physical SHA-256 `16b4ba074221d7fa20cb044584886038989f43657988c6bd6b062774077915bd`.
- Updated public candidate documentation, durable state, this receipt and changelog fragment.

## Authored verification

- Hosted capture run `35884908615` checkout `ae9b809e999e8bdd35b281b98e5393276c396d6a`, installed the pinned qpdf package, passed 6/6 focused regressions, verified the exact PDF identity, reported `SCRIPTORIUM_PERELMAN_PAGE_LABEL_ENTRIES=0`, deleted transient PDF bytes and uploaded only the source-free JSON.
- Authoring-context replay `35885190135` repeated the dedicated job successfully on follow-up head `2d33ac5c28f5e99a6237e9df280ce43efc0a7da9`.
- Downloaded source-free capture bytes independently hash to `16b4ba074221d7fa20cb044584886038989f43657988c6bd6b062774077915bd`.
- Final exact-head CI settlement and independent judgement are deliberately left for the next review wake; this authored unit does not self-merge.

## Decision / gates

- `pdf_internal_page_labels_present=false`
- `internal_page_labels_establish_bibliographic_mapping=false`
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

The current exact PDF `/PageLabels` route is exhausted as a mapping authority. The next candidate-specific evidence is exact-carrier facsimile mapping (visible printed page numbers/front matter/end matter), optionally cross-checked against the frozen DjVu page map. SCRIP-CORPUS-072 is authored and recoverable in Draft PR #234; independent exact-head review remains required before merge.
