# SCRIP-CORPUS-013 authored run receipt

Date: 2026-09-16  
Base revision: `52dc8fbc4b4782b1e7980c09ee420ddd2fd75cc6`  
Observed `STATE_REVISION`: 103  
Issue: #95  
Branch: `scrip-corpus-013-twelve-chairs`

## Selection

The durable queue had no interrupted/review-ready Scriptorium PR and its only executable normal-flow row was `SCRIP-CORPUS continuation`. This unit selects Ilf and Petrov's *The Twelve Chairs* as a legally usable >=300k 20th-century diversity candidate because it also exposes a concrete edition-family split relevant to future source matching and author-voice design.

## Produced

- `corpus/candidates/source-edition-traces/ilf-petrov-twelve-chairs-ru.json` records FantLab's public 2022 counts, the undisclosed-input boundary, the two coexisting Wikisource text families, the 1928 facsimile lead, legal scope, coauthorship caveat and fail-closed admissibility.
- `corpus/candidates/ilf-petrov-twelve-chairs-ru.md` gives repository visitors a source-free explanation of why the 40-chapter later family and 41-chapter 1928 family are separate identities.
- No literary prose, scan bytes or copyrighted editorial apparatus are committed.

## Evidence boundary

The later Wikisource route (`oldid=5706136`) cites the 1961 GIKhL collected works and states that its text reproduces the 1938 Soviet Writer four-volume edition checked against earlier publications. The separate first-standalone-edition route (`oldid=5706135`) identifies Zemlya i Fabrika 1928. Their observed 40-versus-41 chapter structures prove that Scriptorium must keep the routes separate, but do not prove all textual differences or identify FantLab's analyzer input.

FantLab work `182817` reports 572,654 characters / 80,203 words on 2022-09-17 and does not disclose analyzer-input edition/bytes. Its author-recognition warning for this coauthored work is retained only as future VOICE-method evidence, not a profile or parity result.

## Gate state

`source_identity_status=traced_not_frozen`; `fantlab_source_edition_match=unknown`; diagnostics and M2 admission remain disabled. M2 therefore remains 0/5 source-matched works.

## Next action

Open the authored PR, verify the exact head and leave it unmerged for a later independent review. If the PR merges, reconcile the central candidate catalog/navigation plus canonical `STATE_AND_QUEUE.md` / `CHANGELOG.md` in review bookkeeping if not already updated on the branch. A future freeze must select one text family and pin exact literary-page identities, deterministic extraction/composition and composite digests; the 1928 scan additionally requires an exact binary snapshot hash before it can serve as binary evidence.
