# FantLab parity-corpus candidates

This document explains the first seed catalog in
`corpus/candidates/fantlab-parity-v1.json`.

## What counts as a retained candidate

A retained candidate in `SCRIP-CORPUS-001` must have all three of the following:

1. a FantLab linguistic-analysis (`/lp`) surface with an observed text length of at least
   300,000 characters including spaces;
2. a legally usable source text whose legal basis is documented rather than inferred
   from web accessibility;
3. an explicit source-edition confidence and FantLab-edition match state.

A retained candidate is **not** automatically M2 gate-ready. `gate_ready` remains false
until the exact source edition/bytes behind the FantLab analysis are established and a
raw digest can be frozen. Numeric resemblance on an unknown edition is diagnostic only.

## Legal basis used by the seed catalog

The seed deliberately starts with Russian originals first published in the Russian
Empire before 7 November 1917. Russian Wikisource's copyright policy permits works in
that category under its public-domain rules, and each retained work page carries an
explicit public-domain notice for the literary work. We use those source-site rights
statements as the legal basis for source-text analysis; we do **not** infer rights merely
from web accessibility or claim a broader jurisdictional rule than the cited policy and
work pages establish.

Later editorial introductions, notes, commentary, annotations, scans or other protected
apparatus are outside the corpus input and must not be copied merely because they appear
beside the public-domain work.

Evidence policy:

- https://ru.wikisource.org/wiki/Викитека:Авторские_права

The catalog records the particular Wikisource work page and, where the page supplies it,
the edition from which its transcription was prepared. That bibliographic source is
**provenance**, not proof that FantLab analyzed the same edition.

## Seed result

Five independent full novels currently satisfy the candidate-level legal + length +
FantLab-analysis checks:

| Work | FantLab characters | Legal source provenance | FantLab edition match | Gate-ready |
| --- | ---: | --- | --- | --- |
| Лев Толстой — `Анна Каренина` | 1,692,647 | strong; Wikisource cites Nauka 1970 | unknown | no |
| Лев Толстой — `Воскресение` | 881,244 | moderate; Wikisource cites vol. 6 of an 8-volume collected works | unknown | no |
| Фёдор Достоевский — `Идиот` | 1,302,414 | weak; Wikisource explicitly says the transcription source is not identified | unknown | no |
| Фёдор Достоевский — `Братья Карамазовы` | 1,807,107 | strong; Wikisource cites Nauka 1991, vols. 9–10 | unknown | no |
| Фёдор Достоевский — `Бесы` | 1,252,124 | strong; Wikisource cites Nauka 1990, vol. 7 | unknown | no |

The important result is therefore **5 candidate-eligible, 0 parity-gate-ready**. The
reproduction gate has not moved: FantLab publishes the analysis values but does not name
the source edition or immutable text bytes on these `/lp` pages.

## SCRIP-REPRO-003: Anna Karenina source trace

The first source-matching pass now has a machine-readable trace at
`corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.json`.

What changed:

- FantLab's 19 September 2022 `/lp` surface is frozen as the comparison target at
  1,692,647 characters and 253,275 words, but it still discloses no source edition or
  analyzed bytes.
- FantLab's creator described the analyzer corpus as works **uploaded to the database**;
  author profiles use all uploaded works. Therefore the bibliographic editions listed on
  a work page are not evidence of analyzer-input identity.
- On 13 September 2026, the FantLab TXT "download excerpt" link for the work redirected
  to a LitRes trial endpoint (`art=74152506`). The trace records this as a dated,
  point-in-time observation rather than a stable work identity, and it is not treated as
  evidence for the text that produced the 2022 analysis.
- Russian Wikisource identifies its transcription as coming through the FEB Tolstoy
  electronic edition from `Толстой Л. Н. Анна Каренина. М.: Наука, 1970. С. 5–684`, and
  explicitly marks the literary work public domain.
- The current Wikisource work index has permanent revision `oldid=3829834`, but the novel
  is a composite of 239 separately stored chapter subpages across eight parts. Freezing
  the index revision does **not** freeze those chapter text revisions.

