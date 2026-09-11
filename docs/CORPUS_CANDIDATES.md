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

The seed deliberately starts with Russian originals that were first published in the
Russian Empire before 7 November 1917. Russian Wikisource's copyright policy states that
works in that category are public domain worldwide, and each retained work page marks the
literary work as public domain. We use that as the legal basis for source-text analysis.
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
