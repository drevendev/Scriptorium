# Run receipt — SCRIP-CORPUS-027

Date: 2026-09-19
Issue: #141 (closed completed)
Pull request: #142 (squash-merged)
Base at selection: `0788e4233d76d1f0b045d0cfda8349b557c2ae01`
Merged commit: `45ae261c03a18471d7798b1c083ab69fee8c4866`

## Unit

Freeze source-free exact revision identities for the retained 1965-source Russian Wikisource literary route of *Running on Waves*: `/1` through `/35` plus `/Эпилог`.

## Evidence

Candidate-specific bootstrap workflow run `35430448437`, job `105863933461`, completed successfully on head `ce0dbc90ec87b342342d491ece49e98753313dfd`. It ran the repository standard-library suite, captured all 36 current page identities without requesting source text, enforced source-free/fail-closed guards and uploaded artifact `10581001332` with digest `sha256:a0c58c00b0e5a1ea0a6649815ef7489b06ca7eecb129cf7f19bd1729bf288572`.

The captured artifact was reconciled into `grin-running-on-waves-ru.source-revisions.json`. The manifest contains exactly 36 ordered records, each with page ID, revision ID, UTC timestamp and MediaWiki SHA-1. The workflow can replay pinned revisions in memory while serializing no prose.

## Independent review pass

Review of authored head `7a4afc6d0bc1b9f48b852637517c1923e1f610b4` found one acceptance-coverage defect rather than a source/provenance defect: Issue #141 explicitly requires tests for missing-page, redirect and drift failures, but the initial test file did not directly exercise the live-capture missing and redirect branches.

Repair commit `11c21e17128232301c70b6ac11010096be8a8259` added deterministic tests for missing pages, redirected pages and unexpected-title drift. Candidate-specific workflow run `35433085356`, job `105870994908`, checked out that exact repaired head, ran 279 tests successfully, re-captured the live source-free 36-page inventory, matched it semantically to the committed manifest, replayed every pinned revision and passed the source-free/fail-closed guard. It uploaded source-free artifact `10581770727` with ZIP digest `sha256:62950f8e719df4ba2a1ecc903c56477d00eb3b5d6c1280a13944fe879c0a5377`.

The final exact head was `ba4d22a12bb3be2df72637e39a99215fa3c4a842`. All 14 exact-head PR workflows completed successfully. Candidate-specific run `35433175579`, job `105871255330`, checked out that exact SHA, ran 279 tests, matched live capture to the committed manifest, replayed all 36 pinned revisions and passed the source-free guard. Its source-free artifact is `10582210362` with ZIP digest `sha256:41df3264f4934dbe44780c1f27e4ad0c2fdff9a238c940cb4cf41bd215765bdb`. `Scriptorium Pages` run `35433175583`, job `105871255369`, passed tests, canonical build and deterministic rebuild. No unresolved review threads remained; the branch was 10 commits ahead / 0 behind master and mergeable.

PR #142 was marked Ready and squash-merged as `45ae261c03a18471d7798b1c083ab69fee8c4866`; Issue #141 closed completed.

## Boundaries

- `route_inventory_frozen=true`
- `literary_page_revisions_frozen=true`
- `literary_body_extraction_frozen=false`
- `composite_identity_frozen=false`
- `fantlab_source_edition_match=unknown`
- `m2_parity_admissible=false`
- no source text committed

The separate 1980/az.lib.ru `/Версия 2` route remains excluded. Benchmark movement: none; M2 remains 0/5.

## Handoff

SCRIP-CORPUS-027 is complete. No recovery PR remains for this unit. Resume the normal-flow corpus/provenance queue, preserving edition/translation identity and the >=300k/legal-provenance gate. A later Running on Waves unit may define a deterministic literary-body extraction/composition contract, but page-revision identity alone must not be presented as analyzed-text identity or FantLab parity.
