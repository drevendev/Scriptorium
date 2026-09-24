# Darwin/Rachinsky 1864 — `{{ВАР}}` provider-drift guard

This source-free companion records why Scriptorium does **not** silently bind whatever `Module:Header` happens to be live when replaying the unresolved `{{ВАР}}` shape.

The previously reviewed evidence pins Russian Wikisource `Шаблон:ВАР/Документация@5711068` and `Модуль:Дореформенная орфография@5721277`. The latter delegates non-Page title classification to `Module:Header.parse_title(..., "isPRS")` and selects one of the two arguments from that result.

Fresh provider evidence on 2026-09-24 shows `Модуль:Header@5746249`, last edited 2026-09-10 — later than the pinned VAR implementation module. A Russian Wikisource forum discussion on 2026-09-08 explicitly asked whether `{{ВАР}}` had broken after Header-related work and noted that the small orthography module depends on Header for page-title parsing. Scriptorium records that as a **drift risk**, not as proof that production Wikisource was broken.

For the retained Darwin mainspace title `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`, the observed Header rule at revision `5746249` parses the edition segment as `1864 (ВТ:Ё)` and yields `isPRS=false`. If the pinned VAR module's non-Page branch is reached under that observed rule, it therefore selects the **second (modern) argument**.

That narrow classification replay is not a complete `{{ВАР}}` replay. The live `Шаблон:ВАР` root is still unbound; Header's MediaWiki SHA-1 and execution-relevant nested closure are not frozen; no offline/version-pinned MediaWiki runtime is established; historical transclusion is not inferred; and the render profile/backlog is unchanged. `ВАР` remains unresolved at **388** candidate invocations.

The source-free evidence contract is [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-provider-drift-evidence.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-provider-drift-evidence.json), SHA-256 `6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8`.

The next bounded replay step must deliberately choose one coherent snapshot, freeze exact `Шаблон:ВАР`, `Модуль:Дореформенная орфография` and `Module:Header` identities including MediaWiki SHA-1 plus the execution-relevant nested closure, and only then replay the candidate invocation. A later live descendant must not be substituted as if it were historical provenance.

No source text, Page wikitext, template argument values, rendered prose, OCR or scan bytes are published here. Renderer/body/>=300k/FantLab-input/M2 gates remain unchanged; M2 stays **0/5**.
