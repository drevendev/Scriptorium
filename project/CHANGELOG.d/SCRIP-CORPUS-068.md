# SCRIP-CORPUS-068 — exact `Модуль:String` source-free dependency probe

- Selected the next bounded Darwin/Rachinsky provenance unit from the normal-flow corpus queue after reviewed SCRIP-CORPUS-067 retained `Модуль:String@3684569` as an observed-but-unbound replay candidate.
- Added `scriptorium-darwin-module-string-dependency-probe-v1`, which verifies exact revision title/ID/timestamp/MediaWiki SHA-1 against the reviewed SCRIP-CORPUS-067 observation before inspecting transient Lua source.
- The bounded Lua scanner derives only source byte/digest metadata plus static wiki-module references passed to `require(...)`, `mw.loadData(...)` and `mw.loadJsonData(...)`; comments and ordinary/long strings are ignored, non-wiki require literals are separated, and dynamic/unsupported loader calls make `scan_complete=false`.
- Added six synthetic regressions covering literal wiki dependencies, comments/quoted strings, Lua long strings/comments, dynamic loader fail-closed behavior, non-wiki literals and source-free payload enforcement.
- Added read-only PR CI that fetches exact `Модуль:String@3684569` from Russian Wikisource with `rvprop=ids|timestamp|sha1|content` / `rvslots=main`, builds only the source-free probe, deletes the raw API response, and uploads only the derived JSON artifact.
- Updated the public Darwin direct-dependency companion to expose the new probe boundary without presenting it as a replay binding or historical-transclusion proof.
- Draft PR #225 / Issue #224 carry the authored unit for independent exact-head judgement. `module_string_identity_bound=false`, `dependency_closure_complete=false`, output/renderer/body/>=300k/FantLab/M2 gates remain closed and M2 remains 0/5.
