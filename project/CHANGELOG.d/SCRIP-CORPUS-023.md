# SCRIP-CORPUS-023 — Road to Nowhere primary-index routing audit

Date: 2026-09-19
Issue: #133
PR: #134

- Re-audited the retained Russian Wikisource primary source family for Alexander Grin's *Road to Nowhere* rather than proceeding directly to literary-page freezing.
- Preserved permanent work-index revision `oldid=4715367` and its explicit Pravda 1965 volume-6 pp. 3–227 / `lib.web` bibliography as the primary bibliographic-family witness.
- Recorded a new source-free machine-readable index-route audit. The permanent index renders eight chapter labels across two parts but only six distinct link targets: in both parts the Chapter IV label points to the same target as Chapter III.
- Kept immutable index routing distinct from current target existence. At the 2026-09-19 audit, the Part II Chapter I, II and III targets exposed by the index resolve as red links; the Chapter IV label duplicates the Chapter III red-link target. This does not prove that a complete primary transcription cannot exist elsewhere, only that this index is not a complete/reliable route inventory.
- Confirmed that Part I Chapter I–III are live same-family pages carrying the same Pravda-1965 source citation.
- Reconciled the structured provenance trace so the next evidence must first recover or independently establish a complete **same-family** primary route set, then freeze exact page revisions, then define extraction/composition. The separately frozen `az.lib.ru` route may not be used to fill primary-route gaps.
- No source prose, primary literary-body extraction, composite digest, source-edition match or parity promotion was added. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.
- Independent exact-head review later verified PR #134 at `90f10dba3ec2b1de7535eb6d3cbb236d34daddd6`: the branch was 5 commits ahead / 0 behind `master`, had no inline review threads, and all 13 pull-request workflows completed successfully. No blocking provenance/scope defect was found; the PR was marked Ready and squash-merged as `5368c5986577c85ea21d245d8a3d8041f8ca771f`, and Issue #133 was closed as completed.
