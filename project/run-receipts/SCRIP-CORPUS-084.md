# Run receipt — SCRIP-CORPUS-084

Status: COMPLETE

## Orientation

- Authoring identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `e7bf53b7ae2485b106158d09b728c72b86f9e5f6`.
- Exact reviewed head: `85af2a2073dbb1926aaa406bbcc091082a286d8c`.
- Issue: #257 (closed completed).
- PR: #258 (squash-merged).

## Produced

- A source-free identity contract for exactly the six observed-live Darwin/Rachinsky `{{ВАР}}` revisions frozen by canonical SCRIP-CORPUS-083.
- A dedicated workflow that re-fetches those exact revisions through the official Russian Wikisource MediaWiki revisions API and compares provider identity metadata without persisting source prose.
- Deterministic builder/validator, six focused regressions, and a public source-free identity companion.

Evidence SHA-256: `98dc8aed94fd8b4e18f0ad3325673603cba1575c1e745e1175ab4cd3a8aa2a48`.

## Provider capture

The first capture run failed closed on a real namespace canonicalization mismatch: the dependency graph used `Module:Header`, while Russian Wikisource returned the canonical provider title `Модуль:Header`. The workflow was repaired to preserve both identities instead of weakening title checks.

Final exact-head run `36003962326` completed successfully on `85af2a2073dbb1926aaa406bbcc091082a286d8c`. Its checkout, standard-library test suite, provider capture, committed-contract comparison and source-free artifact upload all completed successfully. Authoring handoff recorded 604/604 standard-library tests including all six `DarwinVarRevisionIdentityTests`.

Exact-head artifact `10809920402` was independently downloaded during review. Its ZIP SHA-256 recomputed to `04ece4b07683d9d3fc5f7acbd700d5aee9b1a2d4bc0fe2f1f685ec0439fd92f9`, matching GitHub metadata. The ZIP contained exactly one source-free JSON file with six identity rows matching the committed evidence. The evidence self-digest independently recomputed to `98dc8aed94fd8b4e18f0ad3325673603cba1575c1e745e1175ab4cd3a8aa2a48`.

Provider-bound SHA-1 values:

- `Шаблон:ВАР@3684602` — `fdb6fa7c0d4b08157bc30d44f5f77c5b9313167c`
- `Модуль:Дореформенная орфография@5721277` — `64d28378f4f620c67e1823a0d4292445d9ab293d`
- `Module:Header@5746249` / provider `Модуль:Header` — `2ab2bfdd7e49c73c4ec9ef24e4625c1d228cfba0`
- `Module:BEED@5746253` / provider `Модуль:BEED` — `9e9531e9178e0333bd3a939ace91e6a71e114cc5`
- `Module:Util@5750249` / provider `Модуль:Util` — `945f8e6bf173bb5712385995255a8b6eccef38ed`
- `Module:RomanNumber@3684553` / provider `Модуль:RomanNumber` — `51a3956469ee3fbd4ed56ce3a1f72f76f231e1d3`

## Independent review and merge

The later review pass independently read all 8 changed files against unchanged authoring base `e7bf53b7ae2485b106158d09b728c72b86f9e5f6`, found no merge blockers and found no open review threads. GitHub rejected a formal `APPROVE` event because it treated the connected reviewer as the pull-request author; review `5305445089` therefore records the exact-head judgement as `COMMENT` instead of misrepresenting approval state.

PR #258 was marked Ready and squash-merged with expected-head protection as `70a20089488fffc169bc807318ca82e9eb33f18b`. Issue #257 closed automatically as completed.

## Evidence boundary

`revision_ids_complete=true` and `mediawiki_sha1_complete=true`, but `replay_ready=false`. No full candidate `{{ВАР}}` invocation has been replayed; historical transclusion and an explicit version-pinned Scribunto/runtime boundary remain unproven. No render-profile rule or backlog item is promoted. `ВАР` remains unresolved at 388 invocations; effective unresolved counts remain 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. Literary-body identity, >=300k admission, FantLab analyzer-input identity and parity remain closed; M2 stays 0/5.

## Handoff

Resume the normal corpus/provenance queue. A separately bounded Darwin unit may attempt full candidate `{{ВАР}}` invocation replay against exactly these six identities under an explicit version-pinned Scribunto/MediaWiki runtime boundary. Keep historical-transclusion, promotion, complete-renderer, literary-body, >=300k, FantLab-input and M2 gates closed until separately evidenced.
