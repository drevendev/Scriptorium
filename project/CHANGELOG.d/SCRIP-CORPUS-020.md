# SCRIP-CORPUS-020 — Klim Samgin literary-body source graph

- Issue: #109
- Prerequisite PR: #110 — merged as `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`
- Target-only semantics PR: #111 — merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`
- Historical `poemx1` anchor PR: #112 — merged as `aae7290f6056831bd291ac8a7a59100bad0ff4e8`
- Inclusion-control PR: #113 — merged as `5894878398a8ceba952279c69aaf9b5ab8ebae81`
- Literal parameter-surface PR: #114 — draft; independent review pending
- Status: `POEMX1_PARAMETER_SURFACE_AUTHORED_REVIEW_PENDING`
- Scope: corpus/provenance strengthening and source-graph correctness; no FantLab source-match or M2 promotion.

## Dependency prerequisite

A source-free structural probe of the four pinned Russian Wikisource parent revisions found that Part 2 (`oldid=5198033`) contains a `#lst` reference to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. PR #110 therefore independently pinned that dependency at page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, and SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`. No source prose is committed.

PR #110 was independently reviewed on exact head `69811ae047553ffea7bfa89a94d77656ddf30366`; all four relevant exact-head workflows were green before the squash merge. Issue #109 intentionally remained open for semantic/extraction continuation.

## Target-only `#lst` correction — PR #111

Exact-source replay disproved the prior working assumption that Part 2 selected a labeled section. The retained parent contains exactly one target-only invocation: one argument, target `Жизнь Клима Самгина (Горький)/Часть 2/part2`, no section label and no range, at parent offsets `581758..581810`; the exact invocation SHA-256 is `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`.

Current upstream `wikimedia/mediawiki-extensions-LabeledSectionTransclusion` source at evidence commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6` establishes the relevant semantic branch: `setupPfunc12` resolves the target and, when no arguments remain, returns `newFrame->expand(root)`. Therefore this call performs no labeled-section filtering; it delegates the complete target template DOM to MediaWiki frame expansion.

Scriptorium now has a source-free, fail-closed contract at `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`. CI recaptures the exact parent/dependency revisions, regenerates the contract, byte-compares it to the committed record and replays it. The contract intentionally does **not** assert a resolved Part 2 byte identity.

The source-free dependency inventory also found six `poemx1` template invocations and zero `<section>` tags / nested `#lst` calls in dependency oldid `2366546`. This exposes the next real provenance boundary: MediaWiki template-DOM expansion and any transitive template/parser state must be frozen or deterministically reproduced before a resolved Part 2 wikitext/body identity can be claimed.

## Independent review and merge — PR #111

PR #111 exact head `18d4c2b36e2899e85d44d0166d2fb6f31353d9f9` received an independent later-run review with no blocking defect. It was 16 commits ahead / 0 behind `master`, changed 11 files, and had no inline review threads. Exact-head workflows `35214227300` (Klim source graph), `35214227381` (Pages), `35214227330` (frozen diagnostic), and `35214227371` (pinned pylem provider) all completed successfully. The Klim workflow ran 188 standard-library tests and replayed all five pinned revisions plus the committed target-only contract. The review also re-read the pinned upstream `LabeledSectionTransclusion.php` evidence and confirmed the cited zero-remaining-arguments branch.

PR #111 was then marked Ready and squash-merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`. Issue #109 intentionally remains open.

## Historical `poemx1` revision anchor — PR #112

The next bounded continuation does not attempt to emulate MediaWiki expansion from today's mutable template state. Instead, `scriptorium/template_history.py` introduces a source-free historical-template revision resolver whose explicit policy is **latest revision not later than the pinned page-save timestamp**. The policy is labeled `inferred_reconstruction_anchor` and hard-codes neither render equivalence nor template expansion success.

Applied to `Шаблон:Poemx1` using pinned Part 2 oldid `5198033` / timestamp `2024-11-26T11:16:35Z`, live CI resolves:

- page ID `54236`
- template oldid `5142743`
- revision timestamp `2024-06-02T02:25:12Z`
- MediaWiki SHA-1 `7b7da0fa04913bc902f6455addad437fc19d67d8`
- 2,412 wikitext characters / 2,918 UTF-8 bytes
- wikitext SHA-256 `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`

The immutable source-free manifest is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.revision.json`. Replay re-runs the as-of resolver and separately fetches the exact pinned oldid, so future revision-selection drift and byte drift both fail closed.

A corrected source-shape probe deliberately excludes triple-brace parameters and separates parser functions/magic words from ordinary `{{...}}` openings. For oldid `5142743` it records one raw ordinary template-shaped invocation (`doc`), `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1, `PAGENAME` x1, and HTML-like tags `div` x6, `includeonly` x2, `noinclude` x4, `templatedata` x2. The committed shape artifact explicitly says this is raw source inventory only: inclusion semantics have not yet been applied, and no effective transitive dependency graph is claimed.

