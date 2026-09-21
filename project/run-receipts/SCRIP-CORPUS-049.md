# SCRIP-CORPUS-049 run receipt

- Unit: `SCRIP-CORPUS-049`
- Issue: #185
- Pull request: #186 (Draft; authored repair, fresh independent exact-head review required)
- Base at selection: `master@dfd1eec6f559deb06adc1b3d37b0c8143f72a355`
- Reviewed pre-repair head: `b69470f5f41f0465b25c577b62999289b66dfa99`
- Blocking review: `5266226440`
- Final review head: read from PR #186 after this repair commit; do not infer it from this receipt.

## Repair decision

The independent review identified two fail-closed gaps and both were repaired in this bounded recovery unit.

1. Recursive-expansion provenance is no longer a live `Help:ExpandTemplates` URL. The contract now pins permanent MediaWiki revision `oldid=8168760` dated 2026-01-23.
2. A dependency graph can no longer be called complete merely because both root titles are bound. Every bound node in a complete closure must carry source-free discovery proof with `status=complete`, a non-empty discovery method, an exact direct-dependency title list and an evidence SHA-256. Every discovered child must be bound, and the graph edges must exactly equal those declared child relationships.

This explicitly distinguishes a proved leaf (`direct_dependencies=[]` with complete discovery evidence) from a node whose children were never enumerated.

Canonical contract SHA-256 after repair: `bb67d05c5aed51cc03917638cbd6d49257d51933e0adb88982ac73826849366c`.

## Verification

Local focused verification reconstructed the replay-contract module, upstream documentation evidence and committed contract artifact and passed **14/14 replay-contract tests**. Regressions include:
- both roots without discovery proof cannot pass `require_complete=True`;
- an explicitly evidenced leaf closure can pass;
- discovered-but-unbound children fail closed;
- graph edges must exactly match discovery proof;
- the recursive-expansion evidence must remain pinned to `oldid=8168760`.

Fresh GitHub Actions must settle on the exact repaired PR head before any Ready/merge judgement.

## Gates

`{{ё}}` remains `semantic_status=unresolved`; all 43 unresolved shapes remain in the backlog. `dependency_closure_complete=false`, both forced/non-forced replay-output hashes remain null, and renderer implementation/equivalence, inter-page composition, literary-body count/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed. M2 remains 0/5.

## Handoff

PR #186 remains Draft because this wake authored the substantive recovery repair. The next wake must independently re-read the exact repaired PR head and fresh settled checks before any Ready/merge decision. No template source bodies, Page prose, rendered literary prose, OCR or scan bytes were committed.
