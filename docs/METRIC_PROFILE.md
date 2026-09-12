# Deterministic metric profile

Metric profile: `scriptorium-metrics-v1`  
Punctuation profile: `scriptorium-punctuation-v1`  
Metric contract: `fantlab-2022-v1`

Status: **inferred compatibility candidate**.

This profile is the first executable metric layer on top of
`scriptorium-text-v1`. The FantLab field names identify the public surface being
reconstructed; they do not imply that the current counting rules are reproduced.

## General metrics

`analyze_deterministic_metrics()` emits:

| Metric | Candidate rule | Status |
| --- | --- | --- |
| `fantlab.general.characters` | Python character count of normalized text | inferred |
| `fantlab.general.words` | number of `scriptorium-text-v1` word tokens | inferred |
| `scriptorium.general.sentences` | number of candidate sentence spans | extension |
| `fantlab.general.mean_word_length_chars` | mean Python length of candidate word-token text | inferred |
| `fantlab.general.mean_sentence_length_chars` | mean Python length of trimmed candidate sentence spans | inferred |

The two mean metrics return `null` when their denominator is zero. Character
length, tokenization, sentence boundaries and denominator details are still benchmark
questions because FantLab does not publish enough implementation detail to prove the
candidate rules.

## Punctuation profile

FantLab's 2022 work page exposes 14 punctuation frequencies per 1000 words. The v1
candidate implements all 14 while keeping normalization and overlap behavior explicit.

The scanner is left-to-right. Multi-character forms are consumed before component
glyphs, so a punctuation run contributes to at most one compound/single category at
that position:

- `?..` and `?…` → `question_ellipsis`;
- `!..` and `!…` → `exclamation_ellipsis`;
- `!!!` → `triple_exclamation`;
- `?!` → `question_exclamation`;
- `...` and `…` → `ellipsis`.

Single glyphs then map to comma, period, exclamation, question, colon and semicolon.
ASCII hyphen plus U+2010..U+2014 dash variants map to `dash`. Double-quote families
(`"`, `«`, `»`, `“`, `”`, `„`) are counted as individual `quote` glyph events.
`parentheses` counts opening `(` glyphs as candidate pair events; closing `)` alone
does not increment the metric.

These choices are intentionally easy to inspect and revise. FantLab has not publicly
established Unicode dash/quote normalization, parenthesis pairing, or compound overlap,
so every punctuation value remains `inferred`.

## Artifact contract

`schemas/scriptorium-deterministic-metrics-v1.schema.json` freezes:

- the metric/profile identifiers;
- all five first-wave general/diagnostic rows;
- all 14 FantLab punctuation rows;
- the unit, definition-evidence class and compatibility status of every row;
- the normalized-text SHA-256 used by the metric artifact.

Punctuation rows also preserve the raw event count next to the normalized per-1000-word
value. This is diagnostic evidence, not an extra FantLab metric.

## Public showcase

`showcase/anna-karenina-part1-ch1-opening.json` is the first real-text derived artifact.
It analyzes only the first four prose paragraphs of Part I, Chapter I of Tolstoy's
*Anna Karenina*, from Russian Wikisource revision `oldid=4929732`, joining those four
paragraphs with LF.

The literary work is public domain and Wikisource identifies the chapter source as
Tolstoy, *Anna Karenina*, Moscow: Nauka, 1970, pp. 7–9. No source prose is stored in this
repository; the showcase stores source identity, selection rule, hashes and derived
metrics only.

The showcase is deliberately marked `illustrative_excerpt`. At 1,298 selected
characters it is far below Scriptorium's 300,000-character corpus threshold, is not a
parity corpus entry, and cannot produce a FantLab `pass`. Its purpose is to make the
current executable capability visible while full-work ingestion/provenance remains a
separate unit.

## Verification boundary

Golden tests cover:

- zero denominators;
- exact first-wave general formulas;
- compound punctuation non-overlap;
- raw punctuation counts and per-1000 rates;
- deterministic normalized digests;
- the schema/profile identity.

Source-matched benchmark work remains required before any FantLab metric can move from
`inferred` to `reproduced`.