The source identity is therefore **partial**, not exact. This pass deliberately does not
run a diagnostic comparison: the complete candidate bytes are not yet revision-pinned
or hashed, and FantLab's own uploaded source remains unidentified. M2 remains 0/5.

The next source-matching slice for this candidate is mechanical and testable: build a
revision-pinned manifest for the 239 chapter subpages, freeze extraction/concatenation
order, acquire those exact public-domain revision texts, and compute raw/normalized
SHA-256 plus character count. Only then can Scriptorium run a useful diagnostic against
FantLab. Even a close numeric match remains diagnostic until independent evidence ties
FantLab's uploaded analysis text to the same frozen source.

## Held leads

The machine-readable catalog also records leads that should not be silently promoted:

- `Война и мир. Том первый` has a legal source and a 710,180-character FantLab analysis,
  but FantLab analyzes it as a volume-level work. It is held until Scriptorium decides
  whether a volume can count as an independent M2 work; it does not count toward the
  seed five.
- `Преступление и наказание` has a public-domain Wikisource transcription and a confirmed
  FantLab work identity, but this run did not verify a retrievable `/lp` surface and
  threshold count.
- `Обломов` has a public-domain source, but this run did not verify its FantLab `/lp`
  surface and threshold count.

These records exist so a later run can continue from the missing evidence instead of
repeating discovery.

## Next evidence needed

`SCRIP-CORPUS-001` establishes candidate availability, not source matching. The next
corpus-focused investigation should try to identify FantLab's ingestion source or derive
source-edition evidence from exact text-level fingerprints. A candidate may move toward
M2 only when all of the following exist:

- exact candidate text bytes acquired under the recorded legal basis;
- immutable raw SHA-256 and normalized SHA-256;
- character count including spaces for those bytes;
- evidence that the candidate edition is the exact FantLab edition, not merely the same
  literary work;
- field-by-field benchmark output using the versioned FantLab comparison contract.

Do not compensate for an unknown edition by weakening tolerance or by selecting whichever
public-domain transcription happens to be numerically closest.

## Diversification trace: Darwin / Rachinsky 1864

`darwin-origin-species-rachinsky-1864-ru` is a source-traced **nonfiction / history-of-science** lead added to reduce the retained corpus's fiction-heavy concentration. Russian Wikisource identifies the translation as Sergey A. Rachinsky's 1864 Saint Petersburg edition from bookseller A. I. Glazunov and exposes a completed 399-page ProofreadPage index.

Scriptorium now pins three source-free layers of route evidence: rendered edition-family revision `oldid=5628021`, ProofreadPage index revision `oldid=4494408`, and a machine-readable child graph with exact permanent revisions for numbered rendered routes `/1`–`/14` plus `/Указатель`. The numbered route metadata covers displayed bibliographic pp. **1–387**; the alphabetical index covers **389–399**; displayed p. **388** is explicitly unclassified rather than silently composed.

The rendered route graph still does **not** freeze the underlying Page-namespace revisions, mapping from displayed print pages to scan/Page sequence positions, scan binary, extraction/composition contract, literary-body count or digests. The **399-page bibliographic length and rendered page spans are not accepted as proof of the >=300,000-character rule**, so this candidate is not yet admitted to calibration/profile work.

FantLab work `969964` is retained only as a work-level cross-reference: its currently exposed Russian translation is K. Timiryazev, not Rachinsky. Therefore no FantLab source/analyzer-input identity or linguistic-result match is claimed, `diagnostic_ready=false`, `gate_ready=false`, `m2_parity_admissible=false`, and M2 remains 0/5.

Canonical evidence:

- `../corpus/candidates/darwin-origin-species-rachinsky-1864-ru.md` — public source-free candidate note and strict admission boundary.
- `../corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json` — structured translation identity, parent/index locators, rights evidence, route-graph pointer and next freeze requirements.
- `../corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.source-graph.json` — exact 15-route revision graph, displayed print-page spans, explicit p. 388 gap and underlying-Page freeze boundary.
