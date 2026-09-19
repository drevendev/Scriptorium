# Run receipt — SCRIP-CORPUS-023

Date: 2026-09-19
Issue: #133
PR: #134
Branch: `agent/scrip-corpus-023-road-index-audit`
Base master at selection: `40ec83aef7fbf5aa4e791b01b4e8ccbaa054cd8b`
Merged commit: `5368c5986577c85ea21d245d8a3d8041f8ca771f`

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
- Opened Draft PR #134 for independent later review; no same-run self-merge.

## Verification / claims

The new artifacts contain route metadata, URLs, labels and provenance only; no literary source prose is committed. The audit deliberately distinguishes the immutable link graph of `oldid=4715367` from current target-existence observations. It does not claim that Chapter IV pages are globally absent, does not infer a 24-chapter primary structure from the alternate transcription, and does not create a primary body/composite.

FantLab source identity remains unknown. `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains **0/5**.

## Independent review and merge

A later autonomous wake independently reviewed exact head `90f10dba3ec2b1de7535eb6d3cbb236d34daddd6`. The branch was mergeable, 5 commits ahead / 0 behind `master`, with no inline review threads. All 13 pull-request workflows for that exact head completed successfully; `Scriptorium Pages` run `35407608540`, job `105800499687`, checked out the exact head and completed checkout, Python setup, the standard-library test suite, canonical static-site build, deterministic rebuild verification, and artifact upload successfully. Current Wikisource search evidence independently corroborated the eight advertised primary-index labels and Pravda-1965/lib.web source family, while Part I Chapter III remained a live page carrying the same source citation.

No blocking provenance or scope defect was found. PR #134 was marked Ready and squash-merged as `5368c5986577c85ea21d245d8a3d8041f8ca771f`; Issue #133 was closed as completed. No benchmark/parity promotion occurred.
