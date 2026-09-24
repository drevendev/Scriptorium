# Run receipt — SCRIP-CORPUS-077

## Selection

- Mode: corpus / provenance research from the queued P2 SCRIP-CORPUS continuation.
- Base: exact `master@a55b5e9ad1d29a5665cfe8915a2c7cb7e3d8f291`.
- Issue: #243.
- Branch: `scrip-corpus-077-darwin-yo-output-replay`.
- Pull request: #244 (Draft; independent later review required).
- Reason: SCRIP-CORPUS-076 independently closed the selected Darwin/Rachinsky three-node `{{ё}}` dependency graph; the queue names controlled forced/non-forced output replay as the next admissible semantic step before any render-profile promotion.

## Produced

- Added deterministic source-free replay contract v6 with contract SHA-256 `c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f`.
- Added a dedicated exact-head workflow that requires the reviewed dependency identities before and after replay, expands both documented modes twice, verifies deterministic semantic outputs, deletes transient provider responses and uploads only source-free evidence.
- Added focused regressions for predecessor identity, identity-window failure, output determinism/digests and downstream gate closure.
- Added a public source-free companion describing the replay method, positive evidence target and proof boundary.

## Evidence contract

The selected replay graph remains exactly:

```text
Шаблон:Ё@5687302 -> Шаблон:ЕЁ@3684646 -> Модуль:String@3684569
```

The hosted proof must observe those exact current revisions both before and after replay. It does not use MediaWiki `revid` as a recursive dependency selector and does not claim historical transclusion provenance or a general offline/version-pinned MediaWiki runtime.

Mode targets after explicit Unicode NFC + surrounding-whitespace normalization are:

- forced Darwin `(ВТ:Ё)` context -> `ё`, SHA-256 `30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac`;
- non-forced Darwin base context -> `е`, SHA-256 `259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26`.

## Verification / handoff

- Draft PR #244 is the review surface. Exact-head PR-triggered CI must settle before independent judgement.
- The dedicated output-replay workflow is the provider evidence path: deterministic v6 rebuild plus an identity-stable before/replay/after sequence and a source-free receipt artifact.
- A later wake must independently re-read every changed file at the exact final PR head, inspect the output-replay job/log/artifact and all other required checks, and verify that the provider identities and both semantic output digests match the committed contract.
- If clean and `master` remains compatible, that later wake may mark the PR Ready and squash-merge with expected-head protection. This authoring wake must not self-approve or self-merge the substantive change.

## Gates

Review-pending v6 narrows only zero-argument `{{ё}}` semantics. Render-profile mutation is deliberately deferred: `render_profile_rule_promoted=false` and `backlog_item_removed=false`. Complete renderer semantics/implementation, inter-page composition, literary-body identity, >=300k admission, FantLab analyzer-input identity and M2 parity remain closed; M2 stays 0/5.

## Independent review / merge

- A later wake independently re-read all eight changed files at exact final PR head `822e72635b62aee5cc4cba60fa150a6a9dadd22f` against unchanged `master@a55b5e9ad1d29a5665cfe8915a2c7cb7e3d8f291`; there were no open review threads or merge blockers.
- Review `5298593294` records the exact-head judgement and proof boundary. All 23 PR-triggered workflow runs associated with the reviewed head completed successfully.
- Dedicated output-replay run `35941337473` checked out the exact reviewed head, passed 7/7 focused regressions, rebuilt v6 byte-for-byte and verified the before/replay/after identity-stable window. It reproduced forced digest `30fbc377ae9122edc2cdbed70b9261817d196eca8db96ac8bfa4cfaf412667ac` and non-forced digest `259f56cb715ba3a3f1ca41a4ff1972cca698cb49eef1ae018dff325507da8b26`.
- Source-free artifact `10784458609` independently matched GitHub ZIP SHA-256 `28ead6d946e6664a7b34f61f692ff2b5b95731fd6e1988b678cbc08629f32326`. The v6 contract self-digest recomputed as `c317eb5247701f0ad860811e9349f4e6f42274e72e8856eecb8a9aff610f988f`, and the replay receipt self-digest recomputed as `42f232a350c23c8dea09f58434f08785309bc8a5f748f39d2195fb36dc21d1b1`.
- Frozen-diagnostic run `35941337352` checked out the same exact head and passed the full 561/561 standard-library suite.
- PR #244 was marked Ready and squash-merged with expected-head protection as `93de18df4905b8475fd53aa96fafb47b759567c0`; Issue #243 closed `completed`.
- The accepted evidence remains intentionally narrow: v6 verifies only zero-argument `{{ё}}` forced/non-forced semantics for the selected identity-stable live snapshot. Historical transclusion, an offline/version-pinned MediaWiki runtime, render-profile promotion/backlog removal, complete renderer semantics/implementation, inter-page composition, literary-body identity, >=300k admission, FantLab analyzer-input identity and M2 parity remain unproved. M2 remains 0/5.
