# Darwin/Rachinsky 1864 — `{{ВАР}}` provider revision identities

This source-free companion advances the independently reviewed SCRIP-CORPUS-083 observed-live `{{ВАР}}` closure by binding all six exact revisions to official Russian Wikisource identity metadata. It is an identity-completion artifact, not a full `{{ВАР}}` replay, historical-transclusion claim, or renderer promotion.

The frozen closure remains:

`Шаблон:ВАР@3684602` → `Модуль:Дореформенная орфография@5721277` → `Module:Header@5746249` → `Module:BEED@5746253` + `Module:Util@5750249`; loading BEED also loads `Module:RomanNumber@3684553`.

The official MediaWiki revisions API returned a 40-hex SHA-1 for every exact revision. Russian Wikisource canonicalizes the English `Module:` namespace aliases used by Lua dependency strings to local provider titles under `Модуль:`; the evidence therefore stores both the reviewed closure alias and the provider-returned title.

| Closure title | Provider title | Revision | MediaWiki SHA-1 |
| --- | --- | ---: | --- |
| `Шаблон:ВАР` | `Шаблон:ВАР` | 3684602 | `fdb6fa7c0d4b08157bc30d44f5f77c5b9313167c` |
| `Модуль:Дореформенная орфография` | `Модуль:Дореформенная орфография` | 5721277 | `64d28378f4f620c67e1823a0d4292445d9ab293d` |
| `Module:Header` | `Модуль:Header` | 5746249 | `2ab2bfdd7e49c73c4ec9ef24e4625c1d228cfba0` |
| `Module:BEED` | `Модуль:BEED` | 5746253 | `9e9531e9178e0333bd3a939ace91e6a71e114cc5` |
| `Module:Util` | `Модуль:Util` | 5750249 | `945f8e6bf173bb5712385995255a8b6eccef38ed` |
| `Module:RomanNumber` | `Модуль:RomanNumber` | 3684553 | `51a3956469ee3fbd4ed56ce3a1f72f76f231e1d3` |

The machine-readable contract is [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-revision-identities-evidence.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-revision-identities-evidence.json), SHA-256 `98dc8aed94fd8b4e18f0ad3325673603cba1575c1e745e1175ab4cd3a8aa2a48`. It also retains provider page IDs, UTC revision timestamps, source-free wikitext counts, and SHA-256 digests captured without persisting source prose.

`mediawiki_sha1_complete=true`, but `replay_ready=false`. `ВАР` remains unresolved at **388 invocations**, and the effective backlog remains **4 tag shapes / 130 tag tokens** plus **37 template shapes / 2,356 template invocations**. Full candidate invocation replay, historical transclusion, an explicit version-pinned Scribunto/runtime boundary, renderer promotion, literary-body identity, `>=300k` admission, FantLab analyzer-input identity, and M2 parity all remain open.

The next bounded step is to replay the candidate `{{ВАР}}` branch against exactly these six identities under an explicit version-pinned runtime boundary; no later live descendants may silently substitute for the frozen revisions.
