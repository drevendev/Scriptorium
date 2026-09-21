# SCRIP-CORPUS-049 run receipt

- Unit: `SCRIP-CORPUS-049`
- Issue: #185
- Pull request: #186 (Draft; authored repair, fresh independent exact-head review required)
- Base at selection: `master@dfd1eec6f559deb06adc1b3d37b0c8143f72a355`
- Reviewed pre-repair head: `7f5c80bde4075b546c0dc7f9287254ff8608d371`
- Blocking reviews: `5266226440`, `5267466282`
- Final exact review head: read from PR #186 after the final state commit; do not infer it from this receipt.

## Repair decision

The latest independent review found one remaining fail-closed gap after the earlier provenance/closure repair: per-node `evidence_sha256` values were only validated as 64 lowercase hex characters and were not cryptographically bound to the dependency revision identity or direct-dependency set.

This bounded recovery unit closes that gap without binding any real template revision or advancing renderer semantics:

1. Discovery evidence now has source-free schema `scriptorium-template-dependency-discovery-evidence-v1`.
2. `dependency_discovery_evidence_sha256()` computes canonical SHA-256 over candidate identity, exact dependency identity (`title`, `revision_id`, `revision_timestamp`, `mediawiki_sha1`), discovery `status`, discovery `method`, and the exact ordered `direct_dependencies` list.
3. `_validate_discovery_proof()` recomputes that digest and rejects mismatch. An arbitrary well-formed digest therefore cannot prove a leaf, and changing a node revision or dependency list while retaining the old digest fails closed.
4. Complete closure still requires both roots, valid per-node discovery proofs, every discovered child bound, and graph edges exactly equal to the cryptographically bound child relationships.

Canonical contract SHA-256 after this repair: `35bed756f4fafa4f443315c09d04a35c66441eb2249eced3c7540ac20c981afe`.

## Verification

A reconstructed local focused verification passed **17/17 replay-contract tests**. New/updated regressions cover:
- arbitrary synthetic discovery digests cannot prove a leaf;
- a stale discovery digest fails after `direct_dependencies` changes;
- a stale discovery digest fails after `revision_id` changes;
- properly recomputed evidence digests still allow explicitly evidenced leaf roots;
- discovered-but-unbound children fail closed;
- graph edges must exactly match discovery proof;
- recursive-expansion provenance remains pinned to `Help:ExpandTemplates oldid=8168760`;
- the committed contract rebuilds exactly to SHA-256 `35bed756f4fafa4f443315c09d04a35c66441eb2249eced3c7540ac20c981afe`.

Fresh GitHub Actions on the final exact PR head remain the next verification layer before an independent Ready/merge judgement.

## Gates

`{{ё}}` remains `semantic_status=unresolved`; all 43 unresolved shapes remain in the backlog. `dependencies=[]`, `dependency_closure_complete=false`, both forced/non-forced replay-output hashes remain null, and renderer implementation/equivalence, inter-page composition, literary-body count/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed. M2 remains 0/5.

## Handoff

PR #186 remains Draft because this wake authored the substantive integrity repair. The next wake must independently re-read the final exact PR head and settled checks before any Ready/merge decision. No template source bodies, Page prose, rendered literary prose, OCR or scan bytes were committed.
