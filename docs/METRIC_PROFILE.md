# Deterministic metric profile

Metric profile: `scriptorium-metrics-v4`  
Text profile: `scriptorium-text-v1`  
Dialogue profile: `scriptorium-dialogue-v1`  
Vocabulary profile: `scriptorium-vocabulary-v1`  
Punctuation profile: `scriptorium-punctuation-v2`  
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

FantLab's 2022 work page exposes 14 punctuation frequencies per 1000 words, and the
public methodology says the analyzer measures frequencies of known punctuation marks.
The public row rendered with `-` is labelled `тире`, but FantLab does not publish a
hyphen/dash classifier. `scriptorium-punctuation-v2` therefore remains an inferred
candidate rather than a recovered rule.

Multi-character forms are greedily consumed before component glyphs:

- `?..` and `?…` → `question_ellipsis`;
- `!..` and `!…` → `exclamation_ellipsis`;
- `!!!` → `triple_exclamation`;
- `?!` → `question_exclamation`;
- `...` and `…` → `ellipsis`.

Single glyphs then map to comma, period, exclamation, question, colon and semicolon.
U+2010..U+2014 dash-family glyphs remain `dash` candidates. ASCII hyphen-minus is also a
`dash` candidate **except** when that exact character is retained inside a
`scriptorium-text-v1` word token; in that role the text profile already treats it as a
lexical connector, so punctuation-v2 does not simultaneously count it as punctuation.
This rule applies equally to letter and digit token bodies because it is defined from the
versioned token stream rather than from a language-specific lexical guess. Spaced or
otherwise token-external ASCII hyphens continue to count as dash candidates.

This change fixes an internal double-role inconsistency exposed by `SCRIP-TEXT-004`; it
is not justified by numerical closeness to the source-unmatched *Anna Karenina*
diagnostic. `scriptorium-punctuation-v1` remains the historical all-supported-dash-glyph
policy recorded by older artifacts.

Double-quote families are counted as individual quote events. `parentheses` counts
opening `(` glyphs as candidate pair events. All punctuation choices remain `inferred`.

## Artifact contract

`schemas/scriptorium-deterministic-metrics-v4.schema.json` freezes:

- the v4 aggregate metric profile plus text/dialogue/vocabulary and punctuation-v2
  profile identifiers;
- 29 metric rows: 5 general/diagnostic + 4 dialogue + 6 vocabulary + 14 punctuation;
- per-row unit, definition-evidence class and compatibility status;
- normalized-text SHA-256;
- optional vocabulary dictionary dependency identity as profile + canonical normalized
  lexeme-set SHA-256 + lexeme count.

Punctuation rows additionally preserve raw event counts. Dependency metadata is analysis
provenance, not an extra FantLab metric. The v3 schema remains in the repository for
historical artifacts produced under punctuation-v1; it is not rewritten in place.

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
normalization and rolling windows, punctuation compound overlap, lexical-hyphen
exclusion, dependency digests, schema/profile identity and benchmark gates.

Source-matched benchmark work remains required before any FantLab metric can move from
`inferred` to `reproduced`.
