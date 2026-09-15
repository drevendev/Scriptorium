# Pinned AOT literature homonym-weight diagnostic

Status: **diagnostic provider evidence only**. This document does not define a
FantLab-compatible homonym-selection rule.

## Why this signal is measurable

The exact Scriptorium compatibility candidate remains `pylem==0.0.18` with pinned
`morph_dict@4c5e9b6d048d1ba74e02988593b23fb0cbc87772`.

At pinned pylem revision `68d62ce5452b6b80f2c2ef3345b4160c09e24bdf`,
`LemmaInfo` exposes `predicted`, `word_weight` and `homonym_weight` in addition to the
already-used `part_of_speech` value. The wrapper obtains those values directly from the
JSON emitted by the native holder.

The pinned `morph_dict` source gives the weights a narrower provenance than a generic
"frequency heuristic":

- `CLemmatizer::LoadDictionariesFromPath` loads `m_Statistic` from the `l` prefix and
  comments that this **implicitly loads homonym statistics for literature**;
- it then sets `m_bUseStatistic = true`;
- `AssignWeightIfNeed` copies `get_HomoWeight(paradigm, form)` into each analysis;
- `CFormInfo::GetHomonymWeight()` returns that stored analysis weight;
- `CStatistic::get_HomoWeight` performs an exact lookup in the loaded homonym-weight
  table and returns zero when no entry is present.

Pinned source references:

- `https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/__init__.py`
- `https://github.com/sokirko74/morph_dict/blob/4c5e9b6d048d1ba74e02988593b23fb0cbc87772/LemmatizerBaseLib/Lemmatizers.cpp`
- `https://github.com/sokirko74/morph_dict/blob/4c5e9b6d048d1ba74e02988593b23fb0cbc87772/LemmatizerBaseLib/Paradigm.cpp`
- `https://github.com/sokirko74/morph_dict/blob/4c5e9b6d048d1ba74e02988593b23fb0cbc87772/LemmatizerBaseLib/Statistic.cpp`

This establishes that the pinned provider has a built-in literature-oriented homonym
weight signal. It does **not** establish what corpus produced the statistic, whether its
magnitude is a calibrated probability, whether larger values should always win, or
whether FantLab used this statistic or the same dictionary bytes.

## Scriptorium diagnostic contract

`scriptorium-pylem-candidate-metadata-v1` augments each ephemeral sidecar row with
source-free metadata aligned one-for-one with the existing ordered runtime POS
candidates:

- runtime POS;
- `predicted` boolean;
- integer-or-null `homonym_weight`;
- integer-or-null `word_weight`.

No lemma, token text, morphology-feature set or predictor source is retained in the
uploaded diagnostic artifact. The modern consumer first validates the existing canonical
text/token/provider transport, then validates candidate-metadata alignment and hashes the
canonical metadata matrix.

`scriptorium-pylem-homonym-weight-diagnostic-v1` measures only rows already classified
as `direct_cross_bucket_ambiguity`. For each row it computes the maximum homonym weight
within each directly mapped FantLab-shaped bucket, then reports whether exactly one
bucket has the largest value or the maximum is tied. It also records missing-weight,
all-zero and prediction-presence counts plus source-free bucket-signature aggregates.

The diagnostic deliberately does **not** feed a selected bucket back into
`scriptorium-pos-v1`.

## Evidence boundary

Even if a unique maximum covers most direct ambiguities on a frozen work, the result is
only evidence that the pinned AOT provider supplies a potentially informative signal.
Promotion to a compatibility rule still requires evidence for FantLab's actual
homonym-selection behavior and dictionary identity, ideally on source-matched benchmark
texts.

The following remain fail-closed:

- FantLab homonym-selection policy;
- FantLab dictionary/version identity;
- runtime `N` noun/cardinal recovery;
- folding of `POSL`, `COLLOC`, `ADJ_SHORT`, `PARTICIPLE_SHORT` and `INFINITIVE`;
- service-word aggregation;
- M2 parity admission while source identity is unknown.
