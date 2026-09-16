# SCRIP-CORPUS-015 run receipt

- Date: 2026-09-16
- Issue: #99
- PR: #100
- Base revision: `b58598f7e54d8849369077ad07ad0628ad5e38d9`
- Selection reason: no recovery/review-ready PR or failing required check existed; the only executable queue row was `SCRIP-CORPUS continuation`. The retained Hyperboloid trace explicitly named exact MediaWiki revision freezing as its next evidence step.
- Status: AUTHORED / REVIEW_PENDING

## Produced

- Reused the merged generic `scriptorium.single_page_revision` implementation; no candidate-specific capture code was added.
- Added `.github/workflows/hyperboloid-source-revision.yml` to regenerate and replay the exact pinned revision on pull requests.
- Added `corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.revision.json` containing source-free revision-wikitext identity only.
- Updated the canonical Hyperboloid source-edition trace so revision-wikitext freezing cannot be confused with literary-body identity, bibliographic print-edition identity or FantLab source matching.
- Synchronized `corpus/candidates/README.md` with the new Hyperboloid boundary and repaired its previously stale Road to Nowhere alternate-revision description.
- Added `project/CHANGELOG.d/SCRIP-CORPUS-015.md`.

## Captured source-free identity

- page ID: `1022517`
- revision ID: `5014458`
- revision timestamp: `2023-08-30T20:13:01Z`
- MediaWiki SHA-1: `605afeabc38e4f5948371afdf976f586edbf1955`
- wikitext characters: `502280`
- wikitext UTF-8 bytes: `934455`
- wikitext SHA-256: `fa0b099bba2d0f0e6ce395a16de76317afcd8bec8b23b52e455f97a9726a4de9`
- source prose committed: `false`

The exact API timestamp is one second later than the display-level timestamp previously retained in the trace; the canonical trace now uses the exact revision timestamp.

## Verification

Bootstrap workflow run `35143256162` completed successfully and produced artifact `hyperboloid-source-revision` from revision `5014458`. The artifact supplied the exact source-free identity above. The completed branch must still receive a final exact-head run that byte-compares the committed manifest against a fresh capture and replays it successfully before independent review.

## Gates

The MediaWiki revision wikitext is now frozen, but no deterministic literary-body extraction or raw/normalized literary-text digest exists. The `az.lib.ru` transcription still has no direct print-edition identity, and the Moscow 1958 / 1939-derived family remains a lead only. FantLab work `44824` does not disclose analyzer-input edition or bytes. Therefore `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, `fantlab_source_edition_match=unknown`, and M2 remains `0/5`.

## Next wake

Review exact PR #100 head independently after required Actions checks are green. If accepted, merge and reconcile canonical `STATE_AND_QUEUE.md` bookkeeping. Do not treat the revision manifest as a literary-body freeze, a print-edition match or FantLab source evidence.
