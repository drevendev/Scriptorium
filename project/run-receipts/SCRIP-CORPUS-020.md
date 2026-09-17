# Run receipt — SCRIP-CORPUS-020

- Date: 2026-09-17
- Issue: #109
- PR: #112 — draft, independent review pending
- Branch: `agent/scriptorium-corpus-020-poemx1-history`
- Base at selection: `7798c76f80add8fac45db4aee3361b47f87cb7e4`
- Result: `POEMX1_HISTORY_AUTHORED_REVIEW_PENDING`

## Selected bounded unit

Advance the open Klim Samgin source-graph boundary by freezing a deterministic historical revision identity for the `poemx1` template used six times by the already pinned Part 2 dependency. Do not reproduce or claim resolved MediaWiki expansion in the same unit; preserve the distinction between a deterministic as-of reconstruction anchor and historical render equivalence.

## Implementation

Added `scriptorium/template_history.py`, a source-free historical-template revision resolver. Its policy is `latest_revision_not_after_anchor_timestamp`. Capture stores only page/revision identity, counts and hashes; replay re-resolves the same as-of selection and separately fetches the exact selected oldid. The manifest explicitly records:

- `evidence_class = inferred_reconstruction_anchor`
- `historical_render_equivalence_proven = false`
- `template_expansion_reproduced = false`
- `source_text_committed = false`

Focused mocked tests cover query direction/anchor parameters, rejection of a revision newer than the anchor, title drift, source-free manifest boundaries, exact replay and selection/pinned-byte drift. The repository-wide standard-library suite now includes those tests.

A dedicated PR-head workflow `.github/workflows/klim-samgin-template-history.yml` first requires the existing Part 2 contract to retain exactly six `poemx1` invocations, then captures the historical template revision, probes source shape without prose, byte-compares the committed manifest/shape and replays the exact selected revision. Checkout and Python setup actions are full-SHA pinned and credentials are not persisted.

## Historical template evidence

Using pinned Part 2 oldid `5198033` and timestamp `2024-11-26T11:16:35Z` as the reconstruction anchor, live Russian Wikisource resolution selected `Шаблон:Poemx1`:

- page ID: `54236`
- oldid: `5142743`
- revision timestamp: `2024-06-02T02:25:12Z`
- MediaWiki SHA-1: `7b7da0fa04913bc902f6455addad437fc19d67d8`
- wikitext characters: `2412`
- UTF-8 bytes: `2918`
- wikitext SHA-256: `fa7e35686da5ce4c62986a7e8bfc72f2dba067118218d656b2f0983e5cfa06db`

The immutable source-free record is `corpus/candidates/source-edition-traces/gorky-klim-samgin-ru.poemx1-template.revision.json`.

## Source-shape evidence and correction

The first probe implementation was intentionally treated as diagnostic and was not committed as evidence because its simple double-brace regex could classify triple-brace parameter syntax as template openings. Before freezing shape evidence, the probe was repaired to require an exact double-brace opener (`(?<!\{)\{\{(?!\{)`), and parser functions plus the `PAGENAME` magic word were separated from ordinary template-shaped invocations.

The corrected source-free raw inventory for oldid `5142743` is committed as `gorky-klim-samgin-ru.poemx1-template.shape.json`:

- ordinary raw template-shaped invocations: `doc` x1
- parser functions: `#expr` x2, `#if` x5, `#ifeq` x5, `#iferror` x1, `#tag` x1
- magic words: `PAGENAME` x1
- HTML-like tags: `div` x6, `includeonly` x2, `noinclude` x4, `templatedata` x2

This artifact explicitly does **not** apply MediaWiki `noinclude` / `includeonly` / `onlyinclude` transclusion semantics and therefore does not claim that `doc` or any other raw construct is an effective transitive dependency.

## Verification / repair evidence

The first exact-head capture run `35223860049` completed successfully and ran **192** standard-library tests while establishing the selected template revision identity. A later strict replay run `35224056659` again passed all 192 tests, the Part 2 dependency guard, live template capture and the corrected v2 source-shape probe, then failed at the intended byte comparison because the newly hand-copied committed manifest had one malformed percent-encoded character sequence in `source_work_url`. That authored-data defect was repaired from the workflow's generated manifest, and the workflow was tightened so both manifest and shape artifacts are mandatory and byte-compared before exact replay.

Because this run authored the substantive change, it does not self-approve or merge PR #112. The final exact head must receive independent later-run judgement even if all checks are green.

## Public representation

`corpus/candidates/gorky-klim-samgin-ru.md` now exposes the exact `poemx1` as-of revision identity and the raw structural boundary. It states that the timestamp policy is inferred reconstruction evidence rather than proof of MediaWiki historical render state, and it keeps resolved Part 2/body identities unavailable.

No source prose was committed.

## Evidence boundary / benchmark movement

The new template anchor narrows the MediaWiki-expansion problem but does not produce a literary body. No resolved Part 2 wikitext identity, four-part extraction/composition identity, raw body digest or `scriptorium-text-v1` digest is recorded.

`fantlab_source_edition_match=unknown`; `diagnostic_ready=false`; `gate_ready=false`; `m2_parity_admissible=false`; M2 remains **0/5 source-matched works**.

## Next action

Independently review the final exact head of draft PR #112 and merge the bounded historical-template identity prerequisite only if required checks/evidence remain clean. Keep Issue #109 open. The next continuation should apply/freeze MediaWiki inclusion semantics to pinned `poemx1`, determine the effective transclusion dependency graph, then reproduce the evidenced parser-function and `#tag:poem` behavior before resolving Part 2 bytes.
