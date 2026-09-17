# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #111 (Draft)
- Branch: `scrip-corpus-020-klim-lst-semantics`
- Base at selection: `0de8766941bff76e7b20fbd923cd2df95ffbb20b`
- Result: `TARGET_ONLY_LST_SEMANTICS_AUTHORED_REVIEW_PENDING`

## Selected bounded unit

Continue Issue #109 by resolving and freezing the exact Part 2 `#lst` selection/placement semantics before attempting literary-body extraction or composition. The unit must remain source-free, fail closed on source drift, and must not tune anything toward FantLab's displayed count.

## Discovery and correction

The first implementation assumed a normal labeled-section call. Exact-source CI disproved that assumption. A source-free structural artifact from pinned parent oldid `5198033` showed exactly one `#lst` prefix, one argument, target `Жизнь Клима Самгина (Горький)/Часть 2/part2`, parent offsets `581758..581810`, and **no section argument**. The pinned dependency oldid `2366546` contains zero `<section>` markers.

Upstream implementation research then checked `wikimedia/mediawiki-extensions-LabeledSectionTransclusion`, file `includes/LabeledSectionTransclusion.php`, at evidence commit `3e9a44dec6858aeaf3ca547a32ab3162d6887ed6`. In `setupPfunc12`, after the target has been resolved and the target template DOM/frame created, the zero-remaining-arguments branch returns `newFrame->expand(root)`. Therefore the retained invocation performs no labeled-section selection: it delegates the whole target template DOM to MediaWiki frame expansion.

The implementation was corrected rather than forcing the earlier hypothesis. `scriptorium-klim-samgin-lst-contract-v2` now requires exactly one target-only call and records its source-free placement/identity plus the pinned dependency and upstream semantic branch. The committed contract is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.part2-lst.json`.

Exact observed invocation evidence:

- one argument; `section_label=null`; `range_end_label=null`
- parent offsets `581758..581810`
- invocation character count `52`, UTF-8 byte count `81`
- invocation SHA-256 `89969a0424eb9fa332d132216bbeb96647239ab613cf6dadf6c5e2087ff0f15e`
- dependency oldid `2366546`, wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`

The same source-free contract inventory found **six `poemx1` template invocations** in the dependency, zero nested `#lst` calls and zero section tags. That is a new explicit boundary: the target revision and parser-function semantic branch are frozen, but MediaWiki template-DOM expansion and any transitive template/parser state are not yet reproduced. No resolved Part 2 byte identity is claimed.

## Verification

Bootstrap corrected-head Klim run `35213791952` completed successfully. It:

- ran the full standard-library suite successfully;
- re-captured and byte-compared all four parent revision manifests plus dependency oldid `2366546`;
- replayed all five exact revisions;
- ran source-free source-shape probes;
- captured the corrected target-only contract successfully;
- verified the ordered parent source-identity digest and fail-closed M2 flags;
- uploaded source-free evidence.

The observed contract from that run was inspected before being committed. It records `template_name_counts={"poemx1": 6}` and deliberately sets `mediawiki_template_dom_expansion_reproduced=false`, `resolved_part2_wikitext_identity_frozen=false`, `literary_body_extraction_frozen=false`, and `composite_literary_body_identity_frozen=false`.

Fresh PR-head workflows are required after the final contract/public-state commits; a later run must judge the current exact head independently before merge. This authored run does not self-approve or self-merge PR #111.

## Public representation

The Klim candidate page and machine-readable provenance trace now correct the public explanation: this is a target-only `#lst` edge case, not a labeled-section selection. They expose the exact invocation contract and the six-`poemx1` expansion boundary without publishing source prose or implying FantLab parity.

## Evidence boundary / benchmark movement

The ordered parent source-identity SHA-256 remains `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. The dependency revision remains independently pinned, but no resolved Part 2 or composite literary-body count/digest is claimed.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Next action

Independently review current exact head of PR #111 plus its fresh checks. If clean, merge this bounded semantic prerequisite while leaving Issue #109 open. Then continue #109 by freezing or deterministically reproducing the MediaWiki target template-DOM expansion layer, beginning with the six observed `poemx1` invocations, before any per-part literary extraction, 1->2->3->4 composition or composite digest.
