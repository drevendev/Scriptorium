## 2026-09-24 — Darwin `{{ВАР}}` provider revision identities

- Selected SCRIP-CORPUS-084 / Issue #257 from the normal-flow P2 corpus queue after confirming no interrupted/open PR or issue recovery work.
- Added a dedicated source-free GitHub Actions capture for exactly the six SCRIP-CORPUS-083 observed-live revisions using the existing fail-closed MediaWiki revision fetch primitive.
- The first capture run correctly failed because Russian Wikisource canonicalizes `Module:` aliases to the local `Модуль:` namespace. The workflow was repaired to bind both the reviewed closure alias and provider-returned canonical title instead of weakening title validation.
- Successful provider capture bound all six exact revision IDs to page IDs, UTC timestamps, 40-hex MediaWiki SHA-1 values, source-free wikitext counts, and SHA-256 digests without committing source prose.
- Added deterministic evidence builder/validator, six focused regressions, and a public source-free companion. Evidence SHA-256: `98dc8aed94fd8b4e18f0ad3325673603cba1575c1e745e1175ab4cd3a8aa2a48`.
- `mediawiki_sha1_complete=true`, but `replay_ready=false`: full `{{ВАР}}` candidate replay, historical transclusion, explicit version-pinned Scribunto/runtime identity, renderer promotion, backlog reduction, literary-body identity, >=300k admission, FantLab-input identity and M2 parity remain outside this unit and closed.
- `ВАР` remains unresolved at 388 invocations; effective backlog remains 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. M2 remains 0/5.
- Draft PR #258 remains for a later independent exact-head review; this authoring run does not self-approve or merge its substantive change.
