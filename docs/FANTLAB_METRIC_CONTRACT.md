# FantLab metric contract

Contract ID: `fantlab-2022-v1`

Status: research/specification. This document fixes identifiers, units, evidence status
and benchmark semantics before analyzer implementation. It does **not** claim that the
underlying FantLab implementation has been reproduced.

## Primary evidence

- `https://fantlab.ru/article374` describes the analyzer, the major metric families,
  dictionary-only active-vocabulary windows, POS families, author-profile weighting and
  the fact that some corrective coefficients/know-how are unpublished.
- `https://fantlab.ru/work12625/lp` is a concrete 18 September 2022 analysis page. It
  exposes the scalar labels, POS table, POS-bigram table, sentence-position POS table and
  punctuation surface used below.
- `https://fantlab.ru/rating/work/lingvo` exposes public ranking fields including SZ10
  (UASZ-10000) and SLEN (mean sentence length).
- `benchmarks/fantlab/work488.json` is Scriptorium's first captured numeric reference.

The exact reference surface matters. A work summary page can show rounded/cached summary
values that are not a substitute for the detailed `/lp` page. Every benchmark therefore
records the exact source URL and observed display text rather than joining values from
multiple FantLab surfaces.

## Evidence vocabulary

Every metric implementation and benchmark result records one of these definition states:

- `public_definition` — FantLab publicly states enough semantic meaning to define the
  quantity, while exact implementation details may still need benchmark confirmation;
- `public_surface` — FantLab publishes the field, unit or table but does not disclose a
  complete computation;
- `inferred_candidate` — Scriptorium has chosen an explicit candidate interpretation;
  it remains inferred until source-matched benchmark evidence supports it;
- `unresolved` — the definition/mapping is not established enough to implement without
  knowingly inventing behavior.

This is separate from compatibility status. Until benchmarks demonstrate parity, a
Scriptorium implementation is `inferred`, never `reproduced`, even for a metric whose
high-level definition is public.

## Stable scalar metric IDs

`display` means the reference display text is captured per benchmark. Decimal precision
is not frozen globally because FantLab pages may omit trailing zeroes.

| Metric ID | FantLab surface label | Unit | Definition evidence | Dependencies / unresolved edge |
| --- | --- | --- | --- | --- |
| `fantlab.general.characters` | `Длина текста, знаков` | characters | `public_surface` | normalization; exact whitespace/code-point rule unknown |
| `fantlab.general.words` | `Слов в произведении (СВП)` | words | `public_surface` | tokenization rule unknown |
| `fantlab.general.approx_pages` | `Приблизительно страниц` | pages | `public_surface` | exact formula/cache semantics unknown; compare only the named source surface |
| `fantlab.general.mean_word_length_chars` | `Средняя длина слова, знаков` | characters/word | `public_surface` | tokenization and character denominator unknown |
| `fantlab.general.mean_sentence_length_chars` | `Средняя длина предложения (СДП), знаков` | characters/sentence | `public_surface` | sentence boundaries and character denominator unknown |
| `fantlab.dialogue.mean_narration_sentence_length_chars` | `СДП авторского текста, знаков` | characters/sentence | `public_surface` | sentence + dialogue segmentation unknown |
| `fantlab.dialogue.mean_dialogue_sentence_length_chars` | `СДП диалога, знаков` | characters/sentence | `public_surface` | sentence + dialogue segmentation unknown |
| `fantlab.dialogue.share_percent` | `Доля диалогов в тексте` | percent | `public_surface` | dialogue unit/denominator unknown |
| `fantlab.dialogue.author_text_inside_dialogue_percent` | `Доля авторского текста в диалогах` | percent | `public_surface` | author-in-dialogue segmentation/denominator unknown |
| `fantlab.vocabulary.unique_words` | `Использовано уникальных слов` | words | `public_definition` | token/lexeme normalization still needs benchmarking |
| `fantlab.vocabulary.active_dictionary` | `Активный словарный запас (АСЗ)` | words | `public_definition` | dictionary identity/version required |
| `fantlab.vocabulary.active_nondictionary` | `Активный несловарный запас (АНСЗ)` | words | `public_definition` | dictionary identity/version required |
| `fantlab.vocabulary.uasz_3000` | `Удельный АСЗ на 3000 слов текста` | unique dictionary words/window | `public_definition` | 3000-word window; aggregation across windows unresolved |
| `fantlab.vocabulary.uasz_10000` | `Удельный АСЗ на 10000 слов текста` | unique dictionary words/window | `public_definition` | 10000-word window; aggregation across windows unresolved |
| `fantlab.vocabulary.uasz_100000` | methodology only | unique dictionary words/window | `public_definition` | 100000-word window; may be unavailable for shorter texts; aggregation unresolved |
| `fantlab.pos.undefined.count` | `Неопределённых частей речи (НОЧР), слов` | words | `public_surface` | morphology backend/version |
| `fantlab.pos.undefined.percent_of_words` | NОЧР `% от СВП` | percent | `public_surface` | morphology backend/version |
| `fantlab.pos.defined.count` | `Определённых частей речи (ОЧР), слов` | words | `public_surface` | morphology backend/version |
| `fantlab.pos.defined.percent_of_words` | ОЧР `% от СВП` | percent | `public_surface` | morphology backend/version |
| `fantlab.pos.service.count` | `Служебных слов` | words | `public_surface` | exact POS-to-service mapping unresolved |
| `fantlab.pos.service.percent_of_defined` | service words `% от ОЧР` | percent | `public_surface` | exact POS-to-service mapping unresolved |

