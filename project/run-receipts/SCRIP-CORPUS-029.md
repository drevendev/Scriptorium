# Run receipt — SCRIP-CORPUS-029

Date: 2026-09-19
Issue: #145
Pull request: #146 (`scrip-corpus-029-twelve-chairs-1928-source-graph`)
Mode: normal-flow P2 corpus/provenance strengthening

## Selected bounded unit

Freeze a source-free parent route graph for the distinct first standalone Zemlya i Fabrika 1928 Russian Wikisource transcription of Ilf and Petrov's *The Twelve Chairs*, without claiming a frozen literary body or FantLab source identity.

## Evidence captured

The retained work index remains pinned at `oldid=5706135` and identifies the first standalone 1928 Zemlya i Fabrika family. Current official Russian Wikisource evidence adds the ProofreadPage source index at exact revision `oldid=5702510`, identifying year 1928, publisher `Земля и Фабрика`, publication places `Москва—Ленинград`, and transclusion status `Трансклюзии требует проверки`.

The three exact part-parent revisions all transclude that ProofreadPage index:

- Part 1: `oldid=5702507`, `<pages ... from=8 to=149 />` — 142 dependencies.
- Part 2: `oldid=5704332`, `<pages ... from=152 to=313 />` — 162 dependencies.
- Part 3: `oldid=5702508`, `<pages ... from=316 to=421 />` — 106 dependencies.

The disjoint ranges therefore reference **410 Page-namespace dependencies**. Scan-index gaps **150–151** and **314–315** are not transcluded by these parent pages and are recorded as unclassified; this run does not infer whether they are separators, front/back matter, or literary content.

## Durable result

- Added `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-zif-1928.source-graph.json`.
- Updated `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-ru.json` to distinguish a frozen parent route graph from an unfrozen body.
- Updated the dedicated public candidate page with the same boundary.
- Added the semantic changelog fragment and advanced `STATE_AND_QUEUE` to revision 167 with independent review of Draft PR #146 as P0.
- No literary prose, Page-namespace source content, or scan bytes are committed.

## Freeze boundary

Frozen at this stage:

- retained 1928 work-index revision locator;
- ProofreadPage index revision locator and bibliographic family;
- three part-parent revision locators;
- exact transclusion ranges 8–149, 152–313, and 316–421;
- 410-dependency cardinality;
- explicit two-page gaps 150–151 and 314–315.

Still unfrozen:

- exact revision IDs/timestamps/MediaWiki SHA-1 identities of all 410 referenced Page-namespace pages;
- the facsimile PDF byte stream and digest;
- Page-markup extraction/rendering rules;
- part/composite literary-body counts and digests;
- the relation of this public transcription to FantLab's undisclosed analyzer input.

## Gate status

The later 40-chapter 1938/1961 editorial family remains a distinct identity from the 41-chapter first standalone 1928 family. The work remains coauthored evidence and is not assigned to an individual Ilf or Petrov VOICE profile.

- `fantlab_source_edition_match=unknown`
- `diagnostic_ready=false`
- `gate_ready=false`
- `m2_parity_admissible=false`
- M2 remains **0/5 source-matched works**

## Verification and handoff

The machine-readable manifest records the three monotonic, non-overlapping ranges and their counts (142 + 162 + 106 = 410) and contains metadata only. Draft PR #146 is intentionally left for a later independent exact-head review. That review must inspect the final diff, exact-head workflow results, source-free boundary, range/count arithmetic, explicit gaps, and non-promotion of route topology into literary-body/FantLab identity before any merge.
