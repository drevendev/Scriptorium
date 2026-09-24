# Run receipt — SCRIP-CORPUS-084

Status: REVIEW_PENDING

## Orientation

- Connected GitHub identity: `andy-zen-dev`.
- Repository: `drevendev/Scriptorium`; write permission available.
- Exact authoring base: `e7bf53b7ae2485b106158d09b728c72b86f9e5f6`.
- Issue: #257.
- Draft PR: #258.

## Produced

- A source-free identity contract for exactly the six observed-live Darwin/Rachinsky `{{ВАР}}` revisions frozen by canonical SCRIP-CORPUS-083.
- A dedicated workflow that re-fetches those exact revisions through the official Russian Wikisource MediaWiki revisions API and compares provider identity metadata without persisting source prose.
- Deterministic builder/validator, six focused regressions, and a public source-free identity companion.

Evidence SHA-256: `98dc8aed94fd8b4e18f0ad3325673603cba1575c1e745e1175ab4cd3a8aa2a48`.

## Provider capture

The first exact-head capture run `36002505015` passed the full 598-test standard-library suite, then failed closed on a real namespace canonicalization mismatch: the dependency graph used `Module:Header`, while Russian Wikisource returned the canonical provider title `Модуль:Header`. The workflow was repaired to preserve both identities instead of weakening title checks.

Corrected run `36002651033` completed successfully and produced artifact `10808782333`. The downloaded ZIP independently recomputed to GitHub's digest `sha256:725332a6cf98804f68dce5dd16322a8a2ba09d1921660f216afb55c8e3c896a4` and contained exactly one source-free JSON artifact.

Provider-bound SHA-1 values:

- `Шаблон:ВАР@3684602` — `fdb6fa7c0d4b08157bc30d44f5f77c5b9313167c`
- `Модуль:Дореформенная орфография@5721277` — `64d28378f4f620c67e1823a0d4292445d9ab293d`
- `Module:Header@5746249` / provider `Модуль:Header` — `2ab2bfdd7e49c73c4ec9ef24e4625c1d228cfba0`
- `Module:BEED@5746253` / provider `Модуль:BEED` — `9e9531e9178e0333bd3a939ace91e6a71e114cc5`
- `Module:Util@5750249` / provider `Модуль:Util` — `945f8e6bf173bb5712385995255a8b6eccef38ed`
- `Module:RomanNumber@3684553` / provider `Модуль:RomanNumber` — `51a3956469ee3fbd4ed56ce3a1f72f76f231e1d3`

## Evidence boundary

`revision_ids_complete=true` and `mediawiki_sha1_complete=true`, but `replay_ready=false`. No full candidate `{{ВАР}}` invocation has been replayed; historical transclusion and an explicit version-pinned Scribunto/runtime boundary remain unproven. No render-profile rule or backlog item is promoted. `ВАР` remains unresolved at 388 invocations; effective unresolved counts remain 4 tag shapes / 130 tag tokens and 37 template shapes / 2,356 template invocations. Literary-body identity, >=300k admission, FantLab analyzer-input identity and parity remain closed; M2 stays 0/5.

## Handoff

Draft PR #258 is intentionally left for a later independent exact-head review. The final authored head must re-run the dedicated provider capture, compare the fresh source-free identities to the committed contract, and pass the standard-library suite before review. This authoring run does not approve or merge its own substantive work.
