# Run receipt — SCRIP-CORPUS-027

Date: 2026-09-19
Issue: #141
Pull request: #142 (Draft)
Base at selection: `0788e4233d76d1f0b045d0cfda8349b557c2ae01`

## Unit

Freeze source-free exact revision identities for the retained 1965-source Russian Wikisource literary route of *Running on Waves*: `/1` through `/35` plus `/Эпилог`.

## Evidence

Candidate-specific bootstrap workflow run `35430448437`, job `105863933461`, completed successfully on head `ce0dbc90ec87b342342d491ece49e98753313dfd`. It ran the repository standard-library suite, captured all 36 current page identities without requesting source text, enforced source-free/fail-closed guards and uploaded artifact `10581001332` with digest `sha256:a0c58c00b0e5a1ea0a6649815ef7489b06ca7eecb129cf7f19bd1729bf288572`.

The captured artifact was reconciled into `grin-running-on-waves-ru.source-revisions.json`. The manifest contains exactly 36 ordered records, each with page ID, revision ID, UTC timestamp and MediaWiki SHA-1. The workflow can replay pinned revisions in memory while serializing no prose.

## Independent review pass

Review of authored head `7a4afc6d0bc1b9f48b852637517c1923e1f610b4` found one acceptance-coverage defect rather than a source/provenance defect: Issue #141 explicitly requires tests for missing-page, redirect and drift failures, but the initial test file did not directly exercise the live-capture missing and redirect branches.

Repair commit `11c21e17128232301c70b6ac11010096be8a8259` added deterministic tests for missing pages, redirected pages and unexpected-title drift. Candidate-specific workflow run `35433085356`, job `105870994908`, checked out that exact repaired head, ran 279 tests successfully, re-captured the live source-free 36-page inventory, matched it semantically to the committed manifest, replayed every pinned revision and passed the source-free/fail-closed guard. It uploaded source-free artifact `10581770727` with ZIP digest `sha256:62950f8e719df4ba2a1ecc903c56477d00eb3b5d6c1280a13944fe879c0a5377`.

The repair changes verification coverage only; it does not promote literary-body extraction, composite identity, FantLab source matching or M2 status.

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

PR #142 remains Draft while exact-head CI settles after the review repair. The next judgement point is the final repaired head: verify all required workflows are green, confirm no new review defects, then mark Ready and merge if safe. If another defect appears, keep the PR Draft and repair it without relaxing the provenance/parity boundaries.
