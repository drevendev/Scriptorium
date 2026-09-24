# SCRIP-CORPUS-082 — Darwin/Rachinsky `{{ВАР}}` provider-drift guard

- Re-oriented from `master@bd291227733155672f8dd6d9d3a634348615cdbe`; no open review-ready PR or interrupted unit preempted normal P2 corpus/provenance selection.
- Fresh Russian Wikisource evidence materially changes the next `{{ВАР}}` replay decision: `Модуль:Header@5746249` is dated 2026-09-10, later than the already pinned `Модуль:Дореформенная орфография@5721277`, and a 2026-09-08 Wikisource forum discussion explicitly raised possible `{{ВАР}}` breakage after Header-related changes. This is recorded as provider-drift risk, not as proof of a runtime failure.
- Added deterministic source-free evidence `scriptorium-darwin-var-provider-drift-evidence-v1`, SHA-256 `6126adbc966c7120ca487fb940bd0e01aafa0d7350d332e6422edbf8b3846cb8`.
- Replayed only the observed Header title-classification rule for the retained Darwin mainspace title `О происхождении видов (Дарвин; Рачинский)/1864 (ВТ:Ё)`: edition segment `1864 (ВТ:Ё)` yields `isPRS=false`, therefore the pinned VAR module would select the second/modern argument if that non-Page branch is reached.
- Kept `Шаблон:ВАР` root identity, Header MediaWiki SHA-1, nested replay closure, full VAR invocation replay, historical transclusion and offline/version-pinned runtime explicitly unfrozen. No render-profile/backlog promotion occurs; `ВАР` stays unresolved at 388 occurrences and effective backlog counts do not change.
- Added focused regressions and a public source-free provider-drift companion. Renderer/body/>=300k/FantLab-input gates stay closed; M2 remains 0/5.
- Next evidence must deliberately select one coherent replay snapshot and freeze exact template/module/Header identities plus execution-relevant closure before a full candidate invocation replay. A later live descendant must not be substituted as historical provenance.

Issue: #253. Draft PR: pending at authoring time.
