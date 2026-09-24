# Run receipt — SCRIP-CORPUS-083

Status: COMPLETE

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `ee57313a6974abd326311a7b70f010ae647781a2`.
- Issue: #255, closed completed after merge.
- PR: #256, independently reviewed and squash-merged.

## Produced

- Source-free observed-live `{{ВАР}}` replay-snapshot closure for the retained Darwin/Rachinsky candidate.
- Exact observed revision-ID topology: `Шаблон:ВАР@3684602` -> `Модуль:Дореформенная орфография@5721277` -> `Module:Header@5746249` -> `Module:BEED@5746253` + `Module:Util@5750249`; BEED -> `Module:RomanNumber@3684553`.
- Explicit separation of load-time dependencies from latent function-body dependencies that are not reached by the candidate `parse_title(..., "isPRS")` path.
- Deterministic contract builder/validator, five focused regressions, and a public source-free companion.

Evidence SHA-256: `245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509`.

## Research evidence

- Current Russian Wikisource documentation continues to describe `{{ВАР}}` as a Lua-backed two-argument orthography selector implemented through `Модуль:Дореформенная орфография`.
- `Модуль:Дореформенная орфография@5721277` loads `Module:Header` and uses `header.parse_title(..., "isPRS")` on non-Page namespaces.
- `Module:Header@5746249` is the provider revision independently visible during review and its source loads `Module:BEED` and `Module:Util` at module initialization.
- The authored closure records `Module:BEED@5746253` -> `Module:RomanNumber@3684553` and `Module:Util@5750249` as the remaining observed-live load-time snapshot identities. Direct MediaWiki API retrieval for `rvprop=sha1` remained unavailable in the review environment, so SHA-1 identities were not invented.

## Evidence boundary

`revision_ids_complete=true`, but `mediawiki_sha1_complete=false` and `replay_ready=false`. All six `mediawiki_sha1` fields are null. Historical transclusion is unproven; no offline/version-pinned Scribunto runtime is established; no full candidate `{{ВАР}}` invocation is replayed; no render-profile or backlog promotion occurs. `ВАР` remains unresolved at 388 invocations and effective unresolved counts remain 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. Literary-body identity, >=300k admission, FantLab analyzer-input identity and parity remain closed; M2 stays 0/5.

## Verification performed in authoring run

- Official provider pages/search evidence were re-read for the six revision IDs and their load relationships.
- The evidence contract was generated from the same deterministic structure used by the committed builder; its self-digest is pinned above.
- Substantive changes were left in Draft PR #256 for later independent exact-head review. The authoring run did not approve or merge its own work.

## Independent review and merge

- Exact authored head `8367bc807fd30b90acae81386a481c78681c7b3e` was independently re-read across all 7 changed files against unchanged `master@ee57313a6974abd326311a7b70f010ae647781a2`.
- Review `5304043399` found no merge blocker and no open review thread.
- The evidence self-digest was independently recomputed as `245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509`.
- All 22 PR-triggered workflow runs visible for the exact authored head completed `success`. Frozen-diagnostic run `35990136656` checked out that exact head; both jobs completed their standard-library and frozen-source replay steps successfully. The authoring handoff records 598/598 standard-library tests including all five new `DarwinVarLiveSnapshotClosureTests`.
- PR #256 was marked Ready and squash-merged with expected-head protection as `318d223ed8745597c3b4174d29f3dc0f24a9d0df`; Issue #255 closed with `completed`.

## Next action

Resume normal-flow P2 SCRIP-CORPUS selection. A separate future Darwin/Rachinsky unit may acquire MediaWiki SHA-1 for exactly the six bound revisions before attempting a full `{{ВАР}}` invocation replay. Until then, SHA-1/replay/historical-transclusion/offline-runtime/promotion/body/FantLab/M2 gates remain closed.
