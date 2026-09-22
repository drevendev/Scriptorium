# Run receipt — SCRIP-CORPUS-054

Date: 2026-09-22
Mode: corpus / provenance
Issue: #195
Pull request: #196 (Draft; authored in this wake, independent review pending)
Base at selection: `059a79360065497bbbc9d90bce99d58b991e62b9`

## Selection

The repository had no open pull requests or issues, no recovery work, and `STATE_AND_QUEUE.md` exposed only P2 `SCRIP-CORPUS continuation`. Rather than spend a later source-freezing unit on an attractive but potentially ineligible diversity candidate, this bounded pass screened Alexei N. Tolstoy's *Aelita* against the standing >=300,000-character corpus gate using current FantLab and Russian Wikisource evidence.

## Fresh evidence

FantLab work `44822` exposes a linguistic-analysis page dated **18 September 2022**. Rechecked on 2026-09-22, it reports:

- **276,556 characters**;
- **39,158 words**.

The project manifest requires calibration, parity-benchmark, and author-profile corpus works to contain at least **300,000 characters including spaces**. The FantLab analyzed input is therefore **23,444 characters below** the mandatory floor.

Russian Wikisource separately exposes a reviewed *Aelita* page and marks the literary work public domain in Russia / life+70-or-less jurisdictions. Its bibliographic/source note identifies **A. N. Tolstoy, Collected Works in ten volumes, vol. 3, Moscow: Goslitizdat, 1958**, while also saying the text follows the **1939 `Советский писатель`** collection. The page further states that the original 1922–1923 *Aelita* text underwent substantial authorial revision.

## Decision

*Aelita* is rejected from Scriptorium's calibration corpus, parity-benchmark corpus, and author-profile corpus under the current >=300k rule. This rejection is based on the published FantLab character count alone and is independent of legal usability or source-match uncertainty.

The legal/public-domain evidence remains useful for a possible future **short-input, non-corpus analyzer/showcase** case. Such a future case must preserve edition identity and may not be counted toward M2. The 1939/1958 source-family evidence is not a FantLab analyzer-input match, and no Wikisource revision/body is frozen in this unit.

## Production

Added:

- `corpus/candidates/screenings/tolstoy-aelita-ru.json` — source-free machine decision with the exact threshold arithmetic, FantLab identity/date/counts, legal/source-family facts, edition boundary, closed gates, and allowed future non-corpus use;
- `corpus/candidates/screenings/README.md` — public explanation of qualification screenings and the *Aelita* rejection;
- `project/CHANGELOG.d/SCRIP-CORPUS-054.md` — durable semantic delta;
- `project/STATE_AND_QUEUE.md` revision 221 — `REVIEW_PENDING` with P1 independent review/merge recovery for PR #196;
- this run receipt.

No literary source text, source revision bytes, extracted body, OCR, or copyrighted payload is stored.

## Gate judgement

Advanced:

- corpus candidate qualification discipline for a tempting early-20th-century SF work;
- explicit durable rejection before unnecessary source-freezing work;
- public/source-free explanation that legal usability cannot override the >=300k floor;
- preserved edition-family warning for any future short-input showcase.

Not advanced:

- corpus admission for *Aelita*;
- source revision/body identity;
- FantLab analyzer-input identity;
- diagnostics or parity;
- M2. M2 remains **0/5**.

## Handoff

Draft PR #196 contains the substantive authored change and must not be self-approved or merged in this wake. A later wake should independently review the exact final head against base `059a79360065497bbbc9d90bce99d58b991e62b9`, inspect settled repository checks, and only then decide whether to mark Ready and merge. The review must verify that the absolute size rejection remains separate from legal/source-family evidence and that no edition or FantLab input identity is implied.