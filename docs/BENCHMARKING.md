# FantLab benchmark harness

Harness profile: `scriptorium-benchmark-v1`  
Output schema: `fantlab-benchmark-comparison-v1`  
Metric contract: `fantlab-2022-v1`

The benchmark harness turns a captured FantLab numeric reference plus a **local** UTF-8
text into a field-by-field comparison artifact. It does not acquire texts, does not
embed source prose in the result, and does not treat numeric resemblance as parity.

## Run it

```bash
python -m scriptorium.benchmark \
  --reference benchmarks/fantlab/work488.json \
  --text /path/to/local-text.txt \
  --scriptorium-revision <git-sha> \
  --edition-match unknown \
  --output comparison.json
```

When an exact, legally usable source edition is established, also provide provenance:

```bash
  --edition-match exact \
  --edition-label "edition/transcription identity" \
  --source-reference "https://... or catalog reference" \
  --legal-basis "public_domain / license / permission evidence"
```

All four provenance claims are required before a source-only integer comparison may
become `pass` or `fail`: `edition_match=exact`, a non-empty edition/transcription
identity, a non-empty source reference, and a non-empty legal basis. The raw SHA-256 is
always computed by the harness from supplied bytes. Missing identity/reference evidence
keeps a numeric match diagnostic `unresolved`.

The text path is never copied into the repository. The output records raw-byte and
normalized-text SHA-256 values instead.

## Optional vocabulary dictionary

Vocabulary metrics that require dictionary membership are disabled unless the caller
supplies both a UTF-8 dictionary file (one lexical form per line) and a stable profile ID:

```bash
  --dictionary /path/to/dictionary.txt \
  --dictionary-profile my-dictionary-v1
```

Scriptorium normalizes/deduplicates that lexeme collection and records the profile plus
its canonical normalized-set SHA-256 in the deterministic artifact. The benchmark
`dictionary_version` is rendered as `PROFILE@sha256:DIGEST`.

This makes an external dictionary reproducible; it does **not** make the dictionary
FantLab-compatible. FantLab's production dictionary identity/version is not established,
so active-dictionary, active-nondictionary and UASZ comparisons remain `unresolved` even
when the supplied dictionary produces an identical number on an exact source edition.

## Current comparable surface

The harness now maps 28 FantLab-namespaced metric IDs emitted by
`scriptorium-metrics-v3`:

- four general scalars;
- four dialogue scalars;
- six vocabulary scalars;
- fourteen punctuation rates.

`fantlab.vocabulary.unique_words` is available without a dictionary. Active dictionary,
active non-dictionary and UASZ actuals are `null` unless an explicit dictionary dependency
is supplied. `work488.json` contains five of the six vocabulary fields; it has no captured
UASZ-100000 value.

Unimplemented page and later fields remain absent rather than being fabricated as zero.
POS work-page distribution rows are now an **optional, explicitly inferred** join; see below.


## Optional source-free POS distribution join (#287)

Use the canonical benchmark with a separately produced `scriptorium-pos-metrics-v1`
artifact from **the same normalized input text**:

```bash
python -m scriptorium.benchmark \
  --reference benchmarks/fantlab/work488.json \
  --text /path/to/your-legal-local-input.txt \
  --scriptorium-revision <git-sha> \
  --pos-metrics /path/to/source-free-pos-metrics.json \
  --edition-match unknown --output benchmark-with-pos.json
```

The optional `--pos-metrics` flag adds **40** rows: defined/undefined POS
counts and shares (4), service-word count/share (2, **actual null/unresolved**),
and 17 visible work-page category counts/shares (34). No additional external
dependency is installed. Without the flag, previous benchmark output is
unchanged.

The POS JSON must originate from the versioned `analyze_pos_metrics` API
and genuine token-aligned morphology input, not manual category assignments
or guessed FantLab homonyms. It is checked against the benchmark's normalized
SHA-256, word and sentence counts, metric/text/POS/mapping profiles, full
17×17 bigram and 20×17 position matrix shape, denominators and internal
accounting. Duplicate JSON keys, NaN/Infinity and inconsistent values fail
closed. The module does **not** download source texts or accept morphology
results for a different text.

**Important methodology:** the published FantLab work488 category counts
sum to 46,879 although its defined-word count is 40,522. Their bucket
counts are *not* a one-bucket-per-word partition. The Scriptorium
`scriptorium-pos-v1` profile is conservative and does produce a defined
token partition. Both sets are preserved without silently reinterpreting
FantLab's unknown homonym/categorization methodology. Percentages retain
their reference decimal lexemes, but displayed rounding/tie rules are
unproven. All 40 comparison rows remain diagnostic/unresolved even for
an asserted exact source edition; numerical coincidence is never a parity
PASS. Service-word semantics, AOT `N` ambiguity and the five methodology-only
categories remain unresolved. M2 is still 0/5. This contribution does not
claim that the user-supplied POS artifact or its declared SHA is independently
authenticated.

## Reference display evidence

`work488.json` predates the comparison runner and stores numeric values directly. Normal
JSON parsing would turn a lexical value such as `10.30` into the number `10.3`, losing
what the captured reference actually recorded. The harness therefore parses the
reference twice: once numerically and once with JSON numeric tokens preserved as strings.
The preserved token becomes `expected.display_text`.

This preserves evidence; it does **not** infer decimal precision. A displayed `10.30`
still has `display_places: null` unless precision was established independently for that
exact field and reference surface.

## Result rules

### Integer counts

General character/word counts and dictionary-free unique vocabulary use `exact_integer`.
With admissible source provenance they may produce `pass` or `fail`; without it they stay
`unresolved`.

Dictionary-dependent integer counts add a second gate: the FantLab production dictionary
must also be identified and matched. The current project has no such evidence. Therefore:

- without any dictionary actual, active-dictionary/non-dictionary rows are `not_run`;
- with an explicit but unproven dictionary, the raw value/delta are diagnostic and the
  result remains `unresolved` even when numerically equal.

### Decimal/rate fields

Mean lengths, dialogue shares, UASZ scalars and punctuation rates currently use
`unresolved_precision`. The harness records actual raw values and deltas where available,
but sets `numeric_match: null` and keeps the result `unresolved` because FantLab's
formatting precision and tie rule are not independently established.

The frozen comparison-v1 schema requires every `unresolved_precision` row to have
`result: unresolved`; therefore a missing UASZ actual is also `unresolved` rather than
`not_run`. Its reason additionally records that the analyzer produced no numeric value.
The harness never widens an interval from visible decimal digits and never substitutes
Python rounding for FantLab behavior.

## `Шутиха` today

`benchmarks/fantlab/work488.json` remains a reference-only target: Scriptorium has not
established a legally usable exact source edition for the FantLab analysis, nor the
FantLab production dictionary. A normal diagnostic run therefore cannot advance M2.

The benchmark harness makes these gates executable; it does not solve the source-edition
or dictionary-provenance research problems by itself.
