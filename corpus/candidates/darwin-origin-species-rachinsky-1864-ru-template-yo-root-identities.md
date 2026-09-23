# Darwin/Rachinsky 1864 — exact `{{ё}}` replay-root identities

This source-free companion records the next narrow replay prerequisite after the independently reviewed v2 canonical-title contract. It binds exact MediaWiki revision identities for the two canonical Russian Wikisource roots used by the Darwin/Rachinsky `{{ё}}` replay track. It does **not** claim recursive dependency closure, template-expansion equivalence, literary-body identity, corpus admission, FantLab source identity, or parity.

## Exact roots

The Russian Wikisource Action API was queried by exact revision ID with `rvprop=ids|timestamp|sha1`; no source content was requested. The retained identities are:

| Canonical title | Revision | Timestamp | MediaWiki SHA-1 |
| --- | ---: | --- | --- |
| `Шаблон:Ё` | `5687302` | `2026-01-21T12:32:10Z` | `963c1796d693d5451cf0c0897c35bd7e5b327ae1` |
| `Шаблон:ЕЁ` | `3684646` | `2019-06-04T20:49:40Z` | `435bb2a412d8fb5962ccd5adc0ac2e03412fe109` |

The invocation spelling remains `{{ё}}`; the exact dependency root remains canonical `Шаблон:Ё`, as established by the predecessor contract. The new v3 artifact retains the predecessor identity rather than rewriting that reviewed history.

## What changed

`scriptorium-darwin-template-yo-replay-contract-v3` promotes only `root_identities_bound=true`. The two exact roots now appear in the replay dependency surface with canonical title, revision ID, exact timestamp and MediaWiki SHA-1. The contract is derived from the independently reviewed v2 predecessor with SHA-256 `9b2e8914a5b4c3518ef331c27dc09a6a30d4d6433e90169c677348048f3dcd52`.

Canonical source-free v3 artifact:

- [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v3.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract-v3.json)
- schema: `scriptorium-darwin-template-yo-replay-contract-v3`
- contract SHA-256: `8caa144d9f4c0b9a8149c1822bd79d168d212dea14d72079c3259d55e5e03c8c`
- builder/validator: [`../../scriptorium/darwin_template_yo_replay_contract_v3.py`](../../scriptorium/darwin_template_yo_replay_contract_v3.py)
- predecessor: [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.template-yo-replay-contract.json)

The dedicated read-only workflow re-queries those exact revision IDs, compares title/timestamp/SHA-1 against the committed source-free dependency rows, deterministically rebuilds the v3 artifact and byte-compares it with the committed JSON.

## Next evidence layer

SCRIP-CORPUS-065 freezes complete direct-dependency discovery for these exact roots in the source-free [`darwin-origin-species-rachinsky-1864-ru-template-yo-direct-dependencies.md`](darwin-origin-species-rachinsky-1864-ru-template-yo-direct-dependencies.md) companion. That later layer records the bound `Шаблон:Ё -> Шаблон:ЕЁ` edge and discovers `Шаблон:ЕЁ -> Модуль:String`; the module remains identity-unbound, so recursive closure is still intentionally open.

## Fail-closed boundary

Root identity is only the first layer of deterministic replay. The later v4 direct-dependency layer does not yet bind `Модуль:String` or close the recursive template/module graph. Therefore `dependency_closure_complete=false` remains mandatory even though root identity and root-level direct-dependency discovery are now separately frozen.

The documented forced/non-forced outputs are still unverified in a fully bound replay environment. Accordingly `outputs_verified=false`, `render_profile_rule_promoted=false`, and the `ё` backlog item remains unresolved. Literary-body rendering/count/digests, the >=300k admission gate, `fantlab_source_edition_match`, `diagnostic_ready` and `m2_parity_admissible` also remain closed/unknown. M2 remains **0/5**.

No template body, Page prose, rendered literary text, OCR, scan bytes, or template argument payload is stored by these artifacts.