The current >=300,000-character corpus rule is a Scriptorium corpus-admission rule. It
must not be confused with the unknown definition of `fantlab.general.characters`.

## POS buckets and generated fields

The 2022 work-analysis page observed for this contract displays these 17 buckets:

```text
noun
adjective
verb
pronoun_noun
pronoun_adjective
pronoun_predicative
cardinal
ordinal
adverb
predicative
preposition
conjunction
interjection
introductory_word
particle
participle
gerund
```

For each bucket, the scalar metric IDs are:

```text
fantlab.pos.{bucket}.count
fantlab.pos.{bucket}.percent_of_defined
```

The work page states that the percentages use defined-POS words (`ОЧР`) as 100%.

The methodology article additionally names postpositions, phrasal verbs, short
adjectives, short participles and infinitives. Those are **not** silently added as
separate 2022 work-page buckets. `SCRIP-MORPH-001` must determine whether they were
folded into the displayed buckets, disappeared through the current AOT mapping, or are
available on another surface/version.

### POS bigrams

The public work page defines the table as the frequency of ordered POS pairs, expressed
as the average number of pairs per 1000 words. Stable IDs are generated as:

```text
fantlab.pos_bigram.{first_bucket}.{second_bucket}.per_1000_words
```

The current observed table uses the 17 displayed buckets above. Exact token adjacency,
unknown-token handling and punctuation crossing are unresolved until benchmarked.

### POS by sentence position

The work page defines each cell as the probability/percentage that a POS occupies a
numbered word position in a sentence. Stable IDs are:

```text
fantlab.pos_position.{position}.{bucket}.percent
```

The observed 2022 page renders positions 1..10; the methodology says statistics exist up
to position 20. The analyzer should therefore allow 1..20, while a benchmark records
only positions actually present on its exact reference surface.

## Punctuation family

The work page reports average occurrences per 1000 words. Stable IDs use:

```text
fantlab.punctuation.{key}.per_1000_words
```

| Key | Surface token |
| --- | --- |
| `comma` | `,` |
| `period` | `.` |
| `dash` | `-` |
| `exclamation` | `!` |
| `question` | `?` |
| `ellipsis` | `...` |
| `exclamation_ellipsis` | `!..` |
| `question_ellipsis` | `?..` |
| `triple_exclamation` | `!!!` |
| `question_exclamation` | `?!` |
| `quote` | `"` |
| `parentheses` | `()` |
| `colon` | `:` |
| `semicolon` | `;` |

