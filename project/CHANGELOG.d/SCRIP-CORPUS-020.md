# SCRIP-CORPUS-020 — Klim Samgin literary-body source graph

- Issue: #109
- Prerequisite PR: #110 — merged as `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`
- Current PR: #111
- Status: `TARGET_ONLY_LST_SEMANTICS_AUTHORED_REVIEW_PENDING`
- Scope: corpus/provenance strengthening and source-graph correctness; no FantLab source-match or M2 promotion.

## Dependency prerequisite

A source-free structural probe of the four pinned Russian Wikisource parent revisions found that Part 2 (`oldid=5198033`) contains a `#lst` reference to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. PR #110 therefore independently pinned that dependency at page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, and SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. No source prose is committed.

PR #110 was independently reviewed on exact head `69811ae047553ffea7bfa89a94d77656ddf30366`; all four relevant exact-head workflows were green before the squash merge. Issue #109 intentionally remained open for semantic/extraction continuation.

## Target-only `#lst` correction — PR #111

Exact-source replay disproved the prior working assumption that Part 2 selected a labeled section. The retained parent contains exactly one target-only invocation: one argument, target `Жизнь Клима Самгина (Горький)/Часть 2/part2`, no section label and no range, at parent offsets `581758..581810`; the exact invocation SHA-256 is `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`.

Current upstream `wikimedia/mediawiki-extensions-LabeledSectionTransclusion` source at evidence commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6` establishes the relevant semantic branch: `setupPfunc12` resolves the target and, when no arguments remain, returns `newFrame->expand(root)`. Therefore this call performs no labeled-section filtering; it delegates the complete target template DOM to MediaWiki frame expansion.

Scriptorium now has a source-free, fail-closed contract at `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`. CI recaptures the exact parent/dependency revisions, regenerates the contract, byte-compares it to the committed record and replays it. The contract intentionally does **not** assert a resolved Part 2 byte identity.

The source-free dependency inventory also found six `poemx1` template invocations and zero `<section>` tags / nested `#lst` calls in dependency oldid `2366546`. This exposes the next real provenance boundary: MediaWiki template-DOM expansion and any transitive template/parser state must be frozen or deterministically reproduced before a resolved Part 2 wikitext/body identity can be claimed.

## Boundary / next trigger

PR #111 was authored in this run and must receive a later independent exact-head review before merge. If accepted, continue Issue #109 by resolving the target-only MediaWiki expansion layer, starting with the observed `poemx1` dependency, then define fail-closed per-part literary extraction and deterministic Part 1 -> Part 2 -> Part 3 -> Part 4 composition before recording raw or `scriptorium-text-v1` composite digests.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.
