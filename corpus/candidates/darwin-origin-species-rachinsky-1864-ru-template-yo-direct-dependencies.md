# Darwin/Rachinsky 1864 — `{{ё}}` root direct dependencies

This source-free companion records the deterministic-replay prerequisites after the reviewed v3 root-identity freeze. Exact Russian Wikisource root revision content is fetched only transiently, verified against the already-bound MediaWiki SHA-1, reduced under MediaWiki transclusion controls, and discarded. The repository retains only byte/digest metadata and dependency titles.

## Frozen exact-root observations

| Exact root | Source bytes | Transclusion SHA-256 | Direct template/module dependencies |
| --- | ---: | --- | --- |
| `Шаблон:Ё@5687302` | 271 | `bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7` | `Шаблон:ЕЁ` |
| `Шаблон:ЕЁ@3684646` | 688 | `3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026` | `Модуль:String` |

The scanner handles the bounded syntax needed by these exact roots: comments, `noinclude` / `includeonly` / `onlyinclude`, common non-transcluding literal tags, redirects, static template names, and `#invoke` module names. Bare magic-word handling is deliberately evidence-bounded to the pinned MediaWiki `Help:Magic words@8589537` surface. The exact uppercase `ЕЁ` invocation is bound as a template from root evidence; the exact roots also exercise documented bare `NAMESPACE`, which is explicitly classified as a variable. Unknown uppercase names and parameterized magic-word-like invocations fail closed instead of being silently discarded. Synthetic regressions cover those boundaries, including `{{ЕЁ|ё|е}} -> Шаблон:ЕЁ`. No template body or rendered prose is committed.

Canonical source-free artifact:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json)
- schema: `scriptorium-darwin-template-yo-replay-contract-v4`
- contract SHA-256: `f5a021fe544bb74f8f7a493bf20c7005f5a79c9c7b78eb10c86ff93a86b26e64`
- scanner: [`../../scriptorium/darwin_template_dependency_scan.py`](../../scriptorium/darwin_template_dependency_scan.py)
- builder/validator: [`../../scriptorium/darwin_template_yo_replay_contract_v4.py`](../../scriptorium/darwin_template_yo_replay_contract_v4.py)

## Dependency revision-selection policy

The unbound `Модуль:String` child must **not** be backdated from either exact root's revision timestamp. MediaWiki's public template documentation describes ordinary template calls as dynamic transclusion: changing a template affects pages that transclude it when they are loaded. The `action=expandtemplates` API documents `revid` as revision context for `{{REVISIONID}}` and similar variables, not as a recursive version pin. Wikimedia's T31051 also records the absence of normal versioned-transclusion support for selecting a specific template revision; T70399 was closed as a duplicate on 2026-08-14.

Scriptorium therefore freezes a fail-closed source-free policy: the next child identity may be bound only from an explicit exact revision observed or deliberately selected in a controlled replay snapshot, with canonical title, revision ID, timestamp, MediaWiki SHA-1 and observation context recorded together. Caller timestamps are not dependency selectors.

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.dependency-revision-selection-policy-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.dependency-revision-selection-policy-v1.json)
- schema: `scriptorium-darwin-dependency-revision-selection-policy-v1`
- policy SHA-256: `4a58b70d5935f4455e58a929c6c1b6cc6a527d7b9d63121e0023501055889855`
- validator: [`../../scriptorium/darwin_dependency_revision_policy.py`](../../scriptorium/darwin_dependency_revision_policy.py)

## Controlled `Модуль:String` observation

SCRIP-CORPUS-067 adds the first controlled, metadata-only observation permitted by that policy. On **2026-09-23T06:03:11Z**, the PR workflow queried Russian Wikisource with `curtimestamp=1`, canonical title `Модуль:String`, and `rvprop=ids|timestamp|sha1` while explicitly requesting no source content. The API returned current revision **`3684569`**, timestamp **`2019-06-04T20:18:11Z`**, and MediaWiki SHA-1 **`a34727a1e4ec3c4b4c7ec556c94991f75442d99c`**. The source-free observation SHA-256 is **`e60fc5e4f59164e98114024a4464f377f0684673be979e0fe18ed7b1fb9070bc`**.

This is a reproducible point-in-time **observation**, not a claim about which module revision was historically transcluded when either root revision was authored. The observation is retained as the reviewed exact-revision candidate later selected by SCRIP-CORPUS-076 for a controlled replay snapshot; historical-transclusion provenance remains explicitly unproved.

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json)
- schema: `scriptorium-darwin-dependency-revision-observation-v1`
- observation SHA-256: `e60fc5e4f59164e98114024a4464f377f0684673be979e0fe18ed7b1fb9070bc`
- builder/validator: [`../../scriptorium/darwin_dependency_revision_observation.py`](../../scriptorium/darwin_dependency_revision_observation.py)

