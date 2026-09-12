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

All four provenance claims are required before an integer comparison may become
`pass` or `fail`: `edition_match=exact`, a non-empty edition/transcription identity,
a non-empty source reference, and a non-empty legal basis. The raw SHA-256 is always
computed by the harness from the supplied bytes. Missing identity/reference evidence
keeps the comparison diagnostic `unresolved` even if the numeric value matches.

The text path is never copied into the repository by the harness. The output records the
raw byte SHA-256 and the normalized-text SHA-256 instead.

## Current comparable surface

The first executable harness compares the 18 FantLab-namespaced metrics already emitted
by `scriptorium-metrics-v1`:

- text characters and words;
- mean word length and mean sentence length;
- all 14 punctuation frequencies per 1000 words.

Fields captured in a reference but not yet implemented (pages, dialogue, vocabulary,
POS, and later families) are left out rather than fabricated as zero or `not_run` rows.
They enter the comparison only when their analyzer implementation exists.

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

`fantlab.general.characters` and `fantlab.general.words` use `exact_integer`.

- exact edition identity + source reference + legal basis + raw digest + equality -> `pass`;
- the same admissible provenance + disagreement -> `fail`;
- equality or disagreement without any one of those provenance elements -> `unresolved`.

The last rule is deliberate: a different or unidentified edition can be numerically
close or even equal without proving reproduction.

### Decimal/rate fields

Mean lengths and punctuation rates currently use `unresolved_precision`. The harness
records the actual raw value and raw delta, but sets `numeric_match: null` and keeps the
result `unresolved` because FantLab's formatting precision and tie rule are not yet
independently established. It never widens an interval from the number of visible decimal
digits and never substitutes Python rounding for FantLab behavior.

## `Шутиха` today

`benchmarks/fantlab/work488.json` remains a reference-only target: Scriptorium has not
established a legally usable exact source edition for the FantLab analysis. Therefore a
normal diagnostic run against a user-supplied or unmatched text cannot advance M2 and
must not produce a parity `pass` for this work.

The benchmark harness makes the gate executable; it does not solve the source-edition
research problem by itself.
