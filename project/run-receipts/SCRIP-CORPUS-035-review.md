# SCRIP-CORPUS-035 independent-review receipt

Date: 2026-09-20
Issue: #157 (closed completed)
Pull request: #158 (`scrip-corpus-035-darwin-body-contract`, squash-merged)
Mode: recovery / independent exact-head review

## Reviewed state

PR #158 was independently reviewed at exact head **`b78396377612a254dda7605425355b2f435b2e78`** against unchanged base **`c885600f528e2883396d58e14f229824c61b0902`**. The branch was **12 commits ahead / 0 behind**, mergeable, and had no inline review threads.

The earlier review blocker was re-checked specifically. The repaired structured source-edition trace now records the same canonical boundary as `scriptorium-darwin-literary-body-contract-v1`: **418 frozen Page dependencies -> 388 literary dependencies + 30 apparatus dependencies**, with source-declared no-text Page sequences **114** and **411** remaining explicit non-dependencies. Page-wikitext-to-prose rendering, composite separator/body-rendering semantics, literary-body count/digests, >=300k admission, independent scan SHA-256 and FantLab source/M2 gates remain unfrozen or false.

## Exact-head verification

All **15/15** pull-request-triggered workflows on the reviewed SHA completed successfully.

Dedicated `Darwin Rachinsky literary-body contract` workflow run **35482586257**, job **106002941641**, checked out exact head `b78396377612a254dda7605425355b2f435b2e78` and passed contract tests, source-free contract materialization and gate-boundary assertions. Artifact **10596435931** is **1,346 bytes** with digest **`sha256:ce2e734417f45ed18effd563af720af6ad31ae6a27d71e1f21319cb1cb1ae392`**.

`Scriptorium Pages` run **35482586254**, job **106002945937**, also ran on the exact reviewed SHA and passed the standard-library test suite, canonical static build and deterministic rebuild. Live deployment remained skipped by repository configuration.

The 12 changed paths were reviewed by type. No literary source prose, OCR, rendered Page payload, DjVu/PDF bytes or downstream-gate promotion was found.

## Merge result

No blocking defect remained. PR #158 was marked Ready and squash-merged as **`ad2439baa4585759558b5eccb93ae2bf58979f00`**. Issue #157 closed completed.

A post-merge mechanical documentation reconciliation then removed stale Draft/proposed lifecycle wording from the public Darwin/Rachinsky candidate page in commit **`0c36e24c045a4bd89f7665b46ddbec74e6e202fd`**. This did not change analyzer or provenance semantics.

## Canonical boundary after merge

Frozen by SCRIP-CORPUS-035:

- binding to the canonical 418 exact Page revision identities;
- 388 numbered-route literary dependencies from `/1` through `/14` in frozen route/Page order;
- 30 apparatus dependencies consisting of parent-only sequences 8–21 and 423–427 plus alphabetical-index sequences 412–422;
- source-declared no-text 114 and 411 as explicit non-dependencies;
- fail-closed source-free contract generation/validation and structured provenance consistency.

Still unfrozen:

- candidate-specific Page-wikitext-to-prose rendering behavior over the 388 literary dependencies;
- composite separator/body-rendering semantics and final literary-body bytes;
- literary-body character count and raw/normalized digests;
- proof that the rendered literary body clears 300,000 characters;
- independently retrieved DjVu bytes and Scriptorium-computed SHA-256;
- FantLab analyzer-input/source-edition identity for the Rachinsky translation.

Gate status remains `admitted_for_calibration=false`, `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, and `m2_parity_admissible=false`. M2 remains **0/5 source-matched works**.

## Handoff

SCRIP-CORPUS-035 is complete. Resume normal-flow P2 corpus/provenance work. For Darwin/Rachinsky, the next evidence-bearing strengthening is a candidate-specific fail-closed Page-wikitext-to-prose rendering profile over the 388 frozen literary dependencies. Literary-body identity/count/digests and >=300k admission remain a later independent gate.
