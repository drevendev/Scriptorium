# Darwin/Rachinsky 1864 — `{{ВАР}}` observed-live snapshot closure

This source-free companion narrows the unresolved Darwin/Rachinsky `{{ВАР}}` replay to one explicit provider snapshot observed on **2026-09-24**. It is a replay-preparation artifact, not a historical-transclusion claim and not a renderer promotion.

The observed root/load chain is:

`Шаблон:ВАР@3684602` → `Модуль:Дореформенная орфография@5721277` → `Module:Header@5746249` → `Module:BEED@5746253` + `Module:Util@5750249`; loading BEED also loads `Module:RomanNumber@3684553`.

The template root delegates to the orthography module. The orthography module loads Header for `parse_title(..., "isPRS")`. At Header revision `5746249`, module initialization loads BEED and Util; BEED initialization in turn loads RomanNumber. Source inspection keeps function-body-only dependencies such as `Module:Header/Data`, `Module:BEED/scans`, `Module:BEED/lists`, `Модуль:Math`, and `Модуль:Отексте/ЭСБЕ` outside this candidate's observed load-time path because the retained Darwin replay reaches only Header's title classifier.

The revision-ID topology is now explicit, but the identity gate remains closed. The current execution environment could not retrieve MediaWiki `rvprop=sha1`, so none of the six revisions is claimed SHA-1-frozen. Therefore `mediawiki_sha1_complete=false`, `replay_ready=false`, and no full `{{ВАР}}` invocation has been replayed.

The machine-readable contract is [`source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-live-snapshot-closure-evidence.json`](source-edition-traces/darwin-origin-species-rachinsky-1864-ru.var-live-snapshot-closure-evidence.json), SHA-256 `245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509`.

`ВАР` remains unresolved at **388 invocations**. The effective backlog remains unchanged at **4 tag shapes / 130 tag tokens** and **37 template shapes / 2,356 template invocations**. Historical transclusion, an offline/version-pinned Scribunto runtime, complete renderer/body identity, `>=300k` admission, FantLab analyzer-input identity, and M2 parity all remain open.

The next step is mechanical and deliberately separate: acquire MediaWiki SHA-1 for exactly these six revisions, then perform a bounded full candidate invocation replay without substituting later live descendants.
