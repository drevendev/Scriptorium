# AOT/pylem compatibility candidate

Contract: `aot-pylem-0.0.18-to-fantlab-2022-v1`

Status: **inferred compatibility candidate**, not reproduced behavior.

This note fixes the first morphology stack and the POS mapping boundary needed by
`SCRIP-MORPH-002`. It deliberately separates what is directly documented by AOT/pylem
from what remains unknown about FantLab's production analyzer.

## Pinned stack

The first compatibility candidate is `pylem==0.0.18`.

Pinned identifiers:

- PyPI release: `0.0.18`, published 2022-01-16.
- PyPI sdist SHA-256:
  `66c0d13414006a803f200979540fcee9653738701c14496a418db67542b26515`.
- pylem repository revision:
  `68d62ce5452b6b80f2c2ef3345b4160c09e24bdf`; its `setup.py` declares
  `version="0.0.18"`.
- `morph_dict` submodule at that revision:
  `4c5e9b6d048d1ba74e02988593b23fb0cbc87772`.
- `pybind11` submodule at that revision:
  `cd176ceeff94ec184abde945ef0867ebe9fb3664`.
- AOT documentation snapshot used for the Russian POS inventory:
  `sokirko74/aot@ee2c370c65b01fd78b3f366ed23aa1c2ed2d7c93`.

PyPI does not encode a Git commit for the uploaded sdist, so the repository revision is
recorded as the revision whose `setup.py` declares 0.0.18, not as cryptographic proof
that the sdist bytes were built from that Git commit. The sdist hash is the immutable
package identity.

The release source requires Python `>=3.6` in package metadata, CMake `>=3.16`, and
C++17 (`target_compile_features(... cxx_std_17)`). A source checkout needs the pinned
submodules. These are build-contract facts, not a claim that pylem supports every modern
Python/compiler combination.

## What pylem exposes

`MorphanHolder.lemmatize()` yields zero or more `LemmaInfo` analyses. Each carries
`part_of_speech`, a set of morphology features, prediction metadata and optional weights.
The wrapper does not establish FantLab's homonym/disambiguation policy.

Therefore Scriptorium must preserve all analyses at the morphology-adapter boundary until
a benchmark-backed selection policy exists. It must not choose the first analysis, the
highest weight, or any other heuristic and call that FantLab-compatible behavior.

## Direct POS mapping

AOT's documented Russian POS inventory contains 18 labels. Seventeen have direct
name/meaning counterparts on the observed 2022 FantLab work-analysis surface:

| AOT | Meaning | `fantlab-2022-v1` bucket |
| --- | --- | --- |
| `С` | noun | `noun` |
| `П` | adjective | `adjective` |
| `Г` | finite/personal verb | `verb` |
| `МС` | pronoun-noun | `pronoun_noun` |
| `МС-П` | pronominal adjective | `pronoun_adjective` |
| `МС-ПРЕДК` | pronominal predicative | `pronoun_predicative` |
| `ЧИСЛ` | cardinal numeral | `cardinal` |
| `ЧИСЛ-П` | ordinal numeral | `ordinal` |
| `Н` | adverb | `adverb` |
| `ПРЕДК` | predicative | `predicative` |
| `ПРЕДЛ` | preposition | `preposition` |
| `СОЮЗ` | conjunction | `conjunction` |
| `МЕЖД` | interjection | `interjection` |
| `ВВОДН` | introductory word | `introductory_word` |
| `ЧАСТ` | particle | `particle` |
| `ПРИЧАСТИЕ` | participle | `participle` |
| `ДЕЕПРИЧАСТИЕ` | gerund | `gerund` |

The machine-readable source of truth is
`compatibility/aot-pylem-0.0.18-to-fantlab-2022-v1.json`.

"Direct" means that the public labels correspond semantically. It does **not** mean that
pylem 0.0.18 has been demonstrated to reproduce FantLab's token-level choices.

## Unresolved mapping before direct fallback

The adapter must test unresolved overrides before applying the direct POS table.

`ИНФИНИТИВ` is a standalone AOT POS, while the observed 2022 FantLab page has no
standalone infinitive bucket. FantLab's broader methodology names infinitives, but public
evidence does not establish whether the 2022 surface folds them into `verb`, discards
them from the displayed table, or handles them another way. It therefore remains
unresolved.

AOT documents `кр` as the short-form grammeme for adjectives or participles. FantLab's
methodology names short adjectives and short participles separately, but those categories
are not separately displayed on the observed 2022 work page. `П + кр` and
`ПРИЧАСТИЕ + кр` therefore remain unresolved instead of silently falling through to the
ordinary adjective/participle buckets.

FantLab's methodology also names postpositions and phrasal verbs. They are not standalone
POS labels in AOT's documented inventory and are not standalone buckets on the observed
2022 page. They remain derived-category research questions.

## Dictionary and analyzer drift

The pinned pylem package is useful because it wraps the historical AOT C++ morphology
family and ships a pinned morphology dictionary, but it is not evidence of dictionary
identity with FantLab's 2022 deployment.

The following remain unproven:

- whether FantLab used the same AOT source revision or dictionary bytes;
- whether FantLab applied later dictionary corrections;
- how it resolves multiple AOT analyses/homonyms;
- how predicted/out-of-dictionary analyses participate in POS statistics;
- how the unresolved categories above are folded into the 2022 display buckets.

These questions are benchmark inputs for `SCRIP-MORPH-002`, not implementation defaults.

## Verification performed in this unit

Source-level verification established:

- PyPI still lists 0.0.18 as the latest pylem release and publishes the sdist hash above;
- the pinned pylem commit declares version 0.0.18;
- its submodule SHAs are recoverable from GitHub at that exact revision;
- its CMake files require CMake 3.16 and C++17;
- the wrapper exposes `LemmaInfo.part_of_speech` and can yield multiple analyses;
- the pinned AOT documentation lists the 18 Russian POS labels used by this contract;
- the mapping JSON parses and contains exactly 17 `direct` POS rows.

A native build was **not run** in this automation environment. `pip download
--no-deps pylem==0.0.18` could not resolve the external package host because outbound
network access from the execution container is unavailable. That is an environment
limitation, not a pylem build failure. The package identity and source metadata were
verified through the public package/repository sources instead.

## Primary sources

- https://pypi.org/project/pylem/
- https://github.com/sokirko74/pylem/tree/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf
- https://github.com/sokirko74/aot/blob/ee2c370c65b01fd78b3f366ed23aa1c2ed2d7c93/Source/www/wwwroot/concor.html
- https://fantlab.ru/article374
- https://fantlab.ru/work12625/lp
