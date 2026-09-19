# Run receipt — SCRIP-CORPUS-025

Date: 2026-09-19
Issue: #137
PR: #138
Mode: corpus / provenance
Result: authored, source revision identity frozen, pending independent PR review

## Selected unit

Freeze the exact source-revision identity for the retained Beketova translation of *Children of Captain Grant* without committing source prose. This was selected from the only executable P2 corpus/provenance continuation row because it strengthens an already legally/provenance-qualified translation candidate and removes a concrete blocker before literary-body admission.

## Evidence captured

GitHub Actions bootstrap run `35419728091`, job `105834985697`, on PR head `9e77bbb41263f48e2c1184f6303496b6812ef700` completed successfully. It ran the repository standard-library test suite, fetched exact Russian Wikisource revision `5304880`, validated the source-free artifact boundary and uploaded artifact `10577820530`.

The downloaded artifact ZIP SHA-256 is `215ab04fa6dd3697ef578a5ecad81e2dd195a12443f787afe45d15a88871fc62`. It contains exactly one JSON file, SHA-256 `b14aa6dc2e8ab712edfb559e9cb825a6b12dc203fbd412b9ecfb9267f5e22740`, with no source prose.

Frozen identity:

- title: `Дети капитана Гранта (Верн; Бекетова)`
- page ID: `1012777`
- revision ID: `5304880`
- revision timestamp: `2025-02-25T02:24:10Z`
- MediaWiki SHA-1: `256d816de6743031ea86f266ed004ee72240c200`
- wikitext character count: `1,107,187`
- wikitext UTF-8 byte count: `2,053,126`
- wikitext SHA-256: `71bfbe889cfc91b7dd24831a6a8984f3ac8d010c90d329b99a8f43aa4e3181a0`

The exact API timestamp corrects the prior rounded/incorrect `2025-02-25T02:24:00Z` value in the trace.

## Durable changes

- added `.github/workflows/beketova-source-revision.yml`;
- added `corpus/candidates/source-edition-traces/verne-children-captain-grant-beketova-ru.revision.json`;
- reconciled the structured provenance trace and dedicated candidate page;
- updated `corpus/README.md` so the public translation surface distinguishes frozen revision identity from unfrozen literary body;
- recorded this changelog and receipt; durable queue state points the next wake at independent review of Draft PR #138.

## Gate boundary

This unit freezes revision wikitext identity only. It does **not** define deterministic literary-body extraction, establish the exact literary-body character count or raw/normalized body digests, identify FantLab analyzer input, or advance M2. The 1,107,187 wikitext characters are not substituted for the >=300,000 literary-character admission rule.

`fantlab_source_edition_match=unknown`, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`; M2 remains 0/5.

## Next action

A later independent wake must review the final exact head of PR #138, inspect its workflow replay evidence and public/provenance wording, and merge only if all required checks are successful and no blocker is found. A subsequent normal-flow unit may then implement a candidate-specific fail-closed literary-body extractor for exact revision `5304880`.
