# Run receipt — SCRIP-CORPUS-023

Date: 2026-09-19
Issue: #133
Draft PR: #134
Branch: `agent/scrip-corpus-023-road-index-audit`
Base master at selection: `40ec83aef7fbf5aa4e791b01b4e8ccbaa054cd8b`

## Selected bounded unit

Audit the primary Pravda-1965/lib.web Russian Wikisource index routing for `grin-road-nowhere-ru` before attempting the trace's queued literary-page freeze.

## Evidence checked

- Permanent/current rendered work index `Дорога никуда (Грин)` identifies source family **A. S. Grin, Collected Works, vol. 6, Moscow: Pravda, 1965, pp. 3–227**, electronic source `lib.web`, and exposes permanent revision `oldid=4715367`.
- Its table of contents renders four labels under Part I and four under Part II.
- The Part I `Глава IV` label shares the exact link target of `Глава III`; Part II `Глава IV` likewise shares the exact target of `Глава III`.
- Part I Chapter I, II and III are live pages and repeat the same Pravda-1965 source citation.
- The distinct Part II Chapter I, II and III links exposed by the index resolve as red-link edit routes in the audited current surface.
- The alternate `Дорога в никуда (Грин)` route remains a separately sourced `az.lib.ru` transcription and was not used to infer or repair the primary route set.

## Durable changes

- Added `corpus/candidates/source-edition-traces/grin-road-nowhere-ru.index-route-audit.json` with source-free label-to-target/status evidence and explicit source-family boundary.
- Reconciled `grin-road-nowhere-ru.json`: primary status is now `index_route_surface_audited_not_complete`; a complete same-family route inventory is a prerequisite before exact page-revision freezing and literary-body work.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-023.md`.
- Opened Draft PR #134 for independent later review; no self-merge.

## Verification / claims

The new artifacts contain route metadata, URLs, labels and provenance only; no literary source prose is committed. The audit deliberately distinguishes the immutable link graph of `oldid=4715367` from current target-existence observations. It does not claim that Chapter IV pages are globally absent, does not infer a 24-chapter primary structure from the alternate transcription, and does not create a primary body/composite.

FantLab source identity remains unknown. `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5**. Repository CI is delegated to the Draft PR exact head and must be independently checked before any merge.