The table does not establish Unicode normalization, dash variants, quote variants,
overlapping-pattern handling or whether paired parentheses are counted as pairs or
characters. Those choices belong to the versioned compatibility profile and remain
`inferred_candidate` until source-matched evidence discriminates them.

## Deferred public series

FantLab also exposes dialogue use through the text and UASZ-3000 dynamics. These are
public compatibility surfaces but are not required to unblock the first scalar metric
implementation:

```text
fantlab.dialogue.share_by_character_window
fantlab.vocabulary.uasz_3000_by_text_position
```

They remain queued as later metric/visual-series work; scalar implementation must not
invent the graph window/edge behavior from the image alone.

## Benchmark comparison contract

`schemas/fantlab-benchmark-comparison-v1.schema.json` is the machine-readable comparison
shape. A comparison artifact never contains the copyrighted source text.

Every comparison records:

- exact FantLab reference URL/date/work identity;
- source-edition confidence and legal basis;
- raw and normalized SHA-256 when source bytes are available;
- analyzer/profile/dependency versions;
- per metric: metric ID, definition evidence, expected numeric value **and exact display
  text**, actual raw value/display text, raw delta when meaningful, numeric match and one
  terminal result.

Allowed results:

- `not_run` — Scriptorium produced no actual value;
- `unresolved` — a numeric comparison may be diagnostic, but parity evidence is not
  admissible (for example the edition is not exact, display precision/tie behavior is
  ambiguous, required provenance is missing, or the metric definition is still
  insufficient);
- `fail` — admissible source-matched comparison disagrees;
- `pass` — admissible source-matched comparison satisfies the declared rule.

A result may not be `pass` unless `source_text.edition_match == "exact"` and the source
has a legal basis plus immutable raw digest. Numeric resemblance on a different or
unknown edition remains `unresolved`.

## Equality and display rounding

### Integer/display-exact counts

For integer count metrics, `exact_integer` requires exact numeric equality to the
published integer. Approximate/page fields may still be numerically equal, but their
`definition_evidence` remains visible so equality alone does not promote the metric to
`reproduced` across the project.

### Decimal display values

FantLab publishes decimal display values but does not publicly specify tie-breaking.
For an expected display with `p` decimal places and numeric display value `d`, define the
non-tie display interval:

```text
step  = 10 ** (-p)
lower = d - step / 2
upper = d + step / 2
```

`display_interval` is a numeric match only when the actual raw value lies strictly inside
`(lower, upper)`. A value exactly on either boundary is `unresolved` until FantLab's tie
rule is established; Scriptorium must not silently choose Python/IEEE rounding and call
that FantLab behavior.

The benchmark stores the original display string because JSON numbers do not preserve
trailing-zero precision. `5.8` and `5.80` therefore have different observed display
precision even though their numeric values are equal.

## Gate semantics

M2's parity gate is stricter than one successful comparison:

1. the exact source edition must be established and legally usable;
2. analyzer/config/dependency identity must be pinned;
3. every published compatibility metric in scope must be `pass` under its declared rule;
4. unexplained missing fields, ties, unknown mappings or deltas remain `unresolved`;
5. the metric can be promoted from `inferred` to `reproduced` only after the project has
   the benchmark evidence required by the manifest, not after one plausible sample.

## Known unresolved definition edges

The implementation queue must treat these as research/benchmark questions rather than
fill them with convenient defaults:

1. exact text normalization and the character-count unit;
2. word-token and lexeme-normalization rules;
3. sentence boundaries and sentence-length denominator;
4. dialogue/author-in-dialogue segmentation;
5. page-estimate formula and summary-vs-detail cache behavior;
6. UASZ window placement and scalar aggregation;
7. AOT dictionary/version, ambiguity resolution and POS mapping;
8. article-only POS labels versus the 17 observed 2022 page buckets;
9. punctuation normalization and overlapping pattern rules;
10. decimal rounding ties.

`SCRIP-TEXT-001`, `SCRIP-METRIC-001` and `SCRIP-MORPH-001` should make candidate choices
explicit and versioned; benchmark evidence decides whether those candidates become
reproduced behavior.