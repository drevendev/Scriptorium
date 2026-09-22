# Run receipt — SCRIP-CORPUS-057

- **Unit:** SCRIP-CORPUS-057 — Running on Waves source-free full-work diagnostic
- **Issue:** #201
- **Pull request:** #202 (Draft; independent review required)
- **Base:** `master@35669c62e24743d005163421283f4fb489ea2b68`
- **State handoff parent:** `2ebd84f7653c21453c521436dc3ed494256bfce1`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This run added `scriptorium.running_waves_diagnostic`, five focused regressions, a dedicated exact-body replay workflow, the committed source-free diagnostic artifact `corpus/candidates/diagnostics/grin-running-on-waves-ru.json`, and synchronized candidate/provenance/state/changelog surfaces.

The diagnostic is cryptographically bound to the previously frozen 36-page Running on Waves body: **363,819 characters**, **656,239 UTF-8 bytes**, SHA-256 **`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`**. Literary source text is fetched only transiently from the exact pinned revisions and is not committed or uploaded as an artifact.

## Hosted evidence

Authored-head workflow run `35702370659` checked out exact SHA `091e89e2e9d08c7353b31d792deecac5877bec0f`, passed all **5/5** focused tests, replayed the exact frozen public body, verified the body identity guard, emitted **27** source-free comparison rows, passed the no-source-text/parity-boundary guard, and uploaded only a **1,822-byte** source-free diagnostic artifact (artifact `10681979014`; ZIP SHA-256 `65951f3006f98ed69e4470079400c1b24f4b9078a4d8d7806db8e2993626b973`). The canonical JSON committed later on this branch was copied exactly from that successful hosted capture; final-head CI must independently prove deterministic regeneration by `cmp` before merge.

Two earlier authored heads failed the new focused workflow because of test-fixture defects, not product/source evidence: the first test referenced `literary_pages` instead of the source manifest's actual `pages` key; the next synthetic fixture contained no dialogue and therefore could not exercise non-null dialogue metrics. Both fixture defects were corrected before the successful exact-body capture.

## Diagnostic observations

FantLab work `27344` publicly displays its 18 September 2022 analysis, including **360,987 characters** and **52,985 words**, but does not disclose exact analyzer-input bytes or an edition identity. The retained diagnostic therefore classifies every numeric comparison as `diagnostic_only_source_unmatched` unless a dependency is unbound.

Selected observed Scriptorium values/deltas from the exact frozen public body:

- characters: `363819`, delta `+2832`;
- words: `55778`, delta `+2793`;
- mean word length: `5.159363906916705`, display delta `-0.000636093083295`;
- dialogue share: `35.88986183443132`, display delta `-2.34013816556868` percentage points;
- author text inside dialogue: `34.563165459722235`, display delta `+22.073165459722235` percentage points;
- unique words: `14406`, delta `+7299`;
- comma frequency: `143.67671841944852`, display delta `-10.35328158055148` per 1,000 words;
- dash frequency: `39.87235110617089`, display delta `+10.03235110617089` per 1,000 words.

`active_dictionary`, `active_nondictionary`, `uasz_3000`, and `uasz_10000` are explicitly `not_run_dependency_unbound`; no compatible dictionary was assumed.

## Gates / handoff

- `general_calibration_profile_admissible=true`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=true`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5**.

This authored run does **not** mark PR #202 Ready and does not merge it. The next wake must independently re-read the PR's current exact head, inspect changed files and exact-head CI, verify that the committed diagnostic deterministically replays and remains source-free, and only then decide whether Ready/merge is warranted.
