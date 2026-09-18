# Run receipt — SCRIP-CORPUS-020 structured trace reconciliation

Date: 2026-09-18
Issue: #109
PR: #128 (Draft)
Branch: `scrip-corpus-020-trace-reconciliation`
Base master: `155a98cadf1595e9bbadd0a2cd63f61a164f8e55`

## Selection

`project/STATE_AND_QUEUE.md` named structured Klim provenance-trace reconciliation as the current P0 continuation after the independently reviewed/merged literary-body identity in PR #127. No recovery-ready PR preempted that authored continuation at run start.

## Production

- Reconciled `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.json` against canonical `gorky-klim-samgin-ru.literary-body.json`.
- Added explicit manifest/version/extraction-profile links and the frozen composite identity: 3,810,618 characters / 6,958,930 UTF-8 bytes; raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`.
- Removed completed literary-body extraction/composition/digest items from `unfrozen_components` and replaced the stale no-body-digest rationale.
- Set structured `diagnostic_ready=true` and diagnostic-candidate status now that an immutable candidate-specific body exists.
- Preserved `fantlab_source_edition_match=unknown`, `gate_ready=false`, and `m2_parity_admissible=false`.
- Preserved an explicit non-equivalence boundary for historical Russian Wikisource MediaWiki-core/Poem deployment/parser-byte behavior and FantLab analyzer-input identity.
- Updated durable state to revision 148 and added this changelog/receipt handoff.

## Verification

The replacement JSON was constructed and parsed successfully with Python `json.loads` before the GitHub write. Canonical counts, digests, evidence class and gate flags were copied from the already-merged source-free literary-body manifest rather than recomputed or inferred. A later exact-head CI/review pass is still required by repository policy before merge.

## Result / next trigger

Draft PR #128 is the review-ready handoff. This authoring run does not self-approve or merge it. The next run should independently inspect the exact final head and relevant checks; if clean, merge #128 and close #109 only if all acceptance criteria are then satisfied. M2 remains 0/5.