## Exact module source-free dependency probe

SCRIP-CORPUS-068 adds a separate **probe** before any successor contract is allowed to bind the observed module revision. PR CI fetches exact `Модуль:String@3684569` with `rvprop=ids|timestamp|sha1|content` and `rvslots=main`, verifies the returned title/revision/timestamp/SHA-1 against the reviewed metadata-only observation, then treats the Lua source as transient evidence and discards it. Only source byte/digest metadata and derived loader/dependency names are emitted.

The bounded Lua scanner recognizes literal wiki-module references passed to `require(...)`, `mw.loadData(...)`, and `mw.loadJsonData(...)`; it ignores ordinary quoted/long strings and comments, records non-wiki `require` literals separately, and marks the scan incomplete when a loader argument is dynamic or otherwise unsupported. This probe was intentionally not itself a binding artifact: `module_string_identity_bound=false` and `dependency_closure_complete=false` remain in the v1 probe even when the live scan succeeds.

SCRIP-CORPUS-069 makes the reviewed source-free output repository-durable instead of relying on the probe workflow's seven-day artifact retention. The canonical JSON below is byte-for-byte the reviewed probe (`e27a2af...`); PR CI regenerates it from exact revision `3684569` and fails if the regenerated bytes differ. This durability promotion does **not** widen the scanner's semantic scope or convert the point-in-time revision into historical-transclusion provenance.

- canonical probe: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-dependency-probe-v1.json)
- probe implementation: [`../../scriptorium/darwin_module_string_dependency_probe.py`](../../scriptorium/darwin_module_string_dependency_probe.py)
- schema: `scriptorium-darwin-module-string-dependency-probe-v1`
- probe SHA-256: `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`
- exact source metadata: 18,468 UTF-8 bytes; SHA-256 `258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03`
- source retention: none; the raw exact-revision response is deleted before byte comparison/upload of the source-free derived JSON

## Version-pinned dependency closure

SCRIP-CORPUS-076 adds successor contract **v5**. It deliberately selects the already-reviewed exact `Модуль:String@3684569` observation as a dependency of the controlled replay snapshot, not as a historical-transclusion claim. The reviewed module probe has `scan_complete=true`, no dynamic/unsupported loader calls and no static wiki-module descendants, so v5 can bind the third node with a complete source-free discovery proof.

The closed graph is exactly:

```text
Шаблон:Ё@5687302 -> Шаблон:ЕЁ@3684646 -> Модуль:String@3684569
```

All three nodes carry exact revision ID, timestamp and MediaWiki SHA-1. Every node also carries complete direct-dependency discovery evidence whose SHA-256 is recomputed from the exact identity and child-title list. `validate_dependency_closure(..., require_complete=True)` succeeds only when the two graph edges exactly match those proofs and the module remains a discovered leaf.

Canonical source-free successor:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v5.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v5.json)
- schema: `scriptorium-darwin-template-yo-replay-contract-v5`
- contract SHA-256: `4ded05d3ea45e9cfa9aa657e6b4e1c26c48cf2f1be60643d0194993e995b4c0c`
- `Модуль:String` discovery-evidence SHA-256: `cb1045fbeb2dbb4309e0355fabd2cce8ee5e8bc3051803c9caec4d9bfd7edf0d`
- builder/validator: [`../../scriptorium/darwin_template_yo_replay_contract_v5.py`](../../scriptorium/darwin_template_yo_replay_contract_v5.py)

`semantic_dependency_closure_proved=true` in v5 means only that this selected replay snapshot has a complete source-free dependency graph under the bounded scanners and reviewed exact identities. It does **not** prove that `Модуль:String@3684569` was historically transcluded by either root revision.

## Fail-closed boundary

Dependency identity/discovery is closed in v5, but rendering semantics are not. No forced/non-forced output has yet been verified in an environment that consumes only the three bound revisions. Therefore `outputs_verified=false`, `render_profile_rule_promoted=false`, `renderer_semantics_complete=false`, `renderer_implementation_ready=false`, body/`>=300k` admission gates remain closed, `fantlab_source_edition_match=unknown`, and `m2_parity_admissible=false`. M2 remains **0/5**.

The next admissible step is controlled version-pinned replay of both documented modes (`ё` when forced, `е` otherwise) with deterministic output identities. Dependency closure by itself is not permission to remove `{{ё}}` from the unresolved semantic backlog.
