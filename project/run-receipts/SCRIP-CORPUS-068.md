# Run receipt — SCRIP-CORPUS-068

- **Unit:** SCRIP-CORPUS-068 — exact `Модуль:String` source-free dependency probe
- **Issue:** #224 (closed completed)
- **Pull request:** #225 (independently reviewed; squash-merged as `20ec832fbfef87f5a910d77088f5f429f4161645`)
- **Authoring base:** `master@5aac605ec0a222c60f5fbf60910fa999d664e7c0`
- **Final reviewed head:** `223e3a1bc896eaaae7f625349e7ddc09a9908a18`
- **Branch:** `work/SCRIP-CORPUS-068-module-string-probe`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded unit advances the reviewed SCRIP-CORPUS-067 point-in-time observation without prematurely turning it into historical provenance or a bound replay edge. The probe verifies exact `Модуль:String@3684569` metadata against the committed observation before inspecting source content, then emits only source-free derived metadata.

The Lua dependency-surface scanner records UTF-8 byte count, SHA-1/SHA-256 digests, static wiki-module literals supplied to direct `require`, `mw.loadData`, or `mw.loadJsonData` calls, non-wiki require literals, and any dynamic/unsupported direct loader-call classes. Comments plus ordinary/long strings are skipped so loader-looking text there cannot create false dependencies; Lua's bare quoted function-call form is handled and unsupported long-string/dynamic calls fail closed. The artifact explicitly records that alias/computed semantic analysis is outside this scanner's bounded scope and therefore `semantic_dependency_closure_proved=false`.

PR CI fetches the exact observed revision with `rvprop=ids|timestamp|sha1|content` and `rvslots=main`, verifies title/revision/timestamp/SHA-1 before scanning, deletes the raw response after producing the derived JSON, and uploads only that source-free artifact.

## Verification

- Synthetic scanner coverage has **9** regressions; exact-head PR CI also ran the existing dependency-observation regressions for **15 tests total**, all passing.
- Exact-head probe run `35835760189` checked out `223e3a1bc896eaaae7f625349e7ddc09a9908a18` and completed `success`.
- All **22/22** PR-triggered workflows on the exact reviewed head settled `success` before review/merge.
- Exact identity remained `Модуль:String@3684569`, revision timestamp `2019-06-04T20:18:11Z`, MediaWiki SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`.
- Transient exact source measured **18,468 UTF-8 bytes**, SHA-1 `a34727a1e4ec3c4b4c7ec556c94991f75442d99c`, SHA-256 `258cec6ab8b4c1e3eb0e812d72d39f4302f321a4d1fdd7aa3883187db0eecb03`.
- Bounded direct-loader scan found **no static wiki-module dependencies**, **no non-wiki require literals**, and **no dynamic/unsupported direct loader calls**; `scan_complete=true` only for that stated direct-call scan scope, while `semantic_dependency_closure_proved=false` remains explicit.
- Source-free probe SHA-256: `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.
- Independent review downloaded the exact-head artifact and recomputed its canonical-object digest (excluding its self-digest field); the result matched `e27a2af9f01c760f995c633e296e1d5825642d4c4bcbeb5fba8ae0a697c234cb`.

## Independent review / merge

- Review `5288837999` independently re-read all **7 changed files** plus the exact-head source-free workflow artifact and found no merge-blocking correctness defect or open review thread.
- The unchanged merge base immediately before judgement was `master@5aac605ec0a222c60f5fbf60910fa999d664e7c0`.
- PR #225 was marked Ready and squash-merged with expected-head protection on `223e3a1bc896eaaae7f625349e7ddc09a9908a18` as `20ec832fbfef87f5a910d77088f5f429f4161645`.
- Issue #224 closed automatically as `completed`.

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

SCRIP-CORPUS-068 is complete. Resume normal-flow selection from the canonical queue. Any later binding of the observed module identity into a successor replay contract is a separate bounded unit and must not reinterpret this point-in-time observation/probe as historical transclusion provenance.
