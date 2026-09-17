# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #111 — merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`
- Branch: `scrip-corpus-020-klim-lst-semantics`
- Base at selection: `0de8766941bff76e7b20fbd923cd2df95ffbb20b`
- Reviewed exact head: `18d4c2b36e2899e85d44d0166d2fb6f31353d9f9`
- Result: `TARGET_ONLY_LST_SEMANTICS_MERGED_CONTINUATION_OPEN`

## Selected bounded unit

Independently review the exact authored head of PR #111, merge the bounded target-only `#lst` semantic prerequisite if the evidence/checks are clean, and reconcile durable state without closing the larger literary-body Issue #109.

## Review evidence

The exact head was mergeable, 16 commits ahead / 0 behind `master`, changed 11 files, and had no inline review threads. Review re-checked the source-free contract, implementation/tests, public provenance wording, and the pinned upstream `wikimedia/mediawiki-extensions-LabeledSectionTransclusion` source at commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6`. In `setupPfunc12`, after target resolution and template-DOM/frame creation, the zero-remaining-arguments branch returns `newFrame->expand(root)`, supporting the PR's correction from a labeled-section-selection model to a target-only full-template-DOM expansion boundary.

The retained Part 2 source contract remains:

- one target argument; `section_label=null`; `range_end_label=null`
- parent offsets `581758..581810`
- invocation character count `52`, UTF-8 byte count `81`
- invocation SHA-256 `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`
- dependency oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`
- dependency shape: six `poemx1` template invocations, zero nested `#lst` calls, zero `<section>` tags

No source prose is committed, and the contract still sets `mediawiki_template_dom_expansion_reproduced=false`, `resolved_part2_wikitext_identity_frozen=false`, `literary_body_extraction_frozen=false`, and `composite_literary_body_identity_frozen=false`.

## Exact-head verification

All four current exact-head workflows completed successfully:

- Klim Samgin source graph `35214227300`: success; checked out `18d4c2b36e2899e85d44d0166d2fb6f31353d9f9`, ran **188** standard-library tests, re-captured and byte-compared all four parent revision manifests plus dependency oldid `2366546`, replayed all five exact revisions, probed source shape, recaptured/byte-compared/replayed the committed target-only contract, verified source-graph assertions, and uploaded source-free evidence.
- Scriptorium Pages `35214227381`: success.
- Scriptorium frozen diagnostic `35214227330`: success.
- Scriptorium pinned pylem provider `35214227371`: success.

No blocking defect was found in independent judgement. A review receipt was recorded on PR #111 before mutation.

## Merge and public representation

PR #111 was marked Ready and squash-merged as `d3665bfb84ad84c91f5a99c64559267da2e1f41e`. Issue #109 intentionally remains open because this merge is a semantic/source-graph prerequisite, not the requested literary-body composite freeze.

The public Klim candidate page and machine-readable provenance trace now describe the target-only `#lst` edge correctly and expose the six-`poemx1` MediaWiki-expansion boundary without claiming resolved body bytes or FantLab parity.

## Evidence boundary / benchmark movement

The ordered parent source-identity SHA-256 remains `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. No resolved Part 2 or composite literary-body count/digest exists yet.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Next action

Continue Issue #109 in a later bounded unit by freezing or deterministically reproducing the MediaWiki target template-DOM expansion layer, beginning with the six observed `poemx1` invocations and without treating current mutable template state as historical truth. Only after parser/template dependencies replay deterministically should per-part literary extraction, 1 -> 2 -> 3 -> 4 composition, or composite raw / `scriptorium-text-v1` digests be recorded.
