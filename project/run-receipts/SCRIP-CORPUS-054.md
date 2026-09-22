# Run receipt — SCRIP-CORPUS-054

Date: 2026-09-22
Mode: corpus / provenance
Issue: #195
Pull request: #196 (Draft; authored in this wake, independent review pending)
Base at selection: `059a79360065497bbbc9d90bce99d58b991e62b9`

## Selection

The repository had no open pull requests or issues, no recovery work, and `STATE_AND_QUEUE.md` exposed only P2 `SCRIP-CORPUS continuation`. Rather than spend a later source-freezing unit on an attractive diversity lead without first checking its benchmark eligibility, this bounded pass screened Alexei N. Tolstoy's *Aelita* against the standing >=300,000-character gate using current FantLab and Russian Wikisource evidence.

## Fresh evidence

FantLab work `44822` exposes a linguistic-analysis page dated **18 September 2022**. Rechecked on 2026-09-22, it reports:

- **276,556 characters**;
- **39,158 words**.

The project manifest requires an admitted parity-benchmark work to contain at least **300,000 characters including spaces**. FantLab's analyzed input is therefore **23,444 characters below** the mandatory floor.

Russian Wikisource separately exposes a reviewed *Aelita* page and marks the literary work public domain in Russia / life+70-or-less jurisdictions. Its bibliographic/source note identifies **A. N. Tolstoy, Collected Works in ten volumes, vol. 3, Moscow: Goslitizdat, 1958**, while also saying the text follows the **1939 `Советский писатель`** collection. The page further states that the original 1922–1923 *Aelita* text underwent substantial authorial revision.

## Decision

**FantLab work 44822 is rejected as an M2 parity-benchmark seed under the current >=300k rule.** Even if its exact analyzer input were later identified, the published analyzed input remains below the standing size gate.

The decision is deliberately narrower than a title-level corpus rejection. FantLab's 276,556-character input does not prove that every materially revised public *Aelita* edition is below 300,000 characters. The Russian Wikisource source is a distinct, unmeasured public source: its non-M2 corpus admissibility remains `unknown` until a future unit freezes its own literary body and measures its character count. Legal/public-domain evidence does not substitute for that measurement, and the 1939/1958 source-family evidence is not a FantLab analyzer-input match.

## Production

Added:

- `corpus/candidates/screenings/tolstoy-aelita-ru.json` — source-free machine decision with exact threshold arithmetic for FantLab work 44822, legal/source-family facts, edition boundary, closed M2 gate, and explicit `unknown_until_source_body_is_frozen_and_measured` status for the distinct public source;
- `corpus/candidates/screenings/README.md` — public explanation of qualification screenings and the narrow *Aelita* result;
- `project/CHANGELOG.d/SCRIP-CORPUS-054.md` — durable semantic delta, including the correction of an initially over-broad title-level rejection during the same authoring wake;
- `project/STATE_AND_QUEUE.md` revision 221 — `REVIEW_PENDING` with P1 independent review/merge recovery for PR #196;
- this run receipt.

No literary source text, source revision bytes, extracted body, OCR, or copyrighted payload is stored.

## Verification and correction

During authoring verification, inspection of the PR patch exposed an over-broad first formulation that inferred all corpus ineligibility from FantLab's 276,556-character input. That inference was corrected before handoff: materially revised editions are distinct bodies, so their size must be measured independently. The retained conclusion now concerns only M2 eligibility of FantLab work 44822, while a distinct public source remains unmeasured.

The exact-head repository workflow set was then started for the corrected branch. Repository-wide standard-library tests in the Python 3.13 provider-contract job completed successfully on the then-current head; other workflows were still settling before the final corrective commits, so the final head requires a fresh exact-head check in the independent review wake rather than inheriting an earlier success claim.

## Gate judgement

Advanced:

- corpus candidate qualification discipline for a high-interest early-20th-century SF lead;
- explicit durable rejection of FantLab work 44822 as an M2 seed before unnecessary source-match work;
- public/source-free separation of FantLab-input size from a distinct public edition's still-unmeasured body;
- preserved legal and edition-family evidence for possible future short-input showcase or separately justified source freeze.

Not advanced:

- corpus admission or rejection of the distinct Russian Wikisource body;
- source revision/body identity;
- FantLab analyzer-input identity;
- diagnostics or parity;
- M2. M2 remains **0/5**.

## Handoff

Draft PR #196 contains the substantive authored change and must not be self-approved or merged in this wake. A later wake should independently review the exact final head against base `059a79360065497bbbc9d90bce99d58b991e62b9`, inspect fresh settled checks for that exact head, and only then decide whether to mark Ready and merge. The review must preserve the narrow conclusion: FantLab work 44822 is below the M2 >=300k floor; the distinct public Wikisource source is not admitted or rejected for non-M2 corpus use without its own frozen measured body.
