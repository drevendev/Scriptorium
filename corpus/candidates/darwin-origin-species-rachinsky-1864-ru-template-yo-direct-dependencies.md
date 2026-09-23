# Darwin/Rachinsky 1864 — `{{ё}}` root direct dependencies

This source-free companion records the next deterministic-replay prerequisite after the reviewed v3 root-identity freeze. Exact Russian Wikisource root revision content is fetched only transiently, verified against the already-bound MediaWiki SHA-1, reduced under MediaWiki transclusion controls, and discarded. The repository retains only byte/digest metadata and dependency titles.

## Frozen exact-root observations

| Exact root | Source bytes | Transclusion SHA-256 | Direct template/module dependencies |
| --- | ---: | --- | --- |
| `Шаблон:Ё@5687302` | 271 | `bd7465151d984f06c75eae0c1246c26a0643826a26a170a3e9a9d43c9e5a03b7` | none |
| `Шаблон:ЕЁ@3684646` | 688 | `3975fa227e23e8cc1487a49a3eab86b28e0ddb6a753c347c3191ee800ae56026` | `Модуль:String` |

The scanner handles the bounded syntax needed by these exact roots: comments, `noinclude` / `includeonly` / `onlyinclude`, common non-transcluding literal tags, redirects, static template names, and `#invoke` module names. Dynamic or unsupported invocation names fail closed instead of being guessed. Synthetic regressions cover those boundaries. No template body or rendered prose is committed.

Canonical source-free artifact:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v4.json)
- schema: `scriptorium-darwin-template-yo-replay-contract-v4`
- contract SHA-256: `2e314e81fb3dbbedf05b3b83399d33e233abf0cd858ff70f5728de5c2e613c57`
- scanner: [`../../scriptorium/darwin_template_dependency_scan.py`](../../scriptorium/darwin_template_dependency_scan.py)
- builder/validator: [`../../scriptorium/darwin_template_yo_replay_contract_v4.py`](../../scriptorium/darwin_template_yo_replay_contract_v4.py)

## Fail-closed boundary

Direct-dependency discovery is complete only for the two exact roots. `Шаблон:ЕЁ` discovers `Модуль:String`, but that child has not yet been assigned an exact replay revision identity and its own direct dependencies have not been frozen. The v4 contract therefore records the discovered edge as `target_identity_bound=false`, keeps the executable replay graph empty, and requires `dependency_closure_complete=false`.

No forced/non-forced output has been verified in a recursively bound environment. `outputs_verified=false`, `render_profile_rule_promoted=false`, renderer/body/`>=300k` admission gates remain closed, `fantlab_source_edition_match=unknown`, and `m2_parity_admissible=false`. M2 remains **0/5**.
