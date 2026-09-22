# Run receipt — SCRIP-CORPUS-053

Date: 2026-09-22
Mode: corpus / provenance
Issue: #193 (open)
Pull request: #194 (Draft; authored, independent review pending)
Base at selection: `6027bda0bfcf5a596260fe9f49214a98773e882c`

## Selection

The repository had no open pull requests or issues, no recovery row, and `STATE_AND_QUEUE.md` exposed only P2 `SCRIP-CORPUS continuation`. The retained Perelman 1913 popular-science candidate already had an independently frozen exact Commons PDF and a fail-closed OCR/body promotion contract, but Commons also exposes a materially different DjVu carrier for the same bibliographic edition. Freezing that companion binary is a bounded provenance improvement that can inform later OCR/carrier decisions without prematurely selecting pages, trusting embedded text, or claiming a literary body.

## Fresh provider evidence

On 2026-09-22, Wikimedia Commons presented the DjVu as another version of **Занимательная физика. Кн. 1. СПб., Изд-во П. П. Сойкина, 1913** and public-domain material. The current DjVu file surface reported:

- 218 pages;
- 2,982,171 bytes;
- SHA-1 `05c29d01c5dde91bfcfbb6b7ea7f0ea3dba43a12`;
- current file-history revision timestamp `2021-08-24T09:31:00Z`.

The Commons PDF description separately states that pages 193–194 were added to the PDF because they were missing from the DjVu. Scriptorium treats this and the same-edition link as provider assertions only. Neither the 223-vs-218 page-count difference nor the page note is accepted as proof of exact page mapping or textual equivalence.

## Production

Added `scriptorium/perelman_djvu_identity.py`, focused fail-closed tests and a dedicated hosted workflow. The identity contract records only source-free carrier metadata and cryptographic identity. It binds the companion relationship to the already frozen PDF SHA-256 `3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61` while requiring all of the following to remain false:

- `page_equivalence_verified`;
- `embedded_text_or_ocr_inspected`;
- `canonical_ocr_extraction_carrier_changed`;
- OCR/body freeze, >=300k admission, diagnostics and M2 gates.

No DjVu bytes, page images, embedded text, OCR text or literary source prose are committed or uploaded.

## Hosted capture evidence

Initial PR head `1706e8e499017bdde4858d1db9c5e2fba58b22fa` triggered dedicated run `35669820954`, job `106563543200`. The job completed `success`: it ran focused tests, transiently streamed the exact current Commons DjVu, reproduced the provider byte count and SHA-1, and computed Scriptorium SHA-256:

`f1db2166ae0cb5d420aad445f00d90cb09ac0b97e19fc8ece16d9b8ecf9e2462`

Source-free artifact `10670888071` was downloaded independently. GitHub reports, and the downloaded ZIP independently reproduces, SHA-256 `62d2c752825c9a47dc76ee8234fa588e8304175786fbad1e1e13f8f36d7ad6a3`; the ZIP is 1,150 bytes and contains exactly `perelman-entertaining-physics-book1-1913-ru.djvu-identity.capture.json`. Inspection confirmed the artifact contains only metadata/digests/gate booleans and no source payload.

The captured identity was then frozen as `corpus/candidates/source-edition-traces/perelman-entertaining-physics-book1-1913-ru.djvu-identity.json`, and the workflow was changed from capture mode to exact replay against that committed receipt.

## Public/provenance integration

Updated the Perelman candidate page and machine provenance trace to expose both carrier identities while keeping their relationship narrow. The public surface now states that Commons asserts the same bibliographic edition but Scriptorium has not proved exact PDF↔DjVu page equivalence and has not inspected or trusted embedded DjVu OCR/text. The independently reviewed OCR/body promotion contract v1 remains unchanged, with canonical SHA-256 `f709f2fd298252c3edaf8eaf04fc53955186d48df1f2c2b24d1962d1729ee7e5`, and remains bound to the frozen PDF scan.

Focused provenance integration tests now bind the public/machine claims to the exact committed DjVu receipt and reject any accidental carrier/equivalence/gate promotion.

## Gate judgement

Advanced:

- exact source-free binary identity for the current Commons DjVu companion;
- independently replayable provider byte-count/SHA-1 and Scriptorium SHA-256 evidence;
- public and machine-readable carrier relationship with fail-closed non-equivalence semantics.

Not advanced:

- exact PDF↔DjVu page mapping/equivalence;
- suitability or identity of any embedded DjVu text/OCR layer;
- canonical extraction-carrier selection beyond the existing PDF-bound v1 contract;
- literary-page selection;
- renderer/rasterizer or OCR engine/language-data identity/settings;
- literary-body count/digests;
- >=300,000-character calibration admission;
- work-specific FantLab linguistic-analysis/input identity;
- diagnostics, parity or M2. M2 remains 0/5.

## Handoff

Draft PR #194 remains intentionally unmerged because this wake authored the substantive companion-carrier freeze. A later independent wake must review the exact final head after hosted checks settle, independently inspect the exact-replay evidence and source-free artifact contents, and only then decide Ready/merge.
