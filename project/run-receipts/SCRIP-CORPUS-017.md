# Run receipt — SCRIP-CORPUS-017

Status: `DONE`

Issue: #103  
PR: #104  
Branch: `scrip-corpus-017-klim-samgin`  
Base master: `b88162e58c45821595f5b96649eb52b1b27f7965`  
Reviewed exact head: `69744107743a6c0d7b35199dc8123c92dca2e13c`  
Merged commit: `4240a9df5aae55c84a202327bbae6d3bef97e2df`

## Bounded unit

Qualify Maxim Gorky's *The Life of Klim Samgin* as a twentieth-century, legally usable >=300k provenance lead, preserving the distinction between stable public locators and an actually frozen literary-body identity.

## Evidence captured

- FantLab work `427585`: linguistic analysis dated 2022-09-19, 3,789,857 characters, 531,192 words.
- Russian Wikisource work index: original Russian work marked public domain, Library Moshkov named as electronic source, four-part structure, permanent index locator `oldid=5628161`.
- Literary part permanent locators: Part 1 `oldid=5733765`; Part 2 `oldid=5198033`; Part 3 `oldid=5138882`; Part 4 `oldid=5724453`.
- Part source declarations: GIKhL collected works, Moscow, 1952 vols. 19–21 and 1953 vol. 22.

## Evidence boundary

No source prose is committed. This unit does not have MediaWiki revision timestamps/SHA-1 values or Scriptorium wikitext SHA-256 values for all four part revisions, does not define deterministic literary-body extraction/composition, and has no raw/normalized composite digest. Therefore the lead remains `trace_only`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and is deliberately not added to the main parity catalog yet. M2 remains 0/5.

## Review and repair

Independent exact-head review of authored head `39e068afd78bc77c712f7ca91fbefd9ff5f08a74` accepted the provenance/legal boundary and green CI, but found a blocking public-representation consistency defect: `corpus/candidates/gorky-klim-samgin-ru.md` was not linked from the human-facing `corpus/candidates/README.md` navigation.

The repair added a concise Klim Samgin trace-only section to that README linking both the candidate page and `source-edition-traces/gorky-klim-samgin-ru.json`. It did not add the work to the main parity catalog and did not change any source/parity gate.

## Independent repaired-head verification and merge

- Repaired exact head: `69744107743a6c0d7b35199dc8123c92dca2e13c`.
- PR #104 was mergeable, with 9 commits, 6 changed files and no inline review threads.
- `Scriptorium Pages` run `35175996990` completed successfully.
- `Scriptorium pinned pylem provider` run `35175996991` completed successfully.
- The repaired six-file diff kept README, candidate page, provenance trace, changelog fragment, state and receipt consistent on `trace_only`, source match unknown, diagnostics/gate disabled, no parity-catalog admission and M2 0/5.
- Fresh FantLab verification still reported the retained 19 September 2022 counts: 3,789,857 characters / 531,192 words.
- No source prose, replay-frozen identity claim, parity-catalog admission or FantLab source-match claim was introduced by the repair.
- A later independent review recorded no remaining blocker, marked PR #104 Ready, and squash-merged it as `4240a9df5aae55c84a202327bbae6d3bef97e2df`, closing Issue #103.
