# Run receipt — SCRIP-CORPUS-086

Status: RECOVERY_REQUIRED

## Exact recovery state

- Base: `cde1a4e577a2611a0ea2bf7b3930ca4382f5feef`.
- Recovery branch: `scriptorium-corpus-086-source-identities`.
- Current tested head: `7e491f025cf687b7010c9b28d23114890d6dd210`.
- Issue: #261.
- Authoring identity: `andy-zen-dev`.
- Unit: source-free exact revision identity freeze for the 20 retained Bulgakov chapter pages while preserving the 1–11 / 12–20 mixed-source partition.

## Produced

The branch contains a source-free capture/replay implementation in `scriptorium/white_guard_revisions.py` plus seven deterministic offline regressions in `tests/test_bulgakov_revisions.py`. The tests cover the 20-page chapter order, the 11/9 source-family partition, fail-closed capture scope, duplicate provider identities, source-partition drift, identity ordering and replay receipts that keep literary-body/FantLab gates closed.

Capture requests page ID, revision ID, UTC timestamp and MediaWiki SHA-1 only; literary prose is not serialized. Missing/redirected pages and malformed or duplicate identities fail closed.

## Verification

- The updated test module compiles successfully under Python syntax validation.
- No hosted PR checks exist for `7e491f0...` because Draft PR creation was blocked before GitHub accepted the mutation.
- No live 20-row provider manifest has been captured or claimed.

## Remaining blocker

Issue creation recovered and #261 now owns the unit. Git-object/file writes also work. Draft PR creation is still blocked by the available mutation path, and a follow-up attempt to add explicit composition-contract validation in the implementation was blocked before GitHub accepted it.

## Evidence boundary

No literary-body extraction/composition, composite identity, single-edition equivalence, FantLab analyzer-input identity, diagnostics, benchmark movement, M2 admission or parity is claimed. M2 remains 0/5.

## Exact reconciliation

Recovery still preempts new normal-flow work. Resume this exact branch, re-read #261 and the current head, add explicit fail-closed validation of `composition_contract`, obtain authoritative source-free provider identities for all 20 chapters through an explicit capture path, commit the manifest only after exact-revision replay succeeds, then create the Draft PR when that mutation path recovers. Leave the substantive change REVIEW_PENDING for a later independent judgement.
