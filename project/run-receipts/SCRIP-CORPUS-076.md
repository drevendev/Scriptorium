# SCRIP-CORPUS-076 run receipt

## Selection

- Mode: corpus / provenance research from the queued P2 SCRIP-CORPUS continuation.
- Base: exact `master@003de730681010d02a94dac9dc08c66ab7bad4bc`.
- Issue: #241.
- Branch: `scrip-corpus-076-darwin-yo-closure`.
- Pull request: #242 (Draft; review pending).
- Reason: Darwin/Rachinsky 1864 is a diversified nonfiction/translation candidate whose reviewed replay contract had one remaining unbound dependency even though a durable exact-revision Module:String probe already existed. Closing that bounded source-free dependency graph is a higher-value next provenance step than inferring renderer output or historical transclusion behavior.

## Upstream evidence

- Reviewed predecessor: `scriptorium-darwin-template-yo-replay-contract-v4`, contract SHA-256 `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`.
- Reviewed exact module probe: `scriptorium-darwin-module-string-dependency-probe-v1`, probe SHA-256 `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- Selected exact module identity: `Модуль:String@3684569`, timestamp `2019-06-04T20:18:11Z`, MediaWiki SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`.
- Exact module source metadata from the reviewed probe: 18,468 UTF-8 bytes, SHA-256 `258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03`.
- The probe is complete under `scriptorium-darwin-lua-loader-scan-v1`: no dynamic/unsupported loader calls and no static wiki-module descendants. Source content is not retained.

## Produced

- `scriptorium/darwin_template_yo_replay_contract_v5.py` — validates predecessor/probe self-digests, binds the reviewed exact Module:String identity, derives its source-free complete discovery proof and requires transitive graph closure.
- `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v5.json` — canonical source-free successor, contract SHA-256 `4ded05d3ea45e9cfa9aa657e6b4e1c26c48cf2f1be60643d0194993e995b4c0c`.
- `tests/test_darwin_template_yo_replay_contract_v5.py` — deterministic-build, complete-closure, exact-leaf, stale-evidence and gate-boundary regressions.
- `.github/workflows/darwin-template-yo-direct-dependency-probe.yml` — extends the existing exact-root CI surface to trigger on v5/probe inputs, run v5/probe-freeze focused tests, rebuild v5 from the reviewed predecessor/probe, byte-compare it to the canonical artifact and upload source-free v4/v5 contracts.
- `corpus/candidates/darwin-origin-species-rachinsky-1864-ru-template-yo-direct-dependencies.md` — public companion updated with the selected three-node graph and provenance boundary.
- `project/CHANGELOG.d/SCRIP-CORPUS-076.md`, this receipt and canonical state handoff.

## Decision

The selected controlled-replay dependency graph is now intended to be exactly:

```text
Шаблон:Ё@5687302 -> Шаблон:ЕЁ@3684646 -> Модуль:String@3684569
```

Every node carries exact revision ID/timestamp/MediaWiki SHA-1 and complete direct-dependency discovery evidence. `Модуль:String` is a discovered leaf under the reviewed bounded scanner. The module discovery-evidence SHA-256 is `cb1045fbeb2dbb4309e0355fabd2cce8ee5e8bc3051803c9caec4d9bfd7edf0d`.

This proves dependency identity/discovery closure **only for the deliberately selected replay snapshot**. It does not prove that `Модуль:String@3684569` was historically transcluded when the root revisions were authored.

## Verification / handoff

- Draft PR #242 is the review surface. Exact authored-head PR-triggered CI must settle before judgement.
- The dedicated direct-dependency workflow now provides a byte-for-byte v5 rebuild check in addition to the repository-wide standard-library test suite.
- A later wake must independently re-read the full diff, require exact-head checks to succeed, verify the committed contract can be deterministically rebuilt from the reviewed v4/probe artifacts, and confirm no source prose or downstream gate promotion slipped in.
- This authoring run must not self-approve or merge the substantial change.

## Gates

- `semantic_dependency_closure_proved=true` only for the selected replay snapshot after the v5 contract passes independent review.
- `historical_transclusion_provenance_proved=false`.
- `outputs_verified=false`.
- `render_profile_rule_promoted=false`.
- `renderer_semantics_complete=false`.
- `renderer_implementation_ready=false`.
- `inter_page_composition_frozen=false`.
- `literary_body_count_and_digests_frozen=false`.
- `minimum_300k_proved=false`.
- `admitted_for_calibration=false`.
- `diagnostic_ready=false`.
- `fantlab_source_edition_match=unknown`.
- `m2_parity_admissible=false`; M2 remains 0/5.

Next admissible work after independent merge is deterministic forced/non-forced replay in a controlled environment that consumes only the bound identities. Dependency closure alone does not remove `{{ё}}` from the unresolved renderer backlog.
