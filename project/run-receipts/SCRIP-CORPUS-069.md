# SCRIP-CORPUS-069 run receipt

## Selection

- Mode: corpus / provenance durability recovery within the P2 SCRIP-CORPUS continuation.
- Base: `master@35a67871f086ba9fde017f8b69b29ade1434e6b5`.
- Issue: #227.
- Draft PR: #228.
- Reason: reviewed SCRIP-CORPUS-068 probe evidence was machine-readable only as a seven-day Actions artifact; repository prose retained its digest/summary but not the exact canonical JSON.

## Produced

- Added canonical source-free `darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json` with embedded probe SHA-256 `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- Added focused freeze regressions that recompute the embedded digest, assert exact `Модуль:String@3684569` identity and source-free payload, and keep semantic/downstream gates closed.
- Updated the exact-revision CI probe to regenerate the source-free JSON from transient Wikisource source, delete the raw response, and byte-compare the derived JSON with the committed canonical freeze before upload.
- Updated public provenance and `STATE_AND_QUEUE` to hand off independent review.

## Local deterministic verification

Before GitHub write, the canonical JSON was reconstructed directly from the reviewed SCRIP-CORPUS-068 builder contract and evidence summary. Recomputing `probe_sha256` over canonical JSON excluding the digest field produced exactly `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`, matching the independently reviewed workflow artifact. No source-text field is present.

## Gates / non-claims

- `module_string_identity_bound=false`
- `semantic_dependency_closure_proved=false`
- `dependency_closure_complete=false`
- forced/non-forced outputs remain unverified
- renderer/body/>=300k/FantLab/M2 gates remain closed
- M2 remains 0/5

This run does not claim historical transclusion provenance, recursive semantic closure, renderer equivalence or FantLab parity. Independent exact-head judgement is required before merge. The exact handoff head and settled check evidence are recorded on Draft PR #228 rather than self-approving this authored change.
