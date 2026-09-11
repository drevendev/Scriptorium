# Initial architecture

Status: bootstrap decision; implementation may refine interfaces without weakening the
manifest gates.

## Stack

- Python 3.12+ for the analyzer, CLI, benchmark harness and static artifact generation.
- `pylem`/AOT as the first FantLab-compatible morphology experiment, isolated behind a
  provider interface.
- JSON as the canonical derived-analysis and benchmark interchange format.
- `pytest` for unit/golden/benchmark contract tests.
- A static GitHub Pages frontend built only from derived JSON/artifacts. The first site
  implementation should prefer minimal HTML/CSS/TypeScript or vanilla JavaScript over
  introducing a server/database.

The analysis core must not depend on the Pages implementation.

## Pipeline

```text
input bytes
  -> provenance + raw digest
  -> decode/normalize (versioned profile)
  -> structural segmentation
       paragraphs / dialogue / sentences / tokens
  -> morphology provider
  -> metric extractors
  -> AnalysisArtifact JSON
  -> benchmark / author voice / tag profiles
  -> static Pages dataset and UI
```

Each stage receives explicit version/configuration data. No stage should infer a corpus
license or silently fetch a remote book.

## Input model

The library/CLI accepts local text first. Remote corpus acquisition is a separate
curation concern so a parser bug cannot accidentally become a scraper and a site-access
change cannot affect local analysis.

Every analyzed text identity includes at minimum:

```text
work_id
language
original_author
original_title
translation_of (nullable)
translator (nullable)
edition/source label
source URL/reference
legal basis
raw sha256
raw characters including spaces
normalization profile + version
normalized sha256
```

Two translations must have different `work_id` and hashes even when they refer to the
same source work.

## Compatibility profiles

`fantlab-2022` will be the first compatibility profile. It owns choices that may differ
from modern NLP defaults, including punctuation normalization, sentence boundaries,
dialogue classification, token definitions, dictionary-vs-nondictionary decisions and
POS bucket mapping.

Generic Scriptorium extensions live outside this profile. A later improved NLP backend
may coexist with FantLab compatibility rather than replacing it.

## Morphology interface

A provider returns one normalized record per token while preserving raw provider data:

```text
surface
lemma
is_dictionary
candidate_analyses[]
selected_analysis
scriptorium_pos
provider_name
provider_version
dictionary_version
```

Selection/disambiguation rules are part of the compatibility profile and must be tested
independently. An unknown token remains unknown; it must not be coerced into a POS to
make percentages add up.

## Metric artifact

Metrics are namespaced and versioned. Each field carries or inherits:

```text
metric_id
value
unit
definition_version
compatibility_status: reproduced | inferred | extension
```

The first implementation should group values into:

- `general`: characters, words, page estimate, word/sentence lengths;
- `dialogue`;
- `vocabulary`;
- `pos`;
- `pos_bigrams`;
- `pos_positions`;
- `punctuation`;
- later `characters`/`connector_bigrams`/`distinctive_words`.

## Benchmark harness

A benchmark case never embeds an unlicensed book. It references a locally supplied or
legally acquired source and stores immutable expected metadata. A run emits:

```text
benchmark_id
input provenance + hashes
analyzer/config versions
expected metrics
actual metrics
delta
comparison rule
pass/fail/unresolved per metric
source-edition confidence
```

FantLab display rounding is part of the comparison rule. The raw internal value is
retained when available so implementation changes cannot game a formatted number.

## Author voice

Do not start author-profile modeling until per-work compatibility metrics are stable.
Profile inputs are immutable analysis artifacts, not raw books. Initial implementation
follows the public FantLab weighted-mean/weighted-standard-deviation description and
then evaluates additional feature selection methods as Scriptorium extensions.

Short texts may be compared, but the output must distinguish `insufficient for corpus`
from `invalid input`: a 5,000-character excerpt is analyzable but cannot become an
author-profile training work under the current manifest.

## Tags

Tags are multi-label metadata with provenance and confidence, not analyzer truth.
Store human/source-provided tags separately from model/inference-produced tags. A tag
profile is an aggregate over admitted work artifacts and must be reproducible from the
same corpus revision.

## Pages

Pages reads generated public artifacts only. Planned top-level views:

- works and filters;
- one work's full metric report;
- authors and voice profiles;
- author/work comparison;
- tags and tag profiles;
- benchmark/parity dashboard;
- methodology/provenance.

Never ship full copyrighted text as a hidden JSON payload for convenience.
