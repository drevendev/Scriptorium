# Run receipt — SCRIP-CORPUS-058

- **Unit:** SCRIP-CORPUS-058 — Running on Waves exact-body dialogue-policy sensitivity
- **Issue:** #203 (closed completed)
- **Pull request:** #204 (independently reviewed; squash-merged as `90aa67295e7858a7df46a7cab8b6aac769934a9c`)
- **Base:** `master@063c38fa97215153f43194158c774d6a825c41ad`
- **Authored head:** `31e24f05beb736c7ae504ebdd3c1510c5f8cfda4`
- **Scope:** `drevendev/Scriptorium` only

## Produced

This unit applies the repository's existing diagnostic-only `scriptorium-dialogue-policy-diagnostic-v1` to the already frozen 36-page *Running on Waves* body. It adds an exact-body replay wrapper, focused regressions, a dedicated hosted workflow, the source-free canonical artifact `corpus/candidates/diagnostics/grin-running-on-waves-dialogue-policy.json`, and synchronized candidate/state/changelog surfaces.

The diagnostic is bound to the previously frozen body identity: **363,819 characters**, **656,239 UTF-8 bytes**, SHA-256 **`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`**. Literary source text is fetched only transiently from the exact pinned revisions and is never serialized into the committed diagnostic.

## Hosted evidence

Initial authored-head run `35713185045` at `c6ee6d7b2c2ce4687bfcb859177987c609d94f9c` failed in the new focused test step because the synthetic fixture was too small to satisfy the candidate body's existing >=300,000-character validation floor. This was a fixture defect, not product or source evidence. The fixture was enlarged without changing production analysis behavior.

Repaired hosted run `35713268626` at exact authored SHA `e09ce2b6a63f150aee400aec6241fb4f892c3c4a` passed the focused source-free tests, replayed all 36 exact revisions, verified the canonical body identity, emitted the dialogue-policy diagnostic, passed source-text/parity guards and uploaded source-free artifact `10687625943`. GitHub recorded the artifact ZIP at **1,591 bytes** with digest SHA-256 **`d8163280c9dfdd695f1883a1673488207d428967e7c88450308c4b3f52a007db`**. The archive contains only the generated diagnostic JSON. The canonical JSON committed later on the branch was copied exactly from this successful hosted capture.

Independent exact-head review `5277004834` re-read all 8 changed files at `31e24f05beb736c7ae504ebdd3c1510c5f8cfda4` against unchanged `master@063c38fa97215153f43194158c774d6a825c41ad`. The review found no merge blocker or open review thread, independently reproduced the recorded ratios from the committed counts, and freshly rechecked FantLab work 27344's 18 September 2022 display values. All **17/17** PR-triggered workflow runs on that exact head settled `success`. Dedicated run `35713729969` passed the focused tests, replayed the exact body, compared the regenerated diagnostic byte-for-byte with the committed JSON, passed source/parity guards and uploaded the source-free artifact.

PR #204 was marked Ready and squash-merged with expected-head protection as `90aa67295e7858a7df46a7cab8b6aac769934a9c`. Issue #203 automatically closed as completed.

## Diagnostic observations

The exact body yields:

- dialogue paragraphs: **736**;
- internal separators: **1,215**;
- current-v1 author-remark spans: **706**;
- punctuation-shaped author-remark spans: **571**;
- total non-whitespace characters: **304,345**;
- dialogue non-whitespace characters: **109,229**;
- current-v1 author-remark non-whitespace characters: **37,753**;
- punctuation-shaped author-remark non-whitespace characters: **25,590**.

Against FantLab work `27344`'s displayed **12.49%** author-text-inside-dialogue value, the four inspectable source-unmatched variants are:

- current-v1 remarks / dialogue characters: **34.563165459722235%**, delta **+22.073165459722233 pp**;
- punctuation-shaped remarks / dialogue characters: **23.42784425381538%**, delta **+10.93784425381538 pp**;
- current-v1 remarks / total non-whitespace text: **12.4046723291002%**, delta **-0.08532767089980098 pp**;
- punctuation-shaped remarks / total non-whitespace text: **8.408220933480097%**, delta **-4.081779066519903 pp**.

The same diagnostic reproduces the existing dialogue-share result **35.88986183443132%** versus FantLab's displayed **38.23%** (`-2.340138165568675 pp`).

The near match of `current_v1_over_total_text` is a **denominator hypothesis worth independent investigation**, not recovered FantLab semantics. FantLab's analyzer-input edition/bytes remain undisclosed, and one source-unmatched work cannot distinguish a real denominator rule from compensating source/parser differences. Production `scriptorium-dialogue-v1` is deliberately unchanged.

## Gates / handoff

- `general_calibration_profile_admissible=true`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=true`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5**.

SCRIP-CORPUS-058 is complete. Resume normal-flow selection from the queue. The total-text denominator remains a high-value follow-up hypothesis, but any production-semantics change requires source-matched or multi-work evidence rather than numeric proximity on this source-unmatched work.
