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

## Independent exact-head review

A later recovery/review wake re-read repository policy/state, Issue #145, PR #146 and the full changed-file surface before judging the authored work.

- Exact authored head: `4976172850b375ce34357fdf0e0c860188258d35`.
- Review base: unchanged `master` `8a1195878757126511902625ffbdbbc38a178156`.
- Compare state: 7 commits ahead / 0 behind; PR mergeable; no inline review threads.
- Official Russian Wikisource source views independently showed `<pages ... from=8 to=149 />`, `<pages ... from=152 to=313 />`, and `<pages ... from=316 to=421 />` against the same 1928 Zemlya i Fabrika ProofreadPage index. Inclusive arithmetic independently reproduces 142 + 162 + 106 = 410.
- The diff was inspected for the evidence boundary: the two gaps 150–151 and 314–315 remain explicit/unclassified, the 1938/1961 family remains separate, no literary prose/Page content/scan bytes are committed, and no language promotes the underlying 410 Page revisions, PDF bytes, literary body, digests or FantLab analyzer input to frozen/matched status.
- All 13 pull-request-triggered workflows for the exact head completed successfully.
- `Scriptorium Pages` run `35441912697`, job `105894074343`, checked out the exact SHA, ran **287 tests** successfully, built the canonical static site, verified a deterministic rebuild, and uploaded Pages artifact `10583813114` with SHA-256 `efed0b1a23842e721bb04e9a824703a6f3e64a53e8ba8c522b9e9372b4690789`. Live deployment remained skipped behind the repository gate, as expected.

No blocking defect was found. PR #146 was marked Ready and squash-merged with expected-head protection as commit `a9abd3c01134683a0bc50aea204d2a2c05de9f93`; Issue #145 closed completed. The source-free route graph is therefore canonical in `master`. Literary-body identity and FantLab source match remain open evidence, and M2 remains **0/5**.
