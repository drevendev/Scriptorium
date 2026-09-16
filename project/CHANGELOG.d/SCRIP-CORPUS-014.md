# SCRIP-CORPUS-014 — Road to Nowhere alternate revision identity

Date: 2026-09-16
Issue: #97
PR: #98
Base: `3a01196a10966417e244ef4412c70069d28e95fa`
Status: authored, independent review pending

## Unit

Strengthened the existing `grin-road-nowhere-ru` candidate instead of adding another trace-only work. The alternate single-page Russian Wikisource route `Дорога в никуда (Грин)` is sourced from `az.lib.ru`, identifies the original Russian work as public domain, exposes a 2-part / 24-chapter structure, and is pinned at permanent revision `oldid=5585836`.

A source-free capture now records exact revision-wikitext identity without committing literary prose: page ID `1003775`, revision timestamp `2025-07-30T20:33:01Z`, MediaWiki SHA-1 `135933c3b9155bddb0356d0eb9644d11f55ba870`, 443,991 wikitext characters / 827,730 UTF-8 bytes, and SHA-256 `f47b9b05d06dc2f5c6e2642d0822e6db68128386e4f1374b9188206a69fef11b`.

The capture boundary is deliberately narrower than a frozen literary-text candidate. No deterministic literary-body extraction contract or body/composite digest exists for this route yet, the primary Pravda-1965 Wikisource family remains separately traced and unfrozen, and neither public route is identified as FantLab's analyzer input.

## Verification design

`scriptorium.single_page_revision` fetches the exact pinned revision through the MediaWiki API, validates title/revision identity, hashes the in-memory wikitext, and serializes only source-free identity fields. Unit tests cover fail-closed title/revision drift, capture-scope gating, source-prose omission and replay drift detection. The dedicated pull-request workflow regenerates the pinned identity and compares it byte-for-byte with the committed source-free manifest before replaying it.

Bootstrap Actions run `35131233283` successfully completed the standard-library suite and the source-free capture step and produced artifact `road-nowhere-alternate-source-revision`; final exact-head verification is recorded on PR #98 after the authored branch is complete.

Benchmark movement: none. `source_identity_status=traced_not_frozen`, `fantlab_source_edition_match=unknown`, diagnostics remain disabled, and M2 remains **0/5 source-matched works**.
