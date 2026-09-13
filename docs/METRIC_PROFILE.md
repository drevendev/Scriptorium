# Deterministic metric profile

Metric profile: `scriptorium-metrics-v3`  
Text profile: `scriptorium-text-v1`  
Dialogue profile: `scriptorium-dialogue-v1`  
Vocabulary profile: `scriptorium-vocabulary-v1`  
Punctuation profile: `scriptorium-punctuation-v1`  
Metric contract: `fantlab-2022-v1`

Status: **inferred compatibility candidate**.

The FantLab field names identify the public surface being reconstructed; they do not
imply that Scriptorium's current normalization, segmentation, dictionary, window or
counting rules are reproduced.

## General metrics

`analyze_deterministic_metrics()` emits:

| Metric | Candidate rule | Status |
| --- | --- | --- |
| `fantlab.general.characters` | Python character count of normalized text | inferred |
| `fantlab.general.words` | number of `scriptorium-text-v1` word tokens | inferred |
| `scriptorium.general.sentences` | number of candidate sentence spans | extension |
| `fantlab.general.mean_word_length_chars` | mean Python length of candidate word-token text | inferred |
| `fantlab.general.mean_sentence_length_chars` | mean Python length of trimmed candidate sentence spans | inferred |

The mean metrics return `null` when their denominator is zero. Character length,
tokenization, sentence boundaries and denominator details remain benchmark questions.

## Dialogue metrics

`scriptorium-dialogue-v1` supplies four FantLab-shaped scalar candidates:

- mean narration sentence length;
- mean dialogue sentence length;
- dialogue share;
- author text inside dialogue share.

Paragraph classification, embedded author-remark grammar and denominator choices remain
explicitly inferred. See [`DIALOGUE_MODEL.md`](DIALOGUE_MODEL.md).

## Vocabulary metrics

`scriptorium-vocabulary-v1` adds six rows:

- unique words;
- active dictionary vocabulary;
- active non-dictionary vocabulary;
- UASZ-3000;
- UASZ-10000;
- UASZ-100000.

The dictionary-free unique count uses case-folded `scriptorium-text-v1` word tokens.
Dictionary-dependent rows require an explicitly supplied dictionary lexeme collection and
profile ID. The artifact records the normalized dictionary-set SHA-256 and lexeme count;
without that dependency those values are `null`. An explicit dictionary remains a
reproducible input, **not** proof that it matches FantLab's production dictionary.

The scalar UASZ candidate averages unique dictionary-lexeme counts across every complete
contiguous N-token window with step 1. This window/aggregation policy is inferred. See
[`VOCABULARY_MODEL.md`](VOCABULARY_MODEL.md).

## Punctuation profile

FantLab's 2022 work page exposes 14 punctuation frequencies per 1000 words. The v1
candidate implements all 14 while keeping normalization and overlap behavior explicit.
Multi-character forms are greedily consumed before component glyphs:

- `?..` and `?…` → `question_ellipsis`;
- `!..` and `!…` → `exclamation_ellipsis`;
- `!!!` → `triple_exclamation`;
- `?!` → `question_exclamation`;
- `...` and `…` → `ellipsis`.

Single glyphs then map to comma, period, exclamation, question, colon and semicolon.
ASCII hyphen plus U+2010..U+2014 dash variants map to `dash`. Double-quote families are
counted as individual quote events. `parentheses` counts opening `(` glyphs as candidate
pair events. All choices remain `inferred`.

## Artifact contract

`schemas/scriptorium-deterministic-metrics-v3.schema.json` freezes:

- all profile identifiers;
- 29 metric rows: 5 general/diagnostic + 4 dialogue + 6 vocabulary + 14 punctuation;
- per-row unit, definition-evidence class and compatibility status;
- normalized-text SHA-256;
- optional vocabulary dictionary dependency identity as profile + canonical normalized
  lexeme-set SHA-256 + lexeme count.

Punctuation rows additionally preserve raw event counts. Dependency metadata is analysis
provenance, not an extra FantLab metric.

## Public showcase

The repository currently has two versioned derived showcase artifacts from public-domain
*Anna Karenina* excerpts. They intentionally preserve the metric profile available when
they were generated rather than being silently rewritten as newer metric profiles land.
They contain provenance, hashes and derived metrics only, no source prose, and remain
non-corpus/non-parity examples.

A future vocabulary showcase should regenerate from a provenance-bound source selection
rather than invent values from a digest alone. Full-work derived artifacts remain the
preferred direction as ingestion/source freezing matures.

## Verification boundary

Golden tests cover deterministic text/dialogue behavior, general formulas, vocabulary
normalization and rolling windows, punctuation overlap, dependency digests, schema/profile
identity and benchmark gates.

Source-matched benchmark work remains required before any FantLab metric can move from
`inferred` to `reproduced`.
