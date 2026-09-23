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

This is a reproducible point-in-time **observation**, not a claim about which module revision was historically transcluded when either root revision was authored. The observation is retained so a later bounded unit can independently judge whether to select and bind that exact revision into a successor replay contract. Until such a contract is reviewed, `module_string_identity_observed=true` but `module_string_identity_bound=false`.

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.module-string-observation-v1.json)
- schema: `scriptorium-darwin-dependency-revision-observation-v1`
- observation SHA-256: `e60fc5e4f59164e98114024a4464f377f0684673be979e0fe18ed7b1fb9070bc`
- builder/validator: [`../../scriptorium/darwin_dependency_revision_observation.py`](../../scriptorium/darwin_dependency_revision_observation.py)

## Fail-closed boundary

Direct-dependency discovery is complete only for the two exact roots. The bound replay graph contains `Шаблон:Ё -> Шаблон:ЕЁ`. `Шаблон:ЕЁ` in turn discovers `Модуль:String`; SCRIP-CORPUS-067 now has an explicit exact current-revision observation for that child, but v4 still does not bind it and its own direct dependencies have not been frozen. The v4 contract therefore remains unchanged with the root-to-root edge `target_identity_bound=true`, the module edge `target_identity_bound=false`, and `dependency_closure_complete=false`.

No forced/non-forced output has been verified in a recursively bound environment. `outputs_verified=false`, `render_profile_rule_promoted=false`, renderer/body/`>=300k` admission gates remain closed, `fantlab_source_edition_match=unknown`, and `m2_parity_admissible=false`. M2 remains **0/5**.
