## 2026-09-24 — Darwin `{{ВАР}}` observed-live snapshot closure candidate

- Selected SCRIP-CORPUS-083 / Issue #255 from the normal-flow P2 corpus queue after confirming no interrupted/open PR or issue recovery work.
- Re-checked official Russian Wikisource provider state and bound one explicit observed-live replay topology: `Шаблон:ВАР@3684602` -> `Модуль:Дореформенная орфография@5721277` -> `Module:Header@5746249` -> `Module:BEED@5746253` + `Module:Util@5750249`, with BEED loading `Module:RomanNumber@3684553`.
- Distinguished load-time dependencies from latent function-body-only dependencies (`Module:Header/Data`, `Module:BEED/scans`, `Module:BEED/lists`, `Модуль:Math`, `Модуль:Отексте/ЭСБЕ`) not reached by the retained Darwin `parse_title(..., "isPRS")` path.
- The provider API route needed for `rvprop=sha1` was unavailable from this execution environment. The new source-free contract therefore binds revision IDs/topology but keeps all six `mediawiki_sha1` values null, `mediawiki_sha1_complete=false`, and `replay_ready=false` instead of manufacturing identity evidence.
- Evidence SHA-256: `245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509`.
- Added deterministic reconstruction/validation plus five focused regressions and a public source-free companion. No source prose is committed.
- `ВАР` remains unresolved at 388 candidate invocations. Effective backlog remains 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. Historical transclusion, offline/version-pinned runtime, complete renderer/body, >=300k, FantLab-input and M2 gates remain closed; M2 stays 0/5.
- The next evidence step is mechanical: obtain MediaWiki SHA-1 for exactly the six bound revisions, then run a separately bounded full candidate invocation replay. This authoring run does not self-review or merge its substantive PR.