The first capture workflow run `35223860049` succeeded and ran 192 standard-library tests while establishing the exact template identity. A later strict replay attempt correctly exposed a hand-copied source-URL typo in the newly authored manifest after the test/capture/probe steps had passed; the manifest was repaired and CI was converted to require byte-for-byte manifest and shape comparison plus exact replay.

## Independent review and merge — PR #112

PR #112 exact head `4626bbeb0b99c12dd78c5d1b4e45e5a04581d72d` received an independent later-run review with no blocking defect. It was 14 commits ahead / 0 behind `master`, changed 9 files, was mergeable, and had no inline review threads. Exact-head workflows `35224478878` (Klim historical template dependency), `35224478838` (Pages), `35224478864` (frozen diagnostic), and `35224478848` (pinned pylem provider) all completed successfully. The dedicated Klim run checked out the exact reviewed SHA, ran 192 standard-library tests, re-resolved the as-of `poemx1` revision, byte-compared the committed revision/shape evidence, and replayed exact oldid `5142743`.

The review found the evidence boundary intact: the revision is still only an `inferred_reconstruction_anchor`; `historical_render_equivalence_proven=false` and `template_expansion_reproduced=false`; the raw shape probe does not claim inclusion semantics or an effective dependency graph. PR #112 was marked Ready and squash-merged as `aae7290f6056831bd291ac8a7a59100bad0ff4e8`. Issue #109 intentionally remains open.

## Inclusion-control semantics — PR #113

PR #113 applied and replay-froze only documented MediaWiki `noinclude` / `includeonly` / `onlyinclude` selection semantics for pinned `poemx1` oldid `5142743`. The exact revision has two `noinclude` pairs, one `includeonly` pair and zero `onlyinclude` pairs. After selection, the raw `doc` invocation and raw `PAGENAME` occurrence disappear. The remaining source-free graph is `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1 and `#tag` x1 targeting `poem`, with no ordinary templates or magic words.

An authored-head CI comparison caught an incorrect hand-authored expectation that `PAGENAME` remained in the effective graph. The artifact and wording were repaired from generated evidence. Independent later-run review used exact head `0ecc213bed00e0d3d6a07cfc9df5b61531cd38c6`; all five required workflows were green, no blocking defect was found, and PR #113 was squash-merged as `5894878398a8ceba952279c69aaf9b5ab8ebae81`. Issue #109 remained open.

## Literal template-parameter surface — draft PR #114

The next bounded layer implements only literal triple-brace parameter/default semantics after the already-frozen inclusion selection. Official MediaWiki documentation distinguishes an omitted parameter from a parameter explicitly defined as empty: a missing parameter may use a default, while an explicitly empty argument is defined and suppresses that default. Scriptorium's bounded profile reproduces that distinction for literal parameter names, supports nested literal parameter defaults, leaves a missing parameter without a default as its original triple-brace spelling, and fails closed on dynamic/unsupported parameter-name shapes rather than guessing them. Inserted argument values are not recursively parsed by this layer.

Live exact-source generation on authored head `99031deb1ecf10358e8b94bbd65a4b5be7de138b` established post-inclusion input SHA-256 `86ad628a9d8fc3d904fd513a1b4335f4e9f816ceedfa2af736e8e3a94e32ffbf` and a source-free parameter surface of **21 references**:

- `1` x2
- `2` x1
- `3` x2
- `fixed` x6
- `poem` x1
- `small` x6
- `width` x3

All except one bare `fixed` reference have defaults. Empty defaults occur for `1` x2, `2` x1, `3` x2, `fixed` x1, `poem` x1 and `width` x1. The committed source-free artifact is `gorky-klim-samgin-ru.poemx1-template.parameters.json`.

The first authored-head workflow exposed one over-specific new unit-test expectation: a dynamic/malformed brace form failed closed earlier in the structural parser with `unclosed MediaWiki brace construct` rather than the exact later validation message the test expected. The test was corrected to assert the actual contract—`ValueError` fail-closed behavior—without weakening acceptance. The next dedicated run `35249215580` checked out exact head `99031deb1ecf10358e8b94bbd65a4b5be7de138b`, passed **205** standard-library tests, regenerated the historical revision/raw-shape/inclusion layers and generated the parameter artifact; it then stopped at the intentionally absent expected parameter artifact. That generated artifact was used as the source for the committed source-free record. Final exact-head replay is required before independent review.

PR #114 deliberately does **not** bind the six real `poemx1` invocations, recursively expand inserted argument wikitext, execute `#expr` / `#if` / `#ifeq` / `#iferror`, render `#tag:poem`, resolve Part 2, or claim historical render equivalence.

## Boundary / next trigger

Independent later-run exact-head review of draft PR #114 and all required checks preempts new work. If clean, merge this prerequisite without closing Issue #109. Then continue by source-freezing the six concrete `poemx1` invocation argument shapes and only afterward reproduce the evidenced parser-function / `#tag:poem` behavior. Resolved Part 2 bytes, four-part literary extraction/composition, and raw / `scriptorium-text-v1` composite digests remain prohibited until the target-only expansion layer replays deterministically.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.
