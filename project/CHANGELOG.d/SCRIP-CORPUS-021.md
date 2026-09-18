# SCRIP-CORPUS-021 — Shining World source-inventory audit

- Issue: #129
- Draft PR: #130
- Scope: corpus/provenance correctness for `grin-shining-world-ru`; no literary-body freeze, FantLab source-match claim or M2 promotion.

## Finding

The reviewed Russian Wikisource work index at permanent revision `oldid=4186047` advertises a `16 + 11 + 7 = 34` chapter structure and cites A. S. Grin's 1965 Pravda collected works, volume 3, pp. 66–214. The previous trace shorthand described those links as 34 chapter subpages.

A source-free live MediaWiki audit disproved that assumption. On 2026-09-18 only **19** advertised chapter targets existed: all 16 Part I pages and Part II chapters I–III. **15** advertised targets were missing: Part II chapters IV–XI and all seven Part III chapters. The public family is therefore bibliographically useful but incomplete as a complete-work transcription.

## Implementation

`scriptorium/shining_world_revisions.py` now defines the advertised title contract, probes revision identity without requesting source content, records present pages by exact revision ID / UTC timestamp / MediaWiki SHA-1, records missing targets explicitly without invented identity, and replays only exact pinned present revisions. The committed source-free inventory is `corpus/candidates/source-edition-traces/grin-shining-world-ru.source-inventory.json`; the canonical trace is updated to distinguish advertised navigation from existing pages.

The dedicated workflow checks out the exact PR head, runs the full standard-library suite, re-audits the 34 titles, compares the live source-free inventory with the committed record, replays exact present revisions, rejects prose-bearing keys, and uploads only the source-free audit artifact.

## Evidence boundary

The 19 exact present-page identities do **not** produce a complete literary body. Scriptorium does not silently splice the missing 15 chapters from RVB or another provider. `fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains **0/5**.
