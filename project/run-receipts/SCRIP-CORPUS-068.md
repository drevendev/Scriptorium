# Run receipt — SCRIP-CORPUS-068

- **Unit:** SCRIP-CORPUS-068 — exact `Модуль:String` source-free dependency probe
- **Issue:** #224 (open)
- **Pull request:** #225 (Draft; independent review pending)
- **Authoring base:** `master@5aac605ec0a222c60f5fbf60910fa999d664e7c0`
- **Branch:** `work/SCRIP-CORPUS-068-module-string-probe`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This bounded unit advances the reviewed SCRIP-CORPUS-067 point-in-time observation without prematurely turning it into historical provenance or a bound replay edge. The new probe verifies exact `Модуль:String@3684569` metadata against the committed observation before inspecting source content, then emits only source-free derived metadata.

The Lua dependency-surface scanner records UTF-8 byte count, SHA-1/SHA-256 digests, static wiki-module literals supplied to `require`, `mw.loadData`, or `mw.loadJsonData`, non-wiki require literals, and any dynamic/unsupported loader-call classes. Comments plus ordinary/long strings are skipped so loader-looking text there cannot create false dependencies. Any dynamic/unsupported loader argument makes `scan_complete=false`.

PR CI fetches the exact observed revision with `rvprop=ids|timestamp|sha1|content` and `rvslots=main`, verifies title/revision/timestamp/SHA-1 before scanning, deletes the raw response after producing the derived JSON, and uploads only that source-free artifact.

## Verification

- Local isolated `unittest` execution of the new scanner tests passed **6/6** before repository writes.
- PR-triggered exact-head workflow verification is required before authoring handoff is considered complete; the Draft PR remains unmerged pending that evidence and independent judgement.

## Gates / handoff

- `module_string_identity_bound=false`.
- `dependency_closure_complete=false`.
- No historical-transclusion provenance is claimed for `Модуль:String@3684569`.
- forced/non-forced output verification remains open.
- renderer rule promotion remains false.
- literary-body / >=300k admission remains false.
- `fantlab_source_edition_match=unknown`.
- `m2_parity_admissible=false`; M2 remains **0/5**.

After PR CI settles, reconcile the exact live source-free probe result into this receipt/state. Independent review must decide whether the probe implementation/evidence is trustworthy; binding the observed revision into a successor replay contract remains a separate bounded unit.
