# Run receipt — SCRIP-CORPUS-060

- **Unit:** SCRIP-CORPUS-060 — Perelman 1913 source-free DjVu page map
- **Issue:** #207 (closed completed)
- **Pull request:** #208 (independently reviewed; squash-merged as `00d3600c4f122a01d887677bd0da3ee5304bbebe`)
- **Base:** `master@eea64f4f58af5f3bd30c31a55eacc2f30bf32243`
- **Reviewed head:** `ba0a03d1a7ddf9ee4ce712a0b486645605e90eb4`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This unit advances the retained early-20th-century popular-science candidate *Entertaining Physics, Book 1* (1913) by freezing source-free page-level fingerprints for the already exact and text-bearing Commons DjVu. It adds `scriptorium-perelman-1913-djvu-page-map-v1`, focused regressions, a dedicated hosted replay workflow, the canonical 218-record source-free page map, synchronized public candidate documentation, changelog/state updates, and this receipt.

The extraction path re-verifies the exact 2,982,171-byte DjVu carrier / SHA-1 `05c29d01c5dde91bfcfbb6b7ea7f0ea3dba43a12` / SHA-256 `f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462` before pinned Ubuntu 24.04 `djvulibre-bin` 3.5.28-2ubuntu0.24.04.2 / `djvutxt` is invoked for each page. DjVu bytes, page images and extracted prose remain transient and are not retained.

## Capture / page-map evidence

Initial hosted capture run `35736515710` at authored head `936bbf85417b4fed46e8b66af538816b65efac98` completed the source-free page-map generation successfully. Artifact `10698026997` contained only the generated JSON map; its GitHub archive digest is SHA-256 `803fca693698f6f37be74bcbad28489d1598ce1b335c42b0e1c93c7d1f0b7ab0`.

A controlled authoring-only replay then froze that generated JSON onto the PR branch. The standing workflow was immediately tightened back to read-only checkout (`contents: read`, `persist-credentials: false`) and requires byte-for-byte equality between a fresh exact-carrier replay and the committed page-map JSON.

The canonical map contains **218 ordered page records**. Each record stores only a 1-based page number, UTF-8 byte count, Unicode character count, raw SHA-256, `scriptorium-text-v1` normalized character count and normalized SHA-256. The canonical ordered record-set SHA-256 is **`c7981219680bd549c58f69f12a66d393a23e457c526c3140e1da915f023c3246`**.

The page records sum to **583,825 UTF-8 bytes / 326,992 Unicode characters**, matching the already frozen all-pages SCRIP-CORPUS-059 observation. Per-page UTF-8 output ranges from **124 to 4,136 bytes**. This supplies exact page-level provenance for later page selection without publishing the book text.

## Independent review / merge

Independent review `5279744953` re-read all 8 changed files on exact head `ba0a03d1a7ddf9ee4ce712a0b486645605e90eb4` against unchanged `master@eea64f4f58af5f3bd30c31a55eacc2f30bf32243` and found no merge blocker or open review thread. All **21/21** PR-triggered workflow runs on that exact head were `completed/success`.

Dedicated run `35737181049` checked out the exact reviewed SHA and passed pinned DjVuLibre installation, focused page-map/text-layer/carrier regressions, exact-carrier replay, source-free closed-gate validation, byte-for-byte `cmp` with the canonical JSON, and source-free artifact upload. PR #208 was then marked Ready and squash-merged with expected-head protection as `00d3600c4f122a01d887677bd0da3ee5304bbebe`, automatically closing Issue #207 as completed.

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

The next candidate-specific step is separate and judgement-bearing: use facsimile/page-map evidence to choose and independently justify the exact literary-page sequence, then bind the chosen carrier/page selection and reproducible extraction profile under a new contract version before freezing literary-body counts/digests or considering >=300k admission.