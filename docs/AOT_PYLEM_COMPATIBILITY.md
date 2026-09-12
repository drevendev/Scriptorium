# AOT/pylem compatibility candidate

Contract: `aot-pylem-0.0.18-to-fantlab-2022-v1`

Status: **inferred compatibility candidate**, not reproduced behavior.

This note fixes the first morphology stack and the POS mapping boundary needed by
`SCRIP-MORPH-002`. It deliberately separates the historical/documentation-facing AOT
vocabulary from the strings that pinned pylem actually returns at runtime.

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
- AOT documentation snapshot used as historical terminology reference:
  `sokirko74/aot@ee2c370c65b01fd78b3f366ed23aa1c2ed2d7c93`.

PyPI does not encode a Git commit for the uploaded sdist, so the repository revision is
recorded as the revision whose `setup.py` declares 0.0.18, not as cryptographic proof
that the sdist bytes were built from that Git commit. The sdist hash is the immutable
package identity.

The release source requires Python `>=3.6` in package metadata, CMake `>=3.16`, and
C++17. A source checkout needs the pinned submodules. These are build-contract facts,
not a claim that pylem supports every modern Python/compiler combination.

## Actual pylem runtime representation

The Python binding calls `SetUseNationalConstants(false)` immediately after loading the
morphology holder. Therefore the public Python result uses AOT's **Latin runtime
constants**, not the Cyrillic documentation labels.

`MorphanHolder.lemmatize_json()` produces `morphInfo`; `pylem/__init__.py` takes the
leading token of that string and exposes it as `LemmaInfo.part_of_speech`. That field is
the adapter input described by this contract.

The pinned `morph_dict` source has 22 Russian POS slots but only 21 distinct Latin POS
strings because two source categories collapse to `N`:

| Slot | AOT Cyrillic | pylem runtime | FantLab 2022 target | Status |
| ---: | --- | --- | --- | --- |
| 0 | `С` | `N` | `noun` | runtime collision |
| 1 | `П` | `A` | `adjective` | direct |
| 2 | `Г` | `V` | `verb` | direct |
| 3 | `МС` | `P` | `pronoun_noun` | direct |
| 4 | `МС-П` | `PA` | `pronoun_adjective` | direct |
| 5 | `МС-ПРЕДК` | `P-PRED` | `pronoun_predicative` | direct |
| 6 | `ЧИСЛ` | `N` | `cardinal` | runtime collision |
| 7 | `ЧИСЛ-П` | `NA` | `ordinal` | direct |
| 8 | `Н` | `ADV` | `adverb` | direct |
| 9 | `ПРЕДК` | `PRED` | `predicative` | direct |
| 10 | `ПРЕДЛ` | `PREP` | `preposition` | direct |
| 11 | `ПОСЛ` | `POSL` | — | unresolved |
| 12 | `СОЮЗ` | `CONJ` | `conjunction` | direct |
| 13 | `МЕЖД` | `INT` | `interjection` | direct |
| 14 | `ВВОДН` | `INP` | `introductory_word` | direct |
| 15 | `ФРАЗ` | `COLLOC` | — | unresolved |
| 16 | `ЧАСТ` | `PARTICLE` | `particle` | direct |
| 17 | `КР_ПРИЛ` | `ADJ_SHORT` | — | unresolved |
| 18 | `ПРИЧАСТИЕ` | `PARTICIPLE` | `participle` | direct |
| 19 | `ДЕЕПРИЧАСТИЕ` | `ADV_PARTICIPLE` | `gerund` | direct |
| 20 | `КР_ПРИЧАСТИЕ` | `PARTICIPLE_SHORT` | — | unresolved |
| 21 | `ИНФИНИТИВ` | `INFINITIVE` | — | unresolved |

The machine-readable source of truth is
`compatibility/aot-pylem-0.0.18-to-fantlab-2022-v1.json`.

## Direct runtime mapping

Only 15 runtime strings are directly usable with `LemmaInfo.part_of_speech`:

```text
A -> adjective
V -> verb
P -> pronoun_noun
PA -> pronoun_adjective
P-PRED -> pronoun_predicative
NA -> ordinal
ADV -> adverb
PRED -> predicative
PREP -> preposition
CONJ -> conjunction
INT -> interjection
INP -> introductory_word
PARTICLE -> particle
PARTICIPLE -> participle
ADV_PARTICIPLE -> gerund
```

