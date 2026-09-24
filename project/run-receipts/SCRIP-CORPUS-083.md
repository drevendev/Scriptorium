# Run receipt — SCRIP-CORPUS-083

Status: REVIEW_PENDING

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `ee57313a6974abd326311a7b70f010ae647781a2`.
- Issue: #255.
- Draft PR: #256.

## Produced

- Source-free observed-live `{{ВАР}}` replay-snapshot closure for the retained Darwin/Rachinsky candidate.
- Exact observed revision-ID topology: `Шаблон:ВАР@3684602` -> `Модуль:Дореформенная орфография@5721277` -> `Module:Header@5746249` -> `Module:BEED@5746253` + `Module:Util@5750249`; BEED -> `Module:RomanNumber@3684553`.
- Explicit separation of load-time dependencies from latent function-body dependencies that are not reached by the candidate `parse_title(..., "isPRS")` path.
- Deterministic contract builder/validator, five focused regressions, and a public source-free companion.

Evidence SHA-256: `245f77bf3d99d6610ca5fbbe4fcdcdb4ef68bebca612c5bb81db6c2d77f26509`.

## Research evidence

- Current Russian Wikisource `Шаблон:ВАР` remains revision `3684602` and delegates to `Модуль:Дореформенная орфография`.
- `Модуль:Дореформенная орфография@5721277` loads `Module:Header` and uses `header.parse_title(..., "isPRS")` on non-Page namespaces.
- Current `Module:Header@5746249` loads `Module:BEED` and `Module:Util` at module initialization.
- Current `Module:BEED@5746253` loads `Module:RomanNumber`; current `Module:Util@5750249` and `Module:RomanNumber@3684553` expose no additional load-time module dependency in the observed source.
- The environment's direct MediaWiki API route for `rvprop=sha1` was unavailable, so revision IDs are recorded but SHA-1 identities are deliberately not invented.

## Evidence boundary

`revision_ids_complete=true`, but `mediawiki_sha1_complete=false` and `replay_ready=false`. All six `mediawiki_sha1` fields are null. Historical transclusion is unproven; no offline/version-pinned Scribunto runtime is established; no full candidate `{{ВАР}}` invocation is replayed; no render-profile or backlog promotion occurs. `ВАР` remains unresolved at 388 invocations and effective unresolved counts remain 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. Literary-body identity, >=300k admission, FantLab analyzer-input identity and parity remain closed; M2 stays 0/5.

## Verification performed in authoring run

- Official provider pages/search evidence were re-read for the six revision IDs and their load relationships.
- The evidence contract was generated from the same deterministic structure used by the committed builder; its self-digest is pinned above.
- Substantive changes were left in Draft PR #256 for later independent exact-head review. This authoring run did not approve or merge its own work.

## Next action

Independently re-read all changed files and exact-head CI for PR #256. If clean, mark Ready and merge with expected-head protection. Only after that, in a separate bounded unit, acquire MediaWiki SHA-1 for exactly these six revisions before attempting a full invocation replay.
