# Run receipt — SCRIP-CORPUS-047

## Unit

- Issue: #181 — freeze Darwin/Rachinsky `{{ё}}` documentation evidence boundary.
- Base at selection: `master@ead874a699c9f1a98c100974835f1ffd6601a21e`.
- Branch: `scrip-corpus-047-darwin-yo-evidence`.
- Mode: bounded corpus/provenance + renderer-prerequisite research.

## Research evidence

Official Russian Wikisource documentation at `Шаблон:ЕЁ/Документация`, permanent revision `oldid=5090323` (2024-01-11), documents no-argument `{{ё}}` as a conditional lowercase shorthand: forced yoification -> `ё`; otherwise -> `е`. `Справка:Вычитка` is now pinned at permanent revision `oldid=5731079` (2026-07-19), where `{{ё}}` / `{{ё!}}` are described as the yoification mechanism used to support two finished-text variants.

The retained Darwin Page-revision evidence predates the template-documentation revision. The deterministic witness selected from shard 01 is Page sequence 11 / revision `3358032` / `2018-08-13T19:18:33Z` / MediaWiki SHA-1 `3fe692545a92d2103d667ce02dd7237889fa2ccc`. Therefore current official documentation is useful semantic evidence but is not proof of historical template/dependency equivalence for the frozen Page revisions.

## Produced

- `scriptorium/darwin_template_yo_evidence.py`
- `tests/test_darwin_template_yo_evidence.py`
- `.github/workflows/darwin-template-yo-evidence.yml`
- source-free structured evidence `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-evidence.json`
- public semantic-backlog companion update
- changelog/state handoff for independent review

Canonical evidence SHA-256 after review-blocker repair: `9123d9f2901b4995deac5c4e09ca09af386befc8129f62e844446d44b864bfd2`.

## Independent review repair

Review `5263767395` found two merge blockers on authored head `75be125234db0c6f096dc056f7c799ae531eec24`:

1. proofread-help evidence used a mutable live URL rather than a permanent revision identity;
2. evidence derivation trusted the backlog's stored `backlog_sha256` without recomputing the full canonical backlog digest.

This recovery unit repairs both without changing renderer semantics. The evidence record now pins `Справка:Вычитка@oldid=5731079` / `2026-07-19`, and `build_evidence()` recomputes the semantic backlog self-digest before selecting the target. Tests include a non-target backlog mutation with a stale digest and require fail-closed rejection.

## Boundary / gates

The render profile and existing semantic backlog are intentionally unchanged. Template `ё` remains unresolved in the renderer profile/backlog because historical template revision/dependency identity is not yet frozen. All 43 unresolved shapes remain. Renderer implementation/equivalence, inter-page composition, literary-body counts/digests, >=300k admission, FantLab source match, diagnostic readiness and M2 parity remain closed; M2 remains 0/5.

## Verification handoff

The repair wake authored commits on the existing Draft PR and therefore does not self-approve, mark Ready or merge. Fresh exact-head checks and a separate independent review are required. Append the settled exact-head workflow/artifact evidence in the PR discussion before judgement.

## Independent review and merge

Independent review `5264353490` re-read final exact head `bc0ad4b50931f45a7e87c9019cdece031213cc95` against unchanged base `ead874a699c9f1a98c100974835f1ffd6601a21e`. The PR was 16 commits ahead / 0 behind with 8 changed files and no unresolved review threads. Both blockers from review `5263767395` were confirmed closed and no new blocker was found.

All 15 PR-triggered workflows on the exact reviewed SHA completed `success`. Dedicated run `35576205074` / job `106258518903` checked out the exact SHA, passed 8 template-yo evidence tests plus 5 semantic-backlog regressions, and deterministically reproduced evidence SHA-256 `9123d9f2901b4995deac5c4e09ca09af386befc8129f62e844446d44b864bfd2`. Artifact `10628476850` was independently downloaded and verified as a 1,561-byte ZIP with SHA-256 `eb32a6d31063557539c4e92d2819c6685956138630fedcf8a2f795471f8bb2c6`, containing exactly one 2,982-byte JSON with SHA-256 `4fc6c58ce4252c17caa5d3976332460b612459dd7865fd8b86869c958c88f39a`; recomputing its canonical embedded evidence digest reproduced `9123d9f2901b4995deac5c4e09ca09af386befc8129f62e844446d44b864bfd2`. Pages run `35576205021` checked out the same exact SHA and passed the full 389-test standard-library suite, canonical site build and deterministic rebuild; deploy remained intentionally skipped.

PR #182 was marked Ready and squash-merged as `3470d97a41ca23290f2ae3d517ba7aab596c966f`, automatically closing Issue #181 as completed. This review did not promote renderer implementation/equivalence, inter-page composition, literary-body counts/digests, >=300k admission, FantLab source match, diagnostic readiness or M2 parity. All 43 semantic-backlog shapes remain unresolved and M2 remains 0/5.
