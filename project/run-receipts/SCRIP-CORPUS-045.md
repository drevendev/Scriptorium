# Run receipt — SCRIP-CORPUS-045

- Issue: #177
- Draft PR: #178
- Base: `master@87929007415ede118cc5700a1e34f2cb3cfc576f`
- Authored status: `REVIEW_PENDING`
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

## Verification handoff

PR #178 is intentionally Draft. Record final exact-head CI/artifact evidence in the PR conversation after the final authored commit settles; a later independent wake must judge that exact head before Ready/merge.
