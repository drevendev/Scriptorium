# Run receipt — SCRIP-CORPUS-085

Status: REVIEW_PENDING

## Orientation

- Authoring identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; push/triage permission available.
- Exact authoring base: `82e88eb2d9045b199d595fa96d9cab9260cf6328`.
- Issue: #259.
- Draft PR: #260.
- Semantic evidence head: `272c00c7c47f7a1506a826591b7941e1d49ad05e`.

## Produced

One bounded Perelman 1913 exact-PDF facsimile audit across three previously unobserved mid-body windows:

- carrier pages 59–61;
- carrier pages 109–111;
- carrier pages 159–161.

The existing hosted workflow was extended to reverify the exact 223-page Commons PDF before rendering those windows. It checks 28,168,847 bytes, SHA-1 `3c616f547ff283a2cafd1ac26b448a8e8013f648`, and SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`; PDF bytes are deleted before artifact upload.

Initial capture run `36016017921` at head `56f2e0bec65bc65f9b1d5c16f855da8e8f430ce4` completed successfully. Artifact `10814104285` was downloaded during authoring; its ZIP SHA-256 independently recomputed to `2eb64d55fd61f4cb26a425070759bc4ffe7f2e2c8be6d36631550ecbf7c21d71`, matching GitHub metadata.

## Direct visual observations

Manual visual inspection was performed on the transient exact-carrier JPEGs, not OCR.

Direct visible folios:

- carrier 59 → printed 50;
- carrier 61 → printed 52;
- carrier 109 → printed 100;
- carrier 110 → printed 101;
- carrier 111 → printed 102;
- carrier 159 → printed 150;
- carrier 160 → printed 151;
- carrier 161 → printed 152.

Carrier page 60 has **no directly visible printed folio**. It is deliberately not retained as printed 51.

Every directly visible label in the three windows is compatible with `carrier_page - printed_page = 9`, but this is retained only as a sampled mapping hypothesis. No global offset or unobserved-page mapping is promoted.

The exact per-image SHA-256 values and source-free observation rows are frozen in `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.pdf-facsimile-midbody.json`. Its physical SHA-256 is `26291c4add9272fa2572425597deb99ec8b431cffb374119c134867aca9e02ea`. The downloaded `rendered-pages.sha256` manifest itself independently hashes to `33457b4afaeed309fa6c604bfb0214f4be85979289033ed272f53f978ce30518`.

## Verification

- Exact carrier retrieval/hash verification: success in hosted capture run `36016017921`.
- Transient render artifact upload: success.
- Artifact ZIP digest independently recomputed: match.
- All nine new page images manually inspected.
- Focused retained regression: **5/5 pass** locally before commit.
- PR remains Draft for a later independent exact-head judgement.

## Evidence boundary

This unit does **not** prove:

- a complete bibliographic-to-carrier page map;
- a global carrier-minus-printed offset;
- the missing folio for carrier page 60 or any other unobserved page by interpolation;
- PDF↔DjVu page equivalence;
- canonical extraction-carrier selection;
- OCR correctness;
- literary-page selection or literary-body identity;
- selected-body `>=300k`;
- FantLab analyzer-input identity;
- diagnostic readiness, M2 admissibility, calibration admission, or parity.

M2 remains 0/5. No benchmark movement occurred.

## Handoff

A later independent run must re-read all PR #260 changed files against authoring base `82e88eb2d9045b199d595fa96d9cab9260cf6328`, verify the source-free evidence and exact-head checks, and only then mark Ready / merge with expected-head protection if clean. Keep page 60 uninterpolated and keep the global-offset/body/FantLab/M2 gates closed.
