# Run receipt — SCRIP-CORPUS-055

Date: 2026-09-22
Mode: corpus / provenance
Issue: #197
Pull request: pending authoring handoff
Base at selection: `98e903e6c28f80c26489c90ed137d3bfa606e9a2`

## Selection

The repository had no open pull requests or issues, no recovery work, and `STATE_AND_QUEUE.md` exposed only P2 `SCRIP-CORPUS continuation`. This bounded pass screened Yevgeny Zamyatin's *We* (`Мы`) before any expensive source-freezing or parity work because it is a high-value early-20th-century modernist/dystopian diversity lead with a public-domain Wikisource route and an existing FantLab linguistic-analysis surface.

## Fresh evidence

FantLab work `20055` exposes a linguistic-analysis page dated **17 September 2022**. Rechecked on 2026-09-22, it reports:

- **285,704 characters**;
- **43,500 words**.

The project manifest requires an admitted parity-benchmark work to contain at least **300,000 characters including spaces**. FantLab's analyzed input is therefore **14,296 characters below** the mandatory floor.

Russian Wikisource separately exposes *We* and marks the literary work public domain in Russia / life+70-or-less jurisdictions. Its source note identifies **Yevgeny Zamyatin, Collected Works in five volumes, vol. 2, Moscow: Russkaya kniga, 2003, pp. 211–368, ISBN 5-268-00524-3**. The current work index resolves to permanent revision `oldid=5633449` and links forty separately addressable record pages.

## Decision

**FantLab work 20055 is rejected as an M2 parity-benchmark seed under the current >=300k rule.** Even if its exact analyzer input were later identified, the published analyzed input remains below the standing size gate.

The decision is deliberately narrower than a title-level or public-source rejection. The Russian Wikisource source is a distinct, unmeasured public body. The work-index oldid freezes only that index/navigation page, not the forty linked literary record pages, so it cannot stand in for source-body identity. Any separate corpus-admission decision requires an explicit ordered set of exact body-page revisions, deterministic extraction/composition, and measured character count.

## Production

Added or updated:

- `corpus/candidates/screenings/zamyatin-we-ru.json` — source-free machine decision with exact FantLab threshold arithmetic, legal/source-family evidence, the work-index/body-page boundary, closed M2 gate, and explicit `unknown_until_source_body_is_frozen_and_measured` status for the distinct public source;
- `corpus/candidates/screenings/README.md` — public screening navigation and the narrow *We* result;
- `project/CHANGELOG.d/SCRIP-CORPUS-055.md` — durable semantic delta;
- `project/STATE_AND_QUEUE.md` — authoring/review-pending state;
- this run receipt.

No literary source text, body revision bytes, extracted body, OCR, diagnostics, or copyrighted payload is stored.

## Verification

Fresh public evidence was re-read before writing the decision. FantLab's 285,704-character count and 43,500-word count are taken from the public `work20055/lp` surface dated 17 September 2022. Russian Wikisource was rechecked for the 2003 source-family citation, public-domain surface, current permanent index revision `oldid=5633449`, and the forty linked record entries.

The arithmetic is exact: `300000 - 285704 = 14296`.

The substantive PR is left Draft for a later independent exact-head review. That later review must inspect the final diff, verify settled checks, preserve the index-vs-body revision boundary, and merge only if no blocker remains.

## Gate judgement

Advanced:

- corpus candidate qualification discipline for another high-interest early-20th-century diversity lead;
- explicit durable rejection of FantLab work 20055 as an M2 seed before unnecessary source-match work;
- preserved public-domain/source-family evidence for a separately justified future source-freeze-and-measure pass;
- explicit guard against mistaking a Wikisource work-index oldid for the identity of forty separate body pages.

Not advanced:

- corpus admission or rejection of the distinct Russian Wikisource body;
- body-page revision identity or deterministic composite identity;
- FantLab analyzer-input identity;
- diagnostics or parity;
- M2. M2 remains **0/5**.

## Handoff

Review the exact final Draft PR head independently after repository checks settle. Confirm the source-free screening, threshold arithmetic, public-source boundary, and absence of literary source text. If clean, mark Ready and merge with expected-head protection; then reconcile Issue #197, this receipt, changelog fragment, and canonical state.
