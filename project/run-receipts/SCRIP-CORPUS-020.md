# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #110
- Branch: `scrip-corpus-020-klim-body-freeze`
- Base at selection: `c23128966081455b5c4591e337c592358669d3f7`
- Verified substantive head: `d4c055856f00bd06840b46fd5f9efcec91db32ed`
- Result: `REVIEW_PENDING`

## Selected bounded unit

Attempt to strengthen the retained Maxim Gorky *The Life of Klim Samgin* candidate from four replay-frozen parent revision identities toward a deterministic source-free literary-body identity, while failing closed on any source-graph or extraction ambiguity.

## Discovery and bounded result

The source-free structural probe changed the unit's safe stopping point. Part 2 (`oldid=5198033`) contains an unversioned `#lst` labeled-section reference to `Жизнь Клима Самгина (Горький)/Часть 2/part2`. Therefore the four parent oldids alone are not a complete frozen literary source graph, and proceeding directly to a body digest would manufacture reproducibility.

This run instead completed the dependency prerequisite end-to-end:

1. Added `scriptorium.klim_samgin_freeze` as a source-free structural/dependency probe that first verifies exact pinned parent identity and emits no prose.
2. Resolved and committed a source-free revision manifest for the Part 2 transclusion dependency: page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`.
3. Extended the source-graph summary to bind the dependency while retaining all body/composition flags as false.
4. Added tests proving the dependency manifest is source-free and the summary remains fail-closed.
5. Extended the dedicated Klim workflow to capture, byte-compare and replay the four parent revisions plus the dependency and to probe the exact pinned source shapes.
6. Updated the standalone public candidate page and machine-readable provenance trace to expose the hidden dependency and explain why body identity remains unfrozen.
7. Reframed PR #110 as a prerequisite to #109 rather than closing the full body-freeze issue; Issue #109 remains open with the exact next trigger.

No book prose is committed.

## Verification

Substantive exact head `d4c055856f00bd06840b46fd5f9efcec91db32ed` passed all workflows triggered for the change:

- Klim source-graph replay run `35202668027`: `success`. It ran **183 standard-library tests**, re-captured and byte-compared all four parent revision manifests plus dependency `oldid=2366546`, replayed all five exact revisions, probed source shapes without prose, verified the ordered parent digest and dependency digest, and uploaded source-free evidence. The probe explicitly reported the Part 2 `lst_transclusion_targets` entry `Жизнь Клима Самгина (Горький)/Часть 2/part2`.
- Scriptorium Pages run `35202668056`: `success`.
- Scriptorium frozen diagnostic run `35202667999`: `success`.

The PR remains Draft because this run authored the substantive repair; merge judgement is reserved for an independent later wake.

## Evidence boundary / benchmark movement

The parent ordered source-identity SHA-256 remains `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. The newly pinned dependency has wikitext SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`.

No literary-body count or digest is claimed. Exact `#lst` labeled-section selection/placement semantics, per-part extraction, deterministic 1->2->3->4 composition and composite raw/`scriptorium-text-v1` digests remain the next implementation work. FantLab analyzer-input identity remains undisclosed.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5**.

## Next action

Independently review the final head of draft PR #110. If the source-graph prerequisite is clean and its checks/evidence remain valid, merge #110 without closing Issue #109. A subsequent unit may then continue #109 by freezing exact labeled-section semantics and the four-part literary-body extraction/composition contract. Do not infer FantLab input identity or tune extraction toward FantLab's displayed count.
