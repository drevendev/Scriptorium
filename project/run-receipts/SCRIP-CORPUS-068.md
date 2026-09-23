# Run receipt — SCRIP-CORPUS-068

- **Unit:** SCRIP-CORPUS-068 — exact `Модуль:String` source-free dependency probe
- **Issue:** #224 (open)
- **Pull request:** #225 (Draft; independent review pending)
- **Authoring base:** `master@5aac605ec0a222c60f5fbf60910fa999d664e7c0`
- **Branch:** `work/SCRIP-CORPUS-068-module-string-probe`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded unit advances the reviewed SCRIP-CORPUS-067 point-in-time observation without prematurely turning it into historical provenance or a bound replay edge. The new probe verifies exact `Модуль:String@3684569` metadata against the committed observation before inspecting source content, then emits only source-free derived metadata.

The Lua dependency-surface scanner records UTF-8 byte count, SHA-1/SHA-256 digests, static wiki-module literals supplied to direct `require`, `mw.loadData`, or `mw.loadJsonData` calls, non-wiki require literals, and any dynamic/unsupported direct loader-call classes. Comments plus ordinary/long strings are skipped so loader-looking text there cannot create false dependencies; Lua's bare quoted function-call form is handled and unsupported long-string/dynamic calls fail closed. The artifact explicitly records that alias/computed semantic analysis is outside this scanner's bounded scope and therefore `semantic_dependency_closure_proved=false`.

PR CI fetches the exact observed revision with `rvprop=ids|timestamp|sha1|content` and `rvslots=main`, verifies title/revision/timestamp/SHA-1 before scanning, deletes the raw response after producing the derived JSON, and uploads only that source-free artifact.

## Verification

- Synthetic scanner coverage now has **9** regressions; PR CI also runs the existing dependency-observation regressions.
- Exact-head probe run `35835448030` on `dcda86bec15c4690d65f7531fb2b157547e00f96` completed `success` and uploaded only the source-free derived JSON artifact.
- Exact identity remained `Модуль:String@3684569`, revision timestamp `2019-06-04T20:18:11Z`, MediaWiki SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`.
- Transient exact source measured **18,468 UTF-8 bytes**, SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`, SHA-256 `258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03`.
- Bounded direct-loader scan found **no static wiki-module dependencies**, **no non-wiki require literals**, and **no dynamic/unsupported direct loader calls**; `scan_complete=true` only for that stated direct-call scan scope, while `semantic_dependency_closure_proved=false` remains explicit.
- Source-free probe SHA-256: `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- Final exact-head workflow settlement after durable-state bookkeeping is still required before independent-review handoff; the Draft PR remains unmerged.

## Gates / handoff

- `module_string_identity_bound=false`.
- `dependency_closure_complete=false`.
- No historical-transclusion provenance is claimed for `Модуль:String@3684569`.
- The direct-call scanner result is not semantic dependency-closure proof.
- forced/non-forced output verification remains open.
- renderer rule promotion remains false.
- literary-body / >=300k admission remains false.
- `fantlab_source_edition_match=unknown`.
- `m2_parity_admissible=false`; M2 remains **0/5**.

Independent review must judge the implementation and exact-head evidence. Binding the observed revision into a successor replay contract remains a separate bounded unit and must not infer historical transclusion provenance from this point-in-time probe.
