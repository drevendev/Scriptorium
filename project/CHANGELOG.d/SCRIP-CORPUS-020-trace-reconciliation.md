# SCRIP-CORPUS-020 — structured Klim trace reconciliation

Date: 2026-09-18
Issue: #109
PR: #128 (Draft; authored for independent later-run review)
Base: `155a98cadf1595e9bbadd0a2cd63f61a164f8e55`

## Change

Reconciled `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.json` with the canonical literary-body identity already merged by PR #127.

The structured trace now:

- references `gorky-klim-samgin-ru.literary-body.json` and its manifest/extraction profiles;
- records the frozen four-part composition order `1 -> 2 -> 3 -> 4` with the double-LF separator;
- records the source-free composite identity: 3,810,618 characters / 6,958,930 UTF-8 bytes, raw and `scriptorium-text-v1` SHA-256 `4f8b61e05cf7d96485d9edc0854d99d994da6ba146fabc3f6a3d509110ce4288`;
- removes stale claims that the literary-body extraction/composition/digests remain unfrozen;
- changes structured diagnostic readiness to `true` now that the candidate-specific immutable body identity exists;
- keeps the evidence class `candidate_specific_inferred_reconstruction` and explicitly leaves historical Russian Wikisource MediaWiki-core/Poem deployment/parser-byte equivalence unproven;
- preserves `fantlab_source_edition_match=unknown`, `gate_ready=false`, and `m2_parity_admissible=false` because FantLab's analyzer input remains undisclosed.

## Boundary

This is a provenance-consistency change, not a new parity result. It does not claim historical rendering equivalence and does not move M2 from 0/5. Issue #109 remains open until PR #128 receives an independent exact-head review and, if safe, merge/closure judgement in a later run.