"Direct" means only that the runtime code has an unambiguous semantic counterpart on the
observed 2022 FantLab surface. It does **not** mean pylem 0.0.18 has been demonstrated to
reproduce FantLab's token-level analysis.

## The `N` noun/cardinal collision

Pinned AOT maps both Cyrillic `С` (noun) and `ЧИСЛ` (cardinal numeral) to Latin `N`.
Because pylem turns the rendered `morphInfo` token into `LemmaInfo.part_of_speech`, the
public Python object has already lost the original source-POS distinction at that point.

Scriptorium must therefore treat runtime `N` as unresolved between `noun` and `cardinal`.
It must **not** infer the bucket from list order, lexical guesses, or morphology-feature
patterns merely because such a heuristic looks plausible.

The underlying AOT code still has distinct internal POS slots/ancodes before string
rendering. A future implementation may expose that discriminator through a narrow binding
extension, but it becomes compatibility evidence only after its behavior is pinned and
validated against source-matched FantLab benchmarks. The current pylem Python API does not
provide that discriminator.

## Extra runtime categories

Five runtime POS values are real standalone categories in the pinned backend but have no
standalone bucket on the observed 2022 FantLab work surface:

- `POSL` / `ПОСЛ` — postposition;
- `COLLOC` / `ФРАЗ` — phrasal/collocation category;
- `ADJ_SHORT` / `КР_ПРИЛ` — short adjective;
- `PARTICIPLE_SHORT` / `КР_ПРИЧАСТИЕ` — short participle;
- `INFINITIVE` / `ИНФИНИТИВ` — infinitive.

FantLab's broader methodology names these kinds of categories, but public evidence does
not establish how the 2022 work page folds them into its 17 displayed buckets. They stay
`unresolved`; the repaired contract no longer models short forms as grammeme overrides of
ordinary adjective/participle runtime codes because pinned pylem exposes them as separate
POS values.

## Ambiguity and dictionary drift

`MorphanHolder.lemmatize()` yields zero or more `LemmaInfo` analyses. The wrapper exposes
prediction metadata and optional weights, but no public evidence establishes FantLab's
homonym/disambiguation policy. Scriptorium must preserve all analyses at the morphology
adapter boundary until benchmark evidence supports a deterministic selection rule.

The following also remain unproven:

- whether FantLab used the same AOT source revision or dictionary bytes;
- whether FantLab applied later dictionary corrections;
- how predicted/out-of-dictionary analyses participate in POS statistics;
- how the five extra runtime categories are folded into the 2022 display buckets;
- how FantLab distinguishes the noun/cardinal source categories represented by pylem as
  the same runtime `N` string.

These are benchmark inputs for `SCRIP-MORPH-002`, not implementation defaults.

## Verification performed in this unit

Source-level verification established:

- the pinned pylem binding calls `SetUseNationalConstants(false)`;
- `pylem/__init__.py` parses the leading `morphInfo` token into
  `LemmaInfo.part_of_speech`;
- pinned `morph_dict` defines 22 source POS slots and 21 unique Latin runtime strings;
- the only duplicate runtime string is `N`, shared by noun and cardinal numeral;
- 15 runtime strings map directly to one observed FantLab bucket each;
- five additional runtime strings remain explicitly unresolved;
- the repaired mapping JSON parses and its counts agree with the pinned source inventory.

A native build remains **not run**. The original spike could not resolve the external
package host from its execution container. That is an environment limitation, not a
pylem build failure.

## Primary sources

- https://pypi.org/project/pylem/
- https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/binding/main.cpp
- https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/__init__.py
- https://github.com/sokirko74/morph_dict/blob/4c5e9b6d048d1ba74e02988593b23fb0cbc87772/AgramtabLib/RusGramTab.cpp
- https://github.com/sokirko74/aot/blob/ee2c370c65b01fd78b3f366ed23aa1c2ed2d7c93/Source/www/wwwroot/concor.html
- https://fantlab.ru/article374
- https://fantlab.ru/work12625/lp
