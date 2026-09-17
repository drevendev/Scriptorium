# SCRIP-CORPUS-020 — Klim Samgin literary-body source graph

- Issue: #109
- Prerequisite PR: #110 — merged as `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`
- Target-only semantics PR: #111 — merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`
- Status: `TARGET_ONLY_LST_SEMANTICS_MERGED_CONTINUATION_OPEN`
- Scope: corpus/provenance strengthening and source-graph correctness; no FantLab source-match or M2 promotion.

## Dependency prerequisite

A source-free structural probe of the four pinned Russian Wikisource parent revisions found that Part 2 (`oldid=5198033`) contains a `#lst` reference to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. PR #110 therefore independently pinned that dependency at page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, and SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. No source prose is committed.

PR #110 was independently reviewed on exact head `69811ae047553ffea7bfa89a94d77656ddf30366`; all four relevant exact-head workflows were green before the squash merge. Issue #109 intentionally remained open for semantic/extraction continuation.

## Target-only `#lst` correction — PR #111

Exact-source replay disproved the prior working assumption that Part 2 selected a labeled section. The retained parent contains exactly one target-only invocation: one argument, target `Жизнь Клима Самгина (Горький)/Часть 2/part2`, no section label and no range, at parent offsets `581758..581810`; the exact invocation SHA-256 is `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`.

Current upstream `wikimedia/mediawiki-extensions-LabeledSectionTransclusion` source at evidence commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6` establishes the relevant semantic branch: `setupPfunc12` resolves the target and, when no arguments remain, returns `newFrame->expand(root)`. Therefore this call performs no labeled-section filtering; it delegates the complete target template DOM to MediaWiki frame expansion.

Scriptorium now has a source-free, fail-closed contract at `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`. CI recaptures the exact parent/dependency revisions, regenerates the contract, byte-compares it to the committed record and replays it. The contract intentionally does **not** assert a resolved Part 2 byte identity.

The source-free dependency inventory also found six `poemx1` template invocations and zero `<section>` tags / nested `#lst` calls in dependency oldid `2366546`. This exposes the next real provenance boundary: MediaWiki template-DOM expansion and any transitive template/parser state must be frozen or deterministically reproduced before a resolved Part 2 wikitext/body identity can be claimed.

## Independent review and merge

PR #111 exact head `18d4c2b36e2899e85d44d0166d2fb6f31353d9f9` received an independent later-run review with no blocking defect. It was 16 commits ahead / 0 behind `master`, changed 11 files, and had no inline review threads. Exact-head workflows `35214227300` (Klim source graph), `35214227381` (Pages), `35214227330` (frozen diagnostic), and `35214227371` (pinned pylem provider) all completed successfully. The Klim workflow ran 188 standard-library tests and replayed all five pinned revisions plus the committed target-only contract. The review also re-read the pinned upstream `LabeledSectionTransclusion.php` evidence and confirmed the cited zero-remaining-arguments branch.

PR #111 was then marked Ready and squash-merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`. Issue #109 intentionally remains open.

## Boundary / next trigger

Continue Issue #109 by freezing or deterministically reproducing the target-only MediaWiki template-DOM expansion layer, starting with the observed six `poemx1` invocations. Do not treat current mutable template state as historical truth. Only after those parser/template dependencies replay deterministically should resolved Part 2 bytes, fail-closed per-part literary extraction, deterministic Part 1 -> Part 2 -> Part 3 -> Part 4 composition, or raw / `scriptorium-text-v1` composite digests be recorded.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.
