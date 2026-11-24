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

## Hosted native execution evidence

Source-level verification established:

- the pinned pylem binding calls `SetUseNationalConstants(false)`;
- `pylem/__init__.py` parses the leading `morphInfo` token into
  `LemmaInfo.part_of_speech`;
- pinned `morph_dict` defines 22 source POS slots and 21 unique Latin runtime strings;
- the only duplicate runtime string is `N`, shared by noun and cardinal numeral;
- 15 runtime strings map directly to one observed FantLab bucket each;
- five additional runtime strings remain explicitly unresolved;
- the repaired mapping JSON parses and its counts agree with the pinned source inventory.

The provider execution path is now independently demonstrated on PR #55 exact head
`3c5c5d49294816ef64e81b68311f11f8dfe6c8bf` by GitHub Actions run `34888181464`:

- the modern contract job ran on `ubuntu-24.04` with Python 3.13 and completed the full
  standard-library test suite successfully;
- the isolated native-provider job ran on `ubuntu-22.04` with Python 3.9;
- the native job installed the exact hash-pinned `pylem==0.0.18` source distribution
  with `--require-hashes --no-deps` and `CMAKE_POLICY_VERSION_MINIMUM=3.5`, without
  patching the pylem or vendored `morph_dict` source bytes;
- the install step, isolated native probe and source-free receipt upload all completed
  successfully;
- runtime artifact `10365997598` is 845 bytes with GitHub-recorded archive digest
  `sha256:08f75c60d8b3f611118541ddb74bba871a3f7b13eeafb162fbd737f9174d48c8`;
- before upload the workflow asserts provider distribution `pylem`, version `0.0.18`,
  runtime profile `pylem-0.0.18-python39-sidecar-v1`, a three-token fixture with
  `source_text_included=false`, `fantlab_dictionary_equivalence=unknown`, and
  `m2_parity_admissible=false`.

An earlier Ubuntu 24.04 native attempt reached C++ compilation and failed inside the
pinned legacy `morph_dict` source under the newer hosted toolchain. The reviewed remedy
is isolation of this legacy compatibility backend on the Ubuntu 22.04/Python 3.9 sidecar
lane, not alteration of immutable upstream source. This verifies provider executability;
it does **not** establish FantLab dictionary identity, token-level parity, homonym
selection parity, noun/cardinal recovery, or M2 benchmark admissibility.

## Independent inflected-form native control (PR candidate, not yet measured)

A separate source-free probe, `tools/pylem_inflection_probe.py`, uses nine
**new curated lexical forms**: three oblique-case noun examples, three
inflected-cardinal examples and three unrelated conjunction controls. It runs
under the existing Python 3.9 / hash-pinned `pylem==0.0.18` native lane.
The versioned receipt stores SHA-256 of each lexical fixture (not its original
spelling), *all* observed runtime POS candidates, disjoint N-only/mixed-N
counts, denominators and a digest of the native observations. A conditional
cross-role N observation requires an N-only candidate in both annotated roles
and at least two separately analyzed, N-free conjunction controls. Missing
analyses and all-N backends do not qualify as clean negative controls.

This test is independent of the earlier citation-form/ADJ/ADV/VERB sample;
neither sample can recover the original AOT source POS from a shared runtime
`N` string. The new native outcomes remain **NOT_RUN** until the exact-head
hosted job completes and its artifact is inspected. It is a lexical-control
experiment, **not** a third full-work measurement, a FantLab homonym-policy
experiment or M2 parity evidence. No production POS mapping changes. After
execution, preserve the actual output, toolchain and run link before drawing
conclusions rather than assuming all nine tokens behave as annotated.

## Conditional noun/cardinal N-only impact

The pinned native pylem 0.0.18 Anna replay also emits a source-free
N-only sensitivity artifact. Only token rows whose complete runtime POS
candidate set is N are conditionally considered noun or cardinal. Mixed-N
and all other unknown rows stay unresolved. It quantifies POS bucket
counts/rates, affected bigrams per 1,000 words and sentence-position
percentages as independent per-cell conservative envelopes. Different
maxima cannot necessarily coexist in one assignment. The v2 artifact tightens
bigram maxima using per-sentence dynamic programming: each N-only token must
have one consistent noun/cardinal assignment across its adjacent bigrams.
For example, three consecutive N-only tokens can contribute at most one
noun→cardinal transition, not the two suggested by independent edge sums.
The former loose bound is retained as
`independent_edge_upper_bound_raw_count`; `conditional_max_raw_count` is
now the **exact individual-cell** maximum under these hypothetical choices.
No joint attainability across different cells is asserted.

The v3 artifact also tightens **per-cell minima** using the same
consistent-token DP: a conditional fixed noun → N-only → fixed cardinal
sequence forces one noun→cardinal edge, whereas counting fixed edges
alone incorrectly suggests zero. `conditional_min_raw_count` now means
an attainable minimum within the stated N-only hypothesis;
`fixed_edge_lower_bound_raw_count` preserves the historical looser bound.
This synthetic fixed-category example does not establish that native pylem
reveals noun versus cardinal, nor does it prove a FantLab label.

These are NOT true POS labels, recovered AOT enums, FantLab homonym
decisions, or M2 parity. Provider sdist, runtime candidate SHA, frozen
normalized source hash and commit are recorded; text and token rows are
never uploaded. The production POS mapping and M2 0/5 are unchanged.

The frozen-work N-only diagnostic CLI now uses the same atomic **create-only**
report writer as local analysis: existing reports, sidecar request/response inputs,
and symlink targets cannot be overwritten by a repeat run. On a collision the
command exits with a path-free error and requires a new destination. This changes
receipt safety only, not native measurements, uncertainty bounds or POS mapping.

## Source-free N sensitivity in readable FantLab-shaped units

`scriptorium n-evidence --root . --format html --output native-n.html` also renders the exact retained native witness as a local, self-contained, no-JavaScript HTML report, with accessible tables and print styles. It uses the same source-free observed counts, per-cell conditional bounds and explicitly labelled denominators as Markdown/CSV. The HTML renderer does **not** execute pylem or claim a new measurement, source-matched FantLab parity or recovered noun/cardinal tags. Its create-only output avoids overwriting an earlier report.


The checked-in `scriptorium n-evidence --root . --format json` command now
re-expresses the **already measured** N-only count envelopes with explicit
denominators: noun/cardinal bucket percentage of *conditionally defined*
tokens, POS-pair counts **per 1,000 total word tokens**, and sentence-position
percentage of **all sentences**. Markdown and CSV expose both original integer
bounds and these calculated rates; CSV also retains the looser independent-edge
upper bound so it cannot be confused with the exact per-cell conditional maximum.
The JSON CLI schema is `scriptorium-native-n-cli-evidence-v4` and the
derivation is `scriptorium-native-n-conditional-units-v2`. The same pinned
fixture now reports N-only shares of each *annotated* three-token lexical
control group (100% nouns, 66.666667% cardinals, 0% unrelated controls) in
JSON, CSV and Markdown. These tiny, curated groups are not a classifier,
representative corpus sample, or evidence of recovered AOT enum identity. Six-digit CSV/Markdown
decimal display is Scriptorium presentation precision, **not** FantLab rounding.
The report and public N page also expose the previously omitted N-mixed share:
19,670 / 269,358 = 7.30% of word tokens. Together with the disjoint 55,081
N-only tokens, 74,751 / 269,358 = 27.75% have at least one N candidate.
This is a token-coverage diagnostic, **not** a noun/cardinal rate or recovered
POS classification. The N-mixed rows stay excluded from conditional bounds,
and the endpoints of different cells are not jointly attainable. All records remain source-free; production POS mapping,
source-matched parity and M2 (0/5) are unchanged.

## Native lexical contrast controls (SCRIP-MORPH-009)

The pinned Ubuntu 22.04 / Python 3.9 `pylem==0.0.18` smoke now
also measures a **small curated, source-free control fixture** with three
noun lexemes, three cardinal lexemes and three unrelated POS controls.
Each per-token row records only the SHA-256 of the fixture token, all
observed native runtime tags, the candidate count, and whether `N`
is present or is the *only* reported tag. Native CI records per-role
counts and whether N-only labels occur in both curated noun/cardinal
groups. The original three-token smoke contract is unchanged.

The v2 native control receipt additionally reports whether **every unrelated
negative-control token received at least one native analysis with no `N`
candidate**. The cross-role N-only observation is control-qualified only when
these negatives pass. A provider returning `N` for everything, or returning
no analyses for a negative control, is inconclusive rather than positive
collision evidence. The raw observation remains separately available. This
is not an accuracy score or a recovered noun/cardinal mapping.

This is a **measured capability/ambiguity diagnostic**, not a recovered
AOT enum or a word-level homonym choice. The lexical role labels are
curated *test expectations*, not native ground truth; native analyses
may return multiple homonyms or none. Even cross-role N-only output
does not identify FantLab's dictionary or selection policy. The
source-free receipt is an ephemeral CI artifact, not a literary corpus
entry or an M2 parity benchmark. Frozen full-work N-only bounds
remain a separate independently versioned diagnostic.

## Supplemental negative-control survey (native measured; #282)

The pinned v2 native run [44050332584](https://github.com/drevendev/Scriptorium/actions/runs/44050332584)
observed `N` in the original adjective control `красный` (`A, N`),
so its **control-qualified collision verdict remains false**, despite raw
N-only noun/cardinal observations. This does not imply the backend is defective:
a curated adjective can have additional native analyses.

The separate `scriptorium-aot-n-control-survey-v1` experiment asks the same
native `pylem==0.0.18` executable to test three candidate lexical controls
each for adjectives (`A`), adverbs (`ADV`) and verbs (`V`). An individual
candidate counts as usable only when it receives a nonempty analysis with its
expected native tag and **no** `N` candidate. Missing analyses, an `N`
homonym, and absent expected tags are separately recorded. The source-free
receipt contains token hashes, actual runtime tags, group counts and the
all-roles-covered diagnostic; **no words from books**. This is an exploratory
selection experiment, not a change to the original three v2 controls, its
strict negative gate, production mapping, frozen Anna impact bounds, or M2.
Survey success alone cannot establish the source AOT POS enum or FantLab
homonym policy. The [2026-11-17 pinned native run #44068624527](https://github.com/drevendev/Scriptorium/actions/runs/44068624527)
**confirmed 3/3 usable** in each group (nine total), with the expected
runtime POS and zero N candidates. One adverb had both `ADV` and
`ADJ_SHORT` without N; usable does not mean unambiguous.
The survey input-manifest SHA-256 is
`da56ada4e9861baf81921c61ddc7b082fae26e727c1a647e39beffee9dbf484b`.
The original unrelated v2 group still has 0/3 **N-only** but 1/3
**N-present** (`A, N` for `красный`); its strict
`controlled_cross_role_n_collision_observed` remains **false/INCONCLUSIVE**.
This separate survey cannot establish AOT source POS enums, production
noun/cardinal assignments or FantLab parity.

### Independent v3 contrast (verified in #560)

The distinct `scriptorium-aot-n-independent-controls-v3` diagnostic uses the
**same** pinned native sample and its independently observed negative-control
survey. It requires N-only evidence from both annotated noun and cardinal
lexical groups **and at least two N-free, expected-tag-positive controls out
of three** for each unrelated role (adjectives, adverbs and verbs). Fewer
controls, missing positive evidence, an all-N backend or inconsistent survey
rows fail closed. It records exact per-group coverage, the historical v2
verdict and a separately labelled v3 controlled observation. The v2 result
remains false because `красный` returned `A, N`; v3 does **not** rewrite
those original controls or cherry-pick a v2 result.

The [successful pinned native v3 run #44093423449](https://github.com/drevendev/Scriptorium/actions/runs/44093423449) separately qualifies the v3 observation with 3/3 usable controls in each unrelated role. This only establishes that this pinned runtime returns
indistinguishable `N` strings for selected lexemes annotated as different
lexical roles while unrelated controls show distinct native tags. It still
**cannot reconstruct AOT source POS enums, noun/cardinal assignments,
FantLab's dictionary or its homonym decisions**. Frozen full-book conditional
bounds remain separate, and production mapping, M1/M2 acceptance and corpus
status remain unchanged. Native CI for #560 passed on 2026-11-17; this verifies the bounded native observation, not source AOT POS enums or FantLab parity.


### Independent full-work AOT control: Resurrection (PR candidate, 2026-11-18)

An independent frozen public-domain Russian transcription of Tolstoy's
*Resurrection* (129 pinned Wikisource revisions, 890,835 characters including
spaces, raw/normalized SHA-256
`2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0`)
is an additional pinned `pylem==0.0.18` N-only diagnostic target. The
source-specific extractor handles two verified chapter shapes; applying the
Anna packed-manifest renderer would violate input identity. The CI job checks
all pinned revisions and full body hash before tokenization, runs the Python
3.9 AOT sidecar, and reports native N-only/N-mixed and per-cell conditional
POS, bigram and sentence-position bounds. Ephemeral requests/responses are
removed; only source-free summaries are uploaded.

This is an independent source-bound diagnostic, not recovered noun/cardinal
labels or a FantLab edition match. Native results are NOT_RUN until the
exact-head job succeeds. Anna's retained evidence remains unchanged; M2 0/5.

## Primary sources

- https://pypi.org/project/pylem/
- https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/binding/main.cpp
- https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/__init__.py
- https://github.com/sokirko74/morph_dict/blob/4c5e9b6d048d1ba74e02988593b23fb0cbc87772/AgramtabLib/RusGramTab.cpp
- https://github.com/sokirko74/aot/blob/ee2c370c65b01fd78b3f366ed23aa1c2ed2d7c93/Source/www/wwwroot/concor.html
- https://fantlab.ru/article374
- https://fantlab.ru/work12625/lp

### Third full-work native N contrast: Grin (PR candidate, 2026-11-22)

The existing 36-page, source-verified public-domain *Running on Waves* (1965
edition) literary-body witness has **363,819 characters including spaces** and
normalized SHA-256
`41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`.
It is independent of the two already retained Tolstoy pylem full-work runs.
The new `scriptorium.running_waves_native_n` preparation path checks every
pinned Wikisource page, exact composite identity and normalized request before
allowing the existing hash-pinned Python 3.9/pylem 0.0.18 sidecar to run.

The `third-running-waves-native-n` GitHub Actions job writes an ephemeral
source-bearing request/response, validates per-token native identities through
`scriptorium.n_collision_diagnostic`, deletes both source-bearing transports
and uploads **only** a source-free N-only/mixed-N POS/bigram/position envelope.
An artifact and its measured numbers are NOT_RUN until that exact-head workflow
has completed and the uploaded bytes have been independently inspected. This
does **not** identify N as noun vs cardinal, prove FantLab's input/dictionary
identity or advance the M2 0/5 parity gate. Scientific acceptance and the
eventual public Reader comparison are separate from preparing this run.

### Fourth full-work N witness: Grin's *Road to Nowhere* (PR candidate, 2026-11-22)

This **independent, not-yet-executed** native experiment reuses the existing
public-domain single-page alternate transcription, Wikisource oldid 5585836,
442,656 literary characters including spaces, normalized SHA-256
`e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`.
It is the az.lib-derived alternate edition, not the incomplete primary
Pravda-1965 route or FantLab's disclosed analyzer input.

`scriptorium.road_nowhere_native_n` first enforces the frozen legal and
single-revision identities, replays the full literary body, and binds a
temporary native request to its exact normalized digest. The existing
hash-pinned Python 3.9 / pylem 0.0.18 sidecar then produces a response
consumed through the validated transport and the established N-only conditional
POS/bigram/sentence-position calculation. CI uploads only a source-free JSON
receipt; the source-bearing request/response are removed on all exits.

The fourth-work measurement is **NOT_RUN** until exact-head hosted CI completes
and an independently read-back artifact confirms actual counts. The native N
collision, unknown FantLab homonym policy and M2 **0/5** gate are unchanged.
A completed fourth receipt can support comparisons *within* one author as well
as across authors, but not a claim that noun and cardinal were disambiguated.

## Dictionary-attestation test of N candidates (pending native CI)

Issue #282 adds an **independent source-free diagnostic**, not a morphology remap.
The Python 3.9 pinned-native workflow runs
`python tools/pylem_n_attestation_probe.py --receipt build/morph/pylem-n-attestation.json`
on nine newly selected genitive examples: three annotated nouns, three annotated
cardinals and three unrelated preposition controls. It records the runtime POS
candidates alongside `LemmaInfo.predicted` booleans, and reports N-only,
N-mixed, **dictionary-attested N** (at least one N candidate was not predicted),
and **predicted-only N** counts. The prediction flag comes from pylem's
`found` field; it does **not** restore AOT's original noun/cardinal enum.

The receipt contains only fixture hashes, candidate POS tags, prediction booleans,
aggregates, native package/version hash and observation SHA-256; no fixture words,
lemmas, manuscript text or token sequences leave the workflow. The three role
labels describe curated examples only, not ground-truth classifier performance
or a representative sample. A qualified collision requires dictionary-attested
N-only candidates in *both* annotated noun and cardinal groups and at least two
non-N, nonempty negative controls. That observation is intentionally **not**
treated as a discriminator: the native source POS, FantLab dictionary identity,
homonym selection and M2 parity remain unresolved (0/5). No claimed counts
before exact-head native CI artifact inspection.



## Native Python N source-POS field-surface feasibility (PR candidate)

The next #282 experiment inspects the **public instance field names** exposed by
the already pinned pylem 0.0.18 `LemmaInfo` objects, using the nine previously
curated noun/cardinal/preposition genitive controls. It does **not** reclassify
tokens or repeat the earlier dictionary-attestation inference. The
`tools/pylem_n_source_pos_probe.py` receipt records only allowlisted attribute
names, per-token SHA-256, N candidate counts, coverage of likely original-POS
fields, and a source-free observation hash. It never writes attribute values:
lemmas, grammemes, raw `morphInfo`, fixture spellings and manuscripts stay out
of CI artifacts.

Three disjoint outcomes are defined: no N candidates inspected (no inference);
N candidates without an explicit original-POS field in the inspected Python
instances (no observed discriminator); or a *possible* source-POS field name
that requires separate original-enum semantic validation. Even an attribute
named `source_pos_slot` is **not** accepted as proof without demonstrating its
AOT meaning. This limited field-surface probe cannot establish absence from
the C++ source, a patched binding, or future providers. It cannot validate
FantLab's homonym policy or input editions. Production POS mapping stays
unchanged, the noun/cardinal collision remains unresolved, M2 stays 0/5.

The Python 3.9 native CI receipt and full Python suite are **NOT_RUN** until
the exact PR HEAD finishes. Only after independent artifact readback may the
observed field names and feasibility outcome be reported.


## Native raw JSON boundary (PR candidate, 2026-11-24)

The [independent acceptance of #621](https://github.com/drevendev/Scriptorium/pull/621#issuecomment-7095980311)
observed 10 native N analyses across nine curated forms; none exposed an
explicit source-POS field from its Python instance allowlist. The exact native
receipt was inspected; this is not an absence claim about the underlying JSON.

The pinned upstream [binding](https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/binding/main.cpp)
(Git blob 0ad5756f7c5d8e062a618d476a6328d6a8b2154a) calls the holder's JSON
renderer after choosing non-national constants. The pinned
[Python wrapper](https://github.com/sokirko74/pylem/blob/68d62ce5452b6b80f2c2ef3345b4160c09e24bdf/pylem/__init__.py)
(Git blob e6e25788a2a0569329be7aaf5c187fe15d08091f) parses a subset of that
JSON and takes the POS prefix of morphInfo. These source observations motivate
measuring the **raw public JSON boundary**, not another Python instance audit.
The Git revision is not cryptographic proof of PyPI sdist origin.

The new probe calls lemmatize_json(word, False) and lemmatize(word) for the
same nine pinned controls, fails closed if candidate POS sequences disagree,
and records only allowlisted key names of N rows, counts of unrecognized keys
(not their names or values), fixture hashes and a digest. The native CI step
also checks per-token counts against the previous Python probe from the same
run. Unknown key counts explicitly require source review; an explicit
source-like key requires independent enum validation, never automatic
classification. Zero N rows cannot establish absence.

No raw JSON, values, lexical forms, paradigms or book text enter the artifact.
Native execution and the complete exact-head suite remain NOT_RUN until
hosted CI and independent receipt readback. The package pin, production mapping,
noun/cardinal uncertainty, FantLab input identity and M2 0/5 remain unchanged.
