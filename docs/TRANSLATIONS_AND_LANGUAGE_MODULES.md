# Scriptorium — Russian-first Reader, editions and translations

Status: Product/measurement specification alongside the ten-entry Russian catalogue PR. The default Pages language is **Russian**. English is an independent future analytics module; a French original is not an English original.

## Identity, not just book titles

Every entry is keyed by its own `candidate_id`, `family_id`, `edition_id`, `language` (analyzer language) and `original_language`. Two editions/versions/translator attributions must never share an edition key. A translated edition additionally requires a nonempty named translator with an authority record, rather than leaving it blank or silently attributing translated style to the original author.

- **Дети капитана Гранта:** Jules Verne; original French; Russian version by Alexandra Andreyevna Beketova, a separately frozen source/transcription family. The 1955 Detgiz cited edition is bibliographic evidence, not byte-level identity to that print copy. The source-free Russian version already has 11 deterministic numeric Scriptorium fields. The French original is **NOT_ANALYZED**.
- **О происхождении видов:** Charles Darwin; original English; 1864 Russian translation by Sergey Aleksandrovich Rachinsky, with versioned ProofreadPage route/page identities under investigation. Literary-body extraction and numeric measurements are **NOT_RUN**; an English analyzer does not exist yet.
- Russian originals in the current measured set are Anna Karenina, Running on Waves, Silver Dove, Brothers Karamazov and Hyperboloid of Engineer Garin, each with its own pinned body and scientific limits.

The catalogue has ten entries; **six measured, four awaiting measurement**. No raw source prose or unlicensed private text is published. The 153 recorded field rows (129 actual, 24 unavailable) refer only to the six measured entries; the other four are not metric entries. Corpus length/rights admission and FantLab M2 exact-source parity are *separate* gates. M2 remains 0/5.

## Comparison rules

Within the active Russian module, the Reader can show **descriptive** differences of the same candidate-normalized metric when both editions have measured values, matching algorithm profile versions and matching candidate units. Chart values come from the pinned source-free JSON, not made-up genre scores. The pair view reports signed **right minus left**, percentages in *percentage points*, and never converts UNKNOWN/NOT_RUN into zero. Word totals, raw vocabulary cardinality, and corpus length are deliberately excluded from paired normalized comparison. A shared value does not imply a common underlying FantLab input or an author/translator causal effect.

Between an original and a Russian translation, the future paired view must require an independently rights-cleared frozen original, full source/edition IDs, language-specific tokenization/morphology and cross-language measurement contracts. Differences in word count, mean word length or unique vocabulary across English, French and Russian are *not* direct style parity without a separately validated cross-language normalization policy. Versions by different translators should be compared within Russian first, on compatible measurements, and differences attributed to **editions**, not automatically to translators.

## Language separation

`ru`: active; Scriptorium deterministic metrics profile v4 and separately labelled AOT-lineage compatibility research. `en`: planned/not measured; its lexical/sentence/morphology profiles require a separate implementation and tests. `fr`: original-language future source module, also not measured. Neither may reuse Russian model counts while silently claiming original-language support.

## Evidence requirements for expanding from six to ten analyzed works

For each pending entry — Resurrection, Road to Nowhere (explicit alternate transcription), Petersburg (1916 facsimile) and Darwin/Rachinsky — require: precise edition/legal basis, at least 300,000 characters **including spaces** for corpus use, frozen/replayable source identity, deterministic analyzer version and source-free derived JSON, documented UNAVAILABLE/NOT_RUN and explicit original/translation attribution. Publish a work as measured only after tests, source digest and exact-head CI pass. Source-research cards remain visibly distinct until then; no empty work masquerades as an analyzed novel.

### Provenance and further details
- [Russian Beketova translated edition](../corpus/candidates/source-edition-traces/verne-children-captain-grant-beketova-ru.json)
- [Russian Darwin/Rachinsky edition](../corpus/candidates/source-edition-traces/darwin-origin-species-rachinsky-1864-ru.json)
- [Hyperboloid reproducible source profile](../corpus/candidates/source-edition-traces/tolstoy-hyperboloid-garin-wikisource-ru.json)
- [FantLab metric and equality contract](FANTLAB_METRIC_CONTRACT.md)
