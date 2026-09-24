## 2026-09-24 — Perelman 1913 broad mid-body facsimile anchors

- Selected SCRIP-CORPUS-085 / Issue #259 from the normal-flow corpus/provenance queue after confirming no interrupted open PR required recovery.
- Extended the exact-carrier Perelman facsimile workflow to render three new bounded mid-body windows: carrier pages 59–61, 109–111 and 159–161.
- Hosted capture run `36016017921` reverified the exact 223-page / 28,168,847-byte Commons PDF (`sha1:3c616f547ff283a2cafd1ac26b448a8e8013f648`, `sha256:3d87d22a42ad949654265e066f81211d7831e32c8b62b96c967cd4cd33e7ed61`) before rendering and completed successfully.
- Transient artifact `10814104285` was independently downloaded; its ZIP SHA-256 recomputed to GitHub's `2eb64d55fd61f4cb26a425070759bc4ffe7f2e2c8be6d36631550ecbf7c21d71`.
- Direct visual inspection retained source-free folio observations 59→50, 61→52, 109→100, 110→101, 111→102, 159→150, 160→151 and 161→152. Carrier page 60 directly has no visible folio and is deliberately not inferred as printed page 51.
- All directly visible sampled labels are compatible with carrier-minus-printed=9, but no global offset or unobserved mapping is promoted. This audit therefore strengthens the mapping hypothesis while also proving that visible folios are not a total per-page signal.
- Added source-free JSON evidence, public companion and five deterministic regressions. Evidence JSON physical SHA-256: `26291c4add9272fa2572425597deb99ec8b431cffb374119c134867aca9e02ea`; focused regression is 5/5 green.
- Draft PR #260 remains REVIEW_PENDING for independent exact-head judgement. Complete mapping, PDF↔DjVu equivalence, canonical carrier, OCR correctness, literary-body/>=300k, FantLab-input and M2/parity gates remain closed; M2 remains 0/5.
