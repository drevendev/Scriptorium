# SCRIP-CORPUS-062 — Beketova deterministic showcase

- Added the first source-free deterministic full-work showcase for Jules Verne's *Children of Captain Grant* in Alexandra A. Beketova's Russian translation, using the already frozen legally usable 1,095,467-character body rather than introducing another source identity.
- The replay builder re-fetches exact Russian Wikisource revision `5304880`, verifies the frozen body SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161`, runs `scriptorium-deterministic-metrics-v4`, and persists only provenance identifiers and derived values.
- The canonical showcase exposes 11 representative metrics across general, dialogue, vocabulary and punctuation surfaces: 158,881 words, 14,568 sentences, 29,084 unique words, 32.4738652575% dialogue share, plus representative length and punctuation rates.
- Added focused fail-closed regressions and a dedicated read-only exact-head replay workflow. Bootstrap run `35763381641` passed 4/4 focused tests, replayed the exact pinned source/body, passed source-free/parity guards, and produced the canonical capture.
- Updated the public candidate page with representative real-work metrics and an explicit interpretation boundary: `fantlab.*` metric IDs remain inferred compatibility candidates, no FantLab comparison was performed, no dictionary-dependent rows are claimed, and no source prose is committed.
- `fantlab_source_edition_match=unknown`, `gate_ready=false`, `m2_parity_admissible=false`; benchmark movement is zero and M2 remains 0/5.
- PR #212 remains Draft for an independent next-wake judgement after exact-final-head CI settles; this authoring run does not self-approve or merge the substantial change.
