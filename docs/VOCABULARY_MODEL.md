# Deterministic vocabulary profile

Vocabulary profile: `scriptorium-vocabulary-v1`  
Metric profile: `scriptorium-metrics-v3`  
Metric contract: `fantlab-2022-v1`

Status: **inferred compatibility candidate**.

FantLab's public methodology defines the high-level vocabulary family: unique words,
active dictionary vocabulary, active non-dictionary vocabulary, and UASZ windows of
3,000, 10,000 and 100,000 words. It also says UASZ counts unique dictionary words after
removing repeats and excluding non-dictionary words. The production dictionary,
lexical-normalization details, exact scalar window placement/step and aggregation policy
are not public. Scriptorium therefore keeps each candidate choice versioned and visible.

Primary methodology evidence: `https://fantlab.ru/article374`.

## Lexical identity

`scriptorium-vocabulary-v1` takes the ordered `scriptorium-text-v1` word tokens and uses
Unicode NFC followed by Unicode `casefold()` as lexical identity. The same NFC +
case-fold rule is applied to explicit dictionary entries before membership checks and
dependency hashing. It deliberately does **not**:

- lemmatize words;
- fold `ё` into `е`;
- alter the text profile's internal hyphen/apostrophe behavior;
- guess spelling corrections or morphology.

Consequently `Кот`, `кот`, and `КОТ` are one candidate lexeme, and canonically equivalent
spellings such as composed `ёж` and decomposed `е` + U+0308 + `ж` share one candidate
identity. Different inflected forms remain different lexemes. This is an inspectable
reconstruction, not a claim about FantLab's private lexical pipeline.

`fantlab.vocabulary.unique_words` is available without any external dictionary and is
the number of unique candidate lexemes in the input.

## Dictionary dependency

Scriptorium does not bundle or silently select a dictionary for this profile. The caller
may supply an explicit lexeme collection only together with a non-empty dictionary
profile ID. The collection is normalized with the same NFC + case-fold rule,
deduplicated, and bound into the metric artifact as:

```text
dependencies.vocabulary_dictionary.profile
dependencies.vocabulary_dictionary.normalized_lexemes_sha256
dependencies.vocabulary_dictionary.lexeme_count
```

The SHA-256 covers the canonical sorted normalized lexeme set, so canonically equivalent
Unicode spellings yield the same dependency identity while genuinely different
collections cannot be hidden behind the same profile label without changing the artifact.

Without this dependency the following values are `null`, never fabricated as zero:

- `fantlab.vocabulary.active_dictionary`;
- `fantlab.vocabulary.active_nondictionary`;
- `fantlab.vocabulary.uasz_3000`;
- `fantlab.vocabulary.uasz_10000`;
- `fantlab.vocabulary.uasz_100000`.

Even when a dictionary is supplied, Scriptorium does **not** claim it is FantLab's
production dictionary. Benchmark rows depending on it therefore remain `unresolved`
until dictionary identity/version compatibility is independently established.

## Active vocabulary candidate

With an explicit dictionary dependency:

- active dictionary vocabulary = unique candidate lexemes present in that dictionary;
- active non-dictionary vocabulary = unique candidate lexemes absent from it.

Both are `public_definition` / `inferred`: FantLab publishes the semantic family, while
its exact dictionary/version and lexical normalization remain open compatibility work.

## UASZ scalar candidate

For each N in 3,000 / 10,000 / 100,000, the v1 scalar candidate is:

1. take every **complete contiguous N-token window**;
2. advance the window by one token each time;
3. exclude lexemes absent from the explicit dictionary;
4. count unique remaining dictionary lexemes in that window;
5. return the arithmetic mean across all complete windows.

A text shorter than N has no complete window and returns `null`. Incomplete tail windows
do not contribute. The implementation maintains a rolling frequency counter, so each
window family is O(number of words) rather than rebuilding a set for every position.

FantLab's exact window step, edge policy, dictionary and scalar aggregation are not
published. These choices remain `inferred` until source-matched benchmark pressure can
discriminate them. The methodology's UASZ-3000 dynamics graph is also a separate public
series and is not implemented by this scalar unit.

## Benchmark boundary

The benchmark harness exposes all six vocabulary fields when the captured reference has
them. `unique_words` can participate in the ordinary source-provenance gate without a
dictionary. Dictionary-dependent integer counts are `not_run` when no dictionary value
was produced; if an explicit dictionary is supplied, their numeric comparison remains
`unresolved` because FantLab dictionary compatibility is not established.

UASZ values use the frozen benchmark v1 `unresolved_precision` rule. Therefore a missing
UASZ actual value is still an `unresolved` row rather than `not_run`: the comparison
schema deliberately freezes all `unresolved_precision` rows to `result: unresolved`.
Visible decimal digits are not used as a precision oracle.

## Verification boundary

Golden tests cover lexical normalization including composed/decomposed Unicode equality,
missing-dependency behavior, active-vocabulary partitioning, immutable dictionary
identity, rolling-window edge behavior, the real 3,000-token window size, artifact/schema
identity, and benchmark admission behavior.

None of these tests promote the profile from `inferred` to `reproduced`. Source-matched
FantLab benchmarks and a justified dictionary compatibility story remain required.
