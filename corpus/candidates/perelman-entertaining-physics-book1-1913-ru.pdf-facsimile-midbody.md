# Perelman 1913 PDF — broad mid-body facsimile anchors

Candidate: `perelman-entertaining-physics-book1-1913-ru`

Status: **source-free observed facsimile evidence; review pending**

This companion records one bounded visual audit of three widely separated interior windows from the exact frozen 223-page Commons PDF. The workflow reverified the 28,168,847-byte carrier, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, and SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61` before rendering. No PDF bytes, page images, OCR, or literary source text are committed.

## Direct observations

| Carrier page | Visible printed page | Observation |
| ---: | ---: | --- |
| 59 | 50 | directly visible |
| 60 | — | no printed folio directly visible |
| 61 | 52 | directly visible |
| 109 | 100 | directly visible |
| 110 | 101 | directly visible |
| 111 | 102 | directly visible |
| 159 | 150 | directly visible |
| 160 | 151 | directly visible |
| 161 | 152 | directly visible |

Every **directly visible** printed folio in these windows is compatible with `carrier_page - printed_page = 9`. Carrier page 60 is deliberately **not** assigned printed page 51: the audit saw no visible folio there, so filling that value by arithmetic would turn an observation into an inference.

## Decision

The new anchors strengthen the working `+9` mapping hypothesis across the book interior, but they do **not** promote a global page-offset rule. In particular:

- the observed samples do not prove every unobserved carrier page;
- a visible printed folio is not present on every audited page;
- carrier page 60 remains an explicitly unlabelled observed page rather than an inferred mapping row;
- complete bibliographic-to-carrier mapping, the complete numbered-body range, PDF↔DjVu equivalence, canonical extraction-carrier selection, OCR correctness, literary-page selection/body identity, selected-body `>=300k`, FantLab analyzer-input identity, diagnostic readiness, M2 admissibility, and calibration admission remain closed.

A later complete-mapping unit must model unlabelled folios explicitly and gather enough direct evidence to justify any total map; it may not silently interpolate page 60 or other gaps.

## Reproducibility

Authoring capture workflow: `36016017921` at head `56f2e0bec65bc65f9b1d5c16f855da8e8f430ce4`.

Transient artifact: `10814104285`, GitHub digest `sha256:2eb64d55fd61f4cb26a425070759bc4ffe7f2e2c8be6d36631550ecbf7c21d71`, one-day retention. The downloaded ZIP was independently recomputed to the same SHA-256 during authoring.

The source-free render-manifest file had SHA-256 `33457b4afaeed309fa6c604bfb0214f4be85979289033ed272f53f978ce30518`. Exact per-image SHA-256 values are frozen in the JSON evidence artifact and deterministic regression.

Canonical machine evidence: [`source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-midbody.json`](source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-midbody.json).

Evidence JSON physical SHA-256: `26291c4add9272fa2572425597deb99ec8b431cffb374119c134867aca9e02ea`.
