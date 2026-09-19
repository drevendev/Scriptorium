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

PR #142 remains Draft because this run authored the substantive change. The next run must independently review the exact PR head after CI settles, verify live semantic capture plus pinned replay, inspect provenance/public wording and merge only if no blocker is found.
