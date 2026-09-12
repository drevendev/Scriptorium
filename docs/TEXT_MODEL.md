# Text model

Profile ID: `scriptorium-text-v1`

Status: **inferred candidate**, not reproduced FantLab behavior.

This is the first executable text-structure layer used by Scriptorium. It exists so
later metrics can be deterministic and benchmarked instead of embedding ad-hoc text
rules inside each metric.

## Normalization

`normalize_text()` performs exactly two transformations:

1. CRLF and bare CR line endings become LF;
2. Unicode is normalized to NFC.

It deliberately preserves other whitespace, punctuation, case, quote style and dash
style. Raw-source identity belongs to ingestion/provenance; offsets produced by this
module always reference the normalized text.

## Candidate word tokens

`word_tokens()` returns half-open `TextSpan(text, start, end)` records into normalized
text.

The v1 candidate rule treats Unicode alphanumeric word bodies as tokens and preserves
an internal ASCII apostrophe, right single quotation mark, or hyphen when it connects
two token bodies. Underscores and surrounding punctuation split tokens.

This is a deterministic implementation choice. FantLab's exact tokenization and lexeme
normalization remain unknown and must be tested against source-matched benchmarks before
this behavior can be called reproduced.

## Candidate sentence spans

`sentence_spans()` treats a run of `.`, `!`, `?`, or `…` as a sentence terminator when
it is followed by whitespace or end-of-text. Closing quotes/brackets immediately after
the terminator stay inside the sentence. Leading/trailing whitespace is excluded from
the returned span. A final non-whitespace tail without terminal punctuation is returned
as a sentence candidate.

The profile intentionally has no abbreviation dictionary or hidden heuristic. Inputs
such as initials, abbreviations, decimal numbers and unusual punctuation may therefore
differ from FantLab. Those differences are benchmark questions, not reasons to silently
add guesses.

## Verification

`tests/test_text.py` provides golden cases for:

- newline and NFC normalization;
- preservation of non-newline whitespace/punctuation;
- Cyrillic, numeric, hyphenated and apostrophe-containing word candidates;
- exact normalized-text offsets;
- `.`, `?`, `!`, ellipsis-like runs and closing quotes;
- unterminated tail text and blank input;
- repeatability on identical input.

The module uses only the Python standard library. The initial unit deliberately does not
implement dialogue segmentation, punctuation metrics, morphology, source acquisition,
or a claim of FantLab parity.

## Next public slice

Once the first deterministic character/word/sentence metrics are implemented on top of
this model, Scriptorium should analyze one or more legally usable long works and publish
derived result artifacts plus provenance in the repository. The project should not wait
for the complete analyzer before showing real book output.
