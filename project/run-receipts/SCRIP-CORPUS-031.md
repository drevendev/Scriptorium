# Run receipt — SCRIP-CORPUS-031

Date: 2026-09-19
Issue: #149
Pull request: #150 (`scrip-corpus-031-darwin-route-graph`)
Mode: normal-flow P2 corpus/provenance strengthening

## Selected bounded unit

Strengthen the retained Darwin/Rachinsky 1864 nonfiction candidate by freezing the exact rendered child-route revisions and their displayed bibliographic page spans, while keeping all underlying ProofreadPage identities and literary-body claims fail-closed.

## Evidence captured

The retained Russian Wikisource family already pins edition parent `oldid=5628021` and ProofreadPage index `oldid=4494408`. This run inspected the edition's rendered child routes and retained exact permanent revision locators for:

- numbered routes `/1`–`/14`: `3738261`, `3738286`, `3738290`, `3738294`, `3738299`, `3738303`, `3738307`, `3738312`, `3738315`, `3738265`, `3738270`, `3738274`, `3738278`, `3738282`;
- alphabetical-index route `/Указатель`: `3738318`.

The source displays bibliographic spans pp. 1–35, 36–48, 49–64, 65–108, 109–138, 139–167, 168–196, 197–222, 223–246, 247–274, 275–303, 304–325, 326–361, 362–387, then 389–399 for the alphabetical index. Route `/1` contains the introduction and Chapter I rather than only Chapter I.

Displayed print page 388 is intentionally recorded as an unclassified gap. Page-number continuity is not used to infer whether it is literary text, correction, blank, or apparatus.

## Durable result

- Added `corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json`.
- Updated the public candidate note to expose the stronger route identity and page-388 evidence boundary.
- Updated the structured source-edition trace to `rendered_route_graph_frozen_underlying_pages_unfrozen`.
- Added this semantic changelog fragment and advanced canonical state to hand Draft PR #150 to a later independent exact-head review.
- No literary prose, Page-namespace source content, scan bytes, or OCR are committed.

## Freeze boundary

Frozen at this stage:

- Rachinsky 1864 / Glazunov edition family;
- rendered parent revision locator `oldid=5628021`;
- ProofreadPage index revision locator `oldid=4494408`;
- exact revision locators for 14 numbered rendered routes plus the alphabetical-index route;
- displayed bibliographic print-page spans attached to those routes;
- displayed print page 388 as an explicit unclassified gap.

Still unfrozen:

- exact underlying Page-namespace revision IDs/timestamps/MediaWiki SHA-1 identities;
- mapping from displayed print pages to ProofreadPage scan/Page sequence positions;
- DjVu/PDF byte identity;
- OCR/Page-markup extraction semantics;
- literary-body decisions for front matter, alphabetical index, page 388, and other apparatus;
- deterministic extraction/composition contract and literary-body count/digests;
- FantLab analyzer-input/source-edition identity.

## Corpus and gate status

A 399-page bibliography and a frozen rendered route topology do **not** prove the repository's >=300,000-character literary-body threshold. The candidate therefore remains a retained diversification lead but is not yet admitted for calibration/profile work.

- `admitted_for_calibration=false`
- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Handoff

Draft PR #150 must be reviewed on its exact final head by a later run. That review should verify the source-free manifest, route/page-span evidence, absence of source prose, required CI, and the strict non-promotion boundary before any Ready/merge decision.

## Independent review completion

A later review run evaluated exact head `8b659b84384657d2815e97ec6bbe84f9d8a3942b` rather than relying on the authoring handoff.

- `master` was still `75e36de78937fba87e19c918fa29a655297cea4e`, exactly the PR base. The branch compared 7 commits ahead / 0 behind, remained mergeable, and had no inline review threads.
- Fresh Russian Wikisource reads independently matched all 15 rendered route permanent revision IDs and displayed spans to the committed source graph: `/1`–`/14` cover pp. 1–387 and `/Указатель` covers pp. 389–399. Displayed p. 388 remained an evidence gap and was not classified by inference.
- Full changed-file review found only source-free provenance/metadata, documentation and project-control updates; no literary source prose, Page-namespace payload, scan bytes or OCR were added.
- All 13 pull-request-triggered workflows on the reviewed head completed successfully. `Scriptorium Pages` run `35453635769`, job `105924979260`, passed the standard-library suite, canonical build, deterministic rebuild and artifact upload. Artifact `10587471934` has digest `sha256:e9cbee540ec61dd7e18bca93edad4069b007c350c29e04171c0a97457372c636` and is tied to the reviewed head. Live deploy remained skipped by the repository interlock.
- No boundary promotion occurred: underlying Page revisions, scan mapping/bytes, literary-body extraction/composition, count/digests, >=300k admission and FantLab source identity remain unfrozen/false/unknown; M2 stays 0/5.
- No blocking defect was found. PR #150 was marked Ready and squash-merged as `b64d243f515bf13df1183f53c1c0d5e1fd542615`; Issue #149 closed completed.
