# Run receipt — SCRIP-CORPUS-045

- Issue: #177 (closed completed)
- PR: #178 (squash-merged as `5e3833e96fd5e28fe19d24c8e20798fa54eadca4`)
- Base: `master@87929007415ede118cc5700a1e34f2cb3cfc576f`
- Reviewed exact head: `b8238144caeb23256eae6a61a49e47b07c687f29`
- Final status: `COMPLETE`
- Unit type: corpus / provenance — fail-closed renderer prerequisite

## Produced

- `scriptorium/darwin_render_profile.py`: deterministic profile builder/validator bound to the reviewed Darwin exact-388 render-surface freeze.
- `darwin-origin-species-rachinsky-1864-ru.render-profile.json`: source-free canonical decision profile, SHA-256 `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.
- `tests/test_darwin_render_profile.py`: exact rebuild, shape coverage, stale-digest mutation, unresolved-semantics and closed-gate regressions.
- `.github/workflows/darwin-render-profile.yml`: exact-head Python 3.13 verification, deterministic rebuild and source-free artifact upload.
- synchronized public candidate page, main source-edition trace and render-surface source graph.

## Frozen boundary

- 18/18 observed tag shapes classified; 5,164 observed tag tokens.
- 38/38 observed template shapes classified; 4,583 observed template invocations.
- unresolved: 5 tag shapes / 518 tokens (`math`, `ref`, `references`) and all 38 template shapes / 4,583 invocations; `nop` is explicitly inter-page-sensitive.
- render profile frozen, but renderer semantics/implementation/equivalence and inter-page composition are not frozen.
- literary-body count/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed.

## Safety / source boundary

No Page wikitext, template argument values, OCR, rendered prose, DjVu/PDF bytes or literary text were committed. The profile consumes only the committed source-free freeze and validates its cryptographic self-digest before classification.

## Independent verification

- Exact comparison: 11 commits ahead / 0 behind, 11 changed files, no inline review threads.
- All 16 PR-triggered workflows on `b8238144caeb23256eae6a61a49e47b07c687f29` completed `success`.
- Dedicated run `35546120433`, job `106172226254`, checked out the reviewed SHA; 7 profile + 5 provenance tests passed and deterministic rebuild matched the committed profile.
- Artifact `10616812708` independently matched 1,914-byte ZIP SHA-256 `12f3be444a4565f7aee5413aef9183487a072bfe9de47ae6b6d27fec05474fbb`; it contained only the 12,592-byte source-free profile JSON, whose canonical embedded SHA-256 recomputed to `2ebcfea51282505c28824f54f6a1795bd7e87e2f958ac59f5c843e68c2066f3d`.
- Pages run `35546120447`, job `106172226404`, checked out the same SHA and passed 376 standard-library tests plus canonical and deterministic static-site builds.
- Independent judgement was recorded as COMMENT review `5262352606`, not self-approval.

## Completion

PR #178 was marked Ready and squash-merged as `5e3833e96fd5e28fe19d24c8e20798fa54eadca4`; Issue #177 closed `completed`. Provider/template/reference/math semantics and inter-page composition remain subsequent evidence units. No benchmark gate advanced; M2 remains 0/5.
