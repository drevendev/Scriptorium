# Run receipt — SCRIP-CORPUS-086

Status: REVIEW_PENDING

## Exact recovery state

- Base: `cde1a4e577a2611a0ea2bf7b3930ca4382f5feef`.
- Canonical branch: `scriptorium-corpus-086-source-identities`.
- Issue: #261.
- Draft PR: #262.
- Authoring identity: `andy-zen-dev`.
- Verified semantic/test head for this bounded unit: `ca4b2654318f74d7fdd5042e6713fab86cc123ba`.
- Exact-head verification: 26/26 pull-request-triggered workflow runs completed successfully; no submitted reviews and no review threads were present.
- Unit: source-free exact revision identity freeze for the 20 retained Bulgakov chapter pages while preserving the 1–11 / 12–20 mixed-source partition.

## Produced

The branch now contains:

- source-free current-revision identity capture requesting page ID, revision ID, UTC timestamp and MediaWiki SHA-1 only;
- strict positive-integer identity validation that rejects booleans;
- identity-only pinned replay with no literary content request and fail-closed page ID / revision ID / timestamp / SHA-1 checks;
- exact 20-title provider inventory validation;
- closed four-field provider identity mappings;
- explicit nine-field persisted page rows;
- a closed top-level manifest envelope with provider/source URL/legal-basis validation;
- exact composition and capture-scope checks;
- deterministic offline regressions covering the source partition, identity drift, source-free replay, open-schema rejection and SHA-1 canonicalization.

## Verification boundary

The authoring run re-read the post-write implementation and test blobs from GitHub and confirmed all intended schema/replay guards are present. Draft PR #262 was opened successfully.

Exact-head verification was completed on `ca4b2654318f74d7fdd5042e6713fab86cc123ba`: all 26 pull-request-triggered workflow runs completed successfully, with no submitted reviews and no review threads. This recovery update changes bookkeeping only; the resulting documentation-only PR head still requires a later independent exact-head judgement before Ready/merge.

No live 20-row provider capture is claimed in this receipt, and no literary prose is committed.

## Evidence boundary

Literary-body extraction, composite identity, single-edition equivalence, FantLab analyzer-input identity, diagnostics, benchmark movement, M2 admission and parity remain closed. M2 remains 0/5.

## Exact reconciliation

Recovery remains REVIEW_PENDING. Canonical bookkeeping is reconciled to verified semantic/test head `ca4b2654318f74d7fdd5042e6713fab86cc123ba` and its 26/26 successful PR-triggered workflows. Because this reconciliation itself advances the PR with documentation-only commits, a later independent wake must re-read PR #262 on its new exact head and inspect fresh checks/reviews/threads before any Ready/merge decision. Authoritative 20-page identity-only provider capture/replay is a separate bounded production unit and must not be conflated with this recovery/review handoff.
