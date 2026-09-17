# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #110
- Branch: `scrip-corpus-020-klim-body-freeze`
- Base at selection: `c23128966081455b5c4591e337c592358669d3f7`
- Reviewed exact head: `69811ae047553ffea7bfa89a94d77656ddf30366`
- Merge commit: `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`
- Result: `PREREQUISITE_MERGED_CONTINUATION_OPEN`

## Selected bounded unit

Independently review the existing Klim Samgin hidden-transclusion prerequisite PR, merge it only if exact-head evidence is clean, and preserve Issue #109 as the separate continuation for literary-body extraction/composition.

## Review result

The exact PR head `69811ae047553ffea7bfa89a94d77656ddf30366` was independently re-oriented and reviewed. The PR was mergeable, 14 commits ahead / 0 behind master, changed 10 expected files, and had no inline review threads. The mutation remained correctly limited to source-graph provenance: it pins the Part 2 `#lst` dependency at oldid `2366546`, adds source-free structural probing and replay, and explicitly does not freeze labeled-section semantics, a literary body, or FantLab input identity.

No blocking defect was found. A review comment was recorded on the exact head, the PR was marked Ready, and PR #110 was squash-merged as `c6d49b19f7f9d64b014b60f4ba76c5d542938fdc`.

Issue #109 remains open by design.

## Verification

All exact-head workflows completed successfully:

- Klim source-graph replay run `35203034786`: `success`. The job checked out exact head `69811ae047553ffea7bfa89a94d77656ddf30366`, ran **183 standard-library tests**, re-captured and byte-compared the four parent revision manifests plus dependency `oldid=2366546`, replayed all five exact revisions, probed source shapes without prose, verified the ordered parent digest and dependency digest, and uploaded source-free evidence. The probe reported Part 2 `lst_transclusion_targets=["Жизнь Клима Самгина (Горький)/Часть 2/part2"]`; the dependency revision itself reported no further `#lst` target.
- Scriptorium Pages run `35203034809`: `success`.
- Scriptorium frozen diagnostic run `35203034787`: `success`.
- Scriptorium pinned pylem provider run `35203034757`: `success`.

The dependency remains page ID `580081`, revision `2366546`, timestamp `2016-11-29T05:49:23Z`, MediaWiki SHA-1 `899c3d348b8550486c2c6774b84bc3ff55495f43`, 583,889 wikitext characters / 1,058,733 UTF-8 bytes, SHA-256 `173054997b54b96241adc07aeb6f76624beb497f94602452d7f9e4e57b0c6996`.

## Evidence boundary / benchmark movement

The parent ordered source-identity SHA-256 remains `54beabd28d8459bc6a0f1d83187dca56067e337999688d32c809d34340105577`. No literary-body count or digest is claimed.

Exact `#lst` labeled-section selection/placement semantics, per-part extraction, deterministic 1->2->3->4 composition and composite raw/`scriptorium-text-v1` digests remain open work on Issue #109. FantLab analyzer-input identity remains undisclosed.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5**.

## Next action

Continue Issue #109 in a later bounded run by freezing exact Part 2 labeled-section semantics and then the fail-closed four-part literary-body extraction/composition contract. Do not infer FantLab input identity or tune extraction toward FantLab's displayed count.
