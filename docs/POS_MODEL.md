# POS metric model

Profile: `scriptorium-pos-v1`

Schema: `scriptorium-pos-metrics-v1`

Compatibility mapping: `aot-pylem-0.0.18-to-fantlab-2022-v1`

Status: **inferred compatibility candidate**, not reproduced FantLab behavior.

This profile is the deterministic aggregation layer between the pinned AOT/pylem
runtime contract and FantLab-shaped POS statistics. It intentionally does not import or
build pylem. The caller supplies the runtime POS analyses that a provider produced, one
sequence per `scriptorium-text-v1` word token, plus a non-empty runtime-profile identity.
The artifact hashes that exact candidate matrix so the aggregation input is reproducible.

## Why the provider boundary is explicit

Pinned pylem 0.0.18 exposes `LemmaInfo.part_of_speech` as a Latin runtime string. Public
source verification in [`AOT_PYLEM_COMPATIBILITY.md`](AOT_PYLEM_COMPATIBILITY.md)
shows two important losses of information at this boundary:

- noun `С` and cardinal numeral `ЧИСЛ` both become runtime `N`;
- pylem can return multiple analyses, while FantLab's homonym/disambiguation rule is not
  public.

Scriptorium therefore does not pick the first result, use pylem weights, infer noun vs
cardinal from spelling, or fold unresolved extra AOT categories by plausibility.

## Token resolution

A token is **defined** only when all supplied runtime analyses map through the 15 direct
runtime mappings and all map to the same one of FantLab's 17 displayed buckets.

Examples:

```text
[A]       -> adjective
[A, A]    -> adjective
[A, V]    -> undefined
[N]       -> undefined (noun/cardinal collision)
[POSL]    -> undefined (unresolved 2022 folding)
[]        -> undefined
```

Unknown runtime strings are also undefined. This deliberately makes uncertainty visible
instead of forcing percentages to add up.

The two displayed buckets `noun` and `cardinal` are still present in every output matrix,
but the current public pylem string alone cannot populate them safely. A future adapter
may expose a pinned AOT source discriminator; doing so would require a separately
versioned compatibility decision and source-matched benchmark evidence.

## POS distribution

The artifact reports:

- defined words and `% of all Scriptorium word tokens`;
- undefined words and `% of all Scriptorium word tokens`;
- for each of the 17 FantLab buckets, count and `% of defined words`.

This matches the public FantLab surface at the level of names and denominators. The
actual morphology backend/version, tokenization differences and ambiguity handling are
not proven equivalent, so all values remain `inferred`.

`service_words` is emitted as an explicit unresolved record with null values. Current
FantLab pages publish the scalar, but public evidence does not establish the exact
POS-to-service aggregation. Scriptorium does not guess it from familiar grammatical
categories.

## POS bigrams

FantLab's current `/lp` text describes each cell as an ordered POS pair frequency,
expressed as the average number of that pair per 1000 text words. The v1 candidate
therefore uses:

```text
1000 * resolved_pair_count / all_scriptorium_word_tokens
```

Candidate adjacency is **sentence bounded**. Two adjacent Scriptorium word tokens form a
candidate pair only when they are in the same `scriptorium-text-v1` sentence candidate
and both resolve to direct FantLab buckets. An undefined token breaks the pair; a
sentence boundary never creates a cross-sentence pair.

Sentence-bounded adjacency is an explicit inference. The public FantLab wording does not
establish punctuation crossing, unknown-token behavior or whether its internal token
stream creates pairs across sentence boundaries. Source-matched benchmarks must decide
whether this candidate survives.

The artifact emits a complete 17×17 matrix. Each cell includes both `raw_count` and
`per_1000_words`; zero-count cells are present rather than omitted.

## POS by sentence position

FantLab's current page explains a position cell as the probability that, for example,
the third word in a **randomly selected sentence** is a verb. The v1 candidate therefore
uses the number of Scriptorium sentence candidates as the denominator for every position:

```text
100 * sentences_with_bucket_at_position / all_scriptorium_sentences
```

A sentence shorter than the requested position contributes zero to every bucket
numerator at that position. A sentence whose token at that position is undefined also
contributes zero. This distinction matters: the denominator is not merely the number of
sentences long enough to reach the position.

The artifact emits positions 1..20. The 2022 observed work surface commonly renders the
first ten, while FantLab's public methodology says position statistics exist up to 20.

## Runtime input identity

`runtime_pos_candidates` must align one-for-one with the deterministic Scriptorium word
token stream. A mismatch is an error rather than a truncation or padding rule.

The artifact records:

- `runtime_profile` — caller-supplied identity for the producer/configuration;
- `runtime_analysis_sha256` — SHA-256 of the canonical JSON candidate matrix;
- `mapping_contract` — the pinned runtime-to-FantLab mapping contract.

A runtime profile name plus this digest makes the aggregation reproducible, but it does
**not** prove that the analyses came from FantLab's production morphology or even from a
native pylem build. Provenance of the provider execution belongs to the future adapter
and benchmark record.

## Schema and tests

`schemas/scriptorium-pos-metrics-v1.schema.json` freezes the artifact shape:

- exactly 17 distribution buckets;
- a complete 17×17 bigram matrix;
- exactly positions 1..20, each with all 17 buckets;
- null service-word values with an explicit `unresolved` status;
- an immutable runtime-analysis SHA-256.

`tests/test_morphology.py` covers conservative resolution, empty input, denominator
choices, sentence-boundary behavior, unresolved bigram breaks, alignment checks and the
20-position boundary.

## Primary evidence

- [`AOT_PYLEM_COMPATIBILITY.md`](AOT_PYLEM_COMPATIBILITY.md)
- [`FANTLAB_METRIC_CONTRACT.md`](FANTLAB_METRIC_CONTRACT.md)
- https://fantlab.ru/article374
- https://fantlab.ru/work127106/lp — current public wording for bigram and
  sentence-position tables

FantLab's public page wording establishes the visible meanings above, not hidden
implementation equivalence. `scriptorium-pos-v1` remains inferred until source-matched
benchmarks justify promotion.
