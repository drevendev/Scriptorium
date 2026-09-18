# Run receipt — SCRIP-CORPUS-020 literary-body identity capture

Date: 2026-09-18
Issue: #109
Draft PR: #127
Baseline master: `514881dab01549dad94772a52cc64b0af7b231b9`

## Bounded unit

Independently capture the previously generated source-free four-part literary-body identity only after verifying the exact PR #126 replay artifact, then place the canonical manifest under repository control with a regression and leave the substantive provenance change as Draft for later judgement.

## Evidence recovered

The independently reviewed PR #126 exact-head workflow run `35340846781`, job `105586149163`, checked out `d589a9070b1a830c67b8800ddc9f7abf2d876a4c`, ran 254 standard-library tests successfully, re-fetched all five pinned revisions, generated the source-free literary-body manifest and uploaded artifact `10545296253`.

The downloaded artifact ZIP verifies as SHA-256 `717177464f00e51915cd65d661cb428d22210bb1f7b5055c4a813f0777ae6193`. Its sole contained file, `gorky-klim-samgin-ru.literary-body.observed.json`, verifies as SHA-256 `8057605ce3d8f547c7091647f5315662b1d8d9c04b94b7b16f7fbacf80b7499f`. The committed canonical manifest is byte-for-byte that file.

## Captured identity

- Part 1: 964,215 characters / 1,744,650 UTF-8 bytes; raw and normalized SHA-256 `1a41cef4b2383a149077da372d9a44ab48c3b2616064da6c1ab5f01a6062f4c8`.
- Part 2: 1,164,870 / 2,111,745; SHA-256 `75896b6a0a87bc10087ececbeb919077de58c628f646aab8994cf653edc15794`.
- Part 3: 680,940 / 1,234,441; SHA-256 `7dc6030381371cdcff5a27a872ab1fd6c49840655e3ce11a45d647ea0bf208ab`.
- Part 4: 1,000,587 / 1,868,088; SHA-256 `237b2119e04bdf8c02dded3d138fda457d8f423012d2abe9d752a07c038c8948`.
- Composite: Parts `1 -> 2 -> 3 -> 4`, separator `\n\n`, 3,810,618 characters / 6,958,930 UTF-8 bytes; raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`.

## Production

- Added `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.literary-body.json` from the verified artifact without source prose.
- Added a focused regression proving the committed manifest remains source-free, `candidate_specific_inferred_reconstruction`, FantLab-source-unknown, gate-closed and M2-inadmissible.
- Opened Draft PR #127. The existing dedicated workflow is expected to re-fetch the exact source graph on the PR head, regenerate the manifest, byte-compare it against the committed canonical file and run replay validation.

## Boundary

This capture freezes Scriptorium's candidate-specific inferred reconstruction, not historical Russian Wikisource render equivalence. Exact historical MediaWiki-core/Poem deployment identity and FantLab analyzer-input identity remain unknown. No parity metric is promoted and **M2 remains 0/5**.

## Next trigger

Independent later-run review of Draft PR #127 after its exact-head checks finish. Merge only if the dedicated replay regenerates the committed manifest byte-for-byte and the full required check set is green; then synchronize the public Klim provenance page/trace and queue state as merged canonical evidence.
