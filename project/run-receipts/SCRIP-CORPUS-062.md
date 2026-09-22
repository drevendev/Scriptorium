# Run receipt — SCRIP-CORPUS-062

- **Unit:** SCRIP-CORPUS-062 — Beketova deterministic full-work showcase
- **Issue:** #211 (closed completed on merge)
- **Pull request:** #212 (independently reviewed; squash-merged as `0b9d838bfa5c9844dbf1b503b806c31eed25404c`)
- **Base:** `master@c7c09a9e4bbeeb55f23e87903c6b64e71f361d88`
- **Reviewed head:** `62f0b2921ffc4a662d7e0e2a0f4adf547233688d`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This unit turns the already frozen, legally usable >=300k body of Jules Verne's *Children of Captain Grant* in Alexandra A. Beketova's Russian translation into a concrete public Scriptorium analysis slice.

The `scriptorium-beketova-deterministic-showcase-v1` builder transiently re-fetches exact Russian Wikisource revision `5304880`, verifies its frozen source identity, re-extracts the literary body with `scriptorium-beketova-captain-grant-wikisource-body-v1`, and verifies the exact 1,095,467-character body / SHA-256 `4931eba535a4ef3989ac905d895258f00db57029e488d98511db50a7ce4d1161` before analysis. Source prose remains in process memory only.

The canonical derived artifact stores 11 representative values from `scriptorium-deterministic-metrics-v4`, including:

- 1,095,467 characters;
- 158,881 words;
- 14,568 sentences;
- mean word length 5.534330725511547 characters;
- mean sentence length 73.84287479406919 characters;
- dialogue share 32.4738652575157%;
- current-policy author text inside dialogue 26.463343499491693%;
- 29,084 unique words;
- comma / dash / question rates of 119.31571427672283 / 45.59387214330222 / 7.036713011625053 per 1,000 words.

The public candidate page links the canonical source-free artifact and labels the output as Scriptorium analysis rather than FantLab evidence. Dictionary-dependent vocabulary values are deliberately not included because no compatible dictionary provider is bound.

## Verification contract

Dedicated bootstrap run `35763381641` checked out authored head `5fecffa2ed515001107a0b3325de1a964fa9f712`, passed **4/4** focused standard-library regressions, re-fetched the exact pinned revision, verified the exact frozen body, emitted the source-free artifact, and passed closed-gate guards. The bootstrap artifact was then committed as the canonical JSON so the final-head run could enforce byte-for-byte `cmp` rather than capture-only behavior.

Independent review `5282257475` re-read all 8 changed files at exact final head `62f0b2921ffc4a662d7e0e2a0f4adf547233688d` against unchanged `master@c7c09a9e4bbeeb55f23e87903c6b64e71f361d88`, confirmed the branch was 8 commits ahead / 0 behind with no open review threads, and found no merge blocker.

All **20/20** pull-request-triggered workflows on the exact reviewed head completed with `success`. Dedicated run `35763976181` was anchored to that head and completed focused tests, exact pinned-revision/body replay, byte-for-byte canonical artifact comparison, source-free/parity guards, and artifact upload successfully. The full pinned-pylem provider workflow also completed successfully.

PR #212 was marked Ready and squash-merged with expected-head protection as `0b9d838bfa5c9844dbf1b503b806c31eed25404c`, automatically closing Issue #211 as completed.

## Gates / final state

- `general_calibration_profile_admissible=true`
- `source_text_committed=false`
- `showcase_ready=true`
- `fantlab_comparison_performed=false`
- `fantlab_source_edition_match=unknown`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5**.

The bounded unit is complete. No benchmark/parity gate moved; the durable queue may resume normal-flow corpus/provenance selection.