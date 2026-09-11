# Research evidence and compatibility notes

Last reviewed: 2026-09-11

This file records public evidence that directly changes Scriptorium's design. It is not
a link dump. Detailed conclusions belong in specifications/tests once implemented.

## FantLab analyzer article

Source: https://fantlab.ru/article374

The article by Alexey Lvov says the analyzer was developed for FantLab in 2007-2008
and computes more than one thousand characteristics. Publicly named feature families
include:

- average sentence length overall, in narration and dialogue;
- dialogue share and author-text share inside dialogue;
- unique words, dictionary vocabulary, non-dictionary vocabulary;
- specific active vocabulary over 3,000, 10,000 and 100,000-word windows;
- parts of speech, POS bigrams and POS by sentence position;
- punctuation frequencies;
- character bigrams and cross-word character features;
- first-character word-pair features;
- frequencies of a selected set of high-variance distinguishing words (reported as
  about 1,400 words in the 2022-era method).

For author profiles, the article describes a word-count-weighted mean for each feature
and a word-count-weighted standard deviation across an author's works. It describes a
feature-weight heuristic based on between-author spread divided by average within-author
spread, reporting weights above 0.7 as an effective author-style feature set.

The article reports author-recognition accuracy of 98.79% for novels and 84.32% for
short stories in its tested setup, but explicitly says corrective coefficients and some
implementation know-how are not published. Scriptorium must therefore label a behavior
as reproduced only after benchmark evidence, not because the public formula looks
plausible.

## First numeric target: FantLab work 488

Source: https://fantlab.ru/work488/lp
Analysis date shown by FantLab: 2022-09-19
Work: Henry Lion Oldie, `Шутиха`

The page publishes a useful first regression target: 357,565 characters, 49,009 words,
mean word length 5.8, mean sentence length 62.06 characters, narration sentence length
79.38, dialogue sentence length 39.53, dialogue share 27.86%, author text in dialogue
4.77%, 13,069 unique words, dictionary vocabulary 11,561, non-dictionary vocabulary
1,508, UASZ-3000 1688.66 and UASZ-10000 4341.13. It also exposes POS counts/shares,
POS bigrams per 1,000 words, POS by sentence position and punctuation frequencies.

These values are copied as factual benchmark metadata with the source URL in
`benchmarks/fantlab/work488.json`. The page does not grant Scriptorium a copy of the
underlying full novel; the benchmark is not valid for parity until exact/traceable
input text is legally available.

## FantLab ranking surface

Source: https://fantlab.ru/rating/work/lingvo

The ranking exposes at least `SZ10` (UASZ-10000) and `SLEN` (mean sentence length) over
a large set of analyzed works and supports sorting/correlation views. This is useful for
finding candidate parity works and for population-level sanity checks, but population
agreement cannot substitute for source-matched field-by-field benchmarks.

## AOT morphology lineage

Primary code lineage: https://github.com/sokirko74/aot

The maintained AOT repository describes the RML package and Russian morphology as
LGPL-licensed. FantLab's article explicitly thanks Alexey Sokirko/AOT for the
morphological analyzer used for its work.

Python candidate: https://pypi.org/project/pylem/

`pylem` is maintained by Alexey Sokirko, MIT-licensed, and describes itself as a Python
wrapper for the historical AOT C++ morphology library. It is therefore the first
compatibility backend to test. This is a provenance advantage, not proof of identical
2022 FantLab dictionaries or disambiguation behavior.

## Design consequences

1. Store a versioned `fantlab` compatibility profile instead of baking assumptions into
   generic metrics.
2. Separate deterministic text segmentation/counting from morphology so both can be
   reverse-engineered independently.
3. Keep raw/normalized text hashes and exact dependency versions in every parity run.
4. Record expected, actual and delta values per metric; do not hide mismatch behind an
   aggregate score.
5. Treat AOT dictionary/version drift as a benchmark variable.
6. Keep author-recognition/profile work after the per-work metric surface is stable;
   otherwise profile deltas conflate hundreds of lower-level incompatibilities.
