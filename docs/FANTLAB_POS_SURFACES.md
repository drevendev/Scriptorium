# FantLab POS surfaces

Scriptorium distinguishes two public FantLab POS surfaces that must not be conflated.

## Full documented methodology inventory

FantLab article 374 explicitly says its analyzer computes POS percentages for 22 categories: nouns, adjectives, verbs, three pronoun classes, cardinal and ordinal numerals, adverbs, predicatives, prepositions, **postpositions**, conjunctions, interjections, introductory words, **phrasal verbs**, particles, **short adjectives**, participles, gerunds, **short participles**, and **infinitives**. The same article says POS bigrams and sentence-position statistics cover the listed parts of speech.

Primary evidence: <https://fantlab.ru/article374> (the POS inventory is item 14; bigrams and position metrics are items 15–16).

The pinned AOT backend independently exposes standalone source POS slots for all five categories highlighted above. With national constants disabled, pinned `morph_dict@4c5e9b6d048d1ba74e02988593b23fb0cbc87772` renders them as:

| AOT source category | pylem runtime string | Scriptorium methodology bucket |
| --- | --- | --- |
| `ПОСЛ` | `POSL` | `postposition` |
| `ФРАЗ` | `COLLOC` | `phrasal_verb` |
| `КР_ПРИЛ` | `ADJ_SHORT` | `short_adjective` |
| `КР_ПРИЧАСТИЕ` | `PARTICIPLE_SHORT` | `short_participle` |
| `ИНФИНИТИВ` | `INFINITIVE` | `infinitive` |

Pinned source: `AgramtabLib/RusGramTab.cpp` at revision `4c5e9b6d048d1ba74e02988593b23fb0cbc87772`.

## Observed work-page surface

The current FantLab work-page output observed by Scriptorium exposes a narrower 17-bucket POS table: noun, adjective, verb, the three pronoun classes, cardinal, ordinal, adverb, predicative, preposition, conjunction, interjection, introductory word, particle, participle and gerund.

Public evidence does **not** establish what happened between the full methodology inventory and this narrower work-page presentation. In particular, absence from the visible table is not evidence that postpositions, phrasal verbs, short adjectives, short participles or infinitives are folded into another displayed bucket. They may be omitted from presentation, retained in hidden/internal statistics, transformed by unpublished logic, or handled in some other way.

Therefore `scriptorium-pos-v1` stays unchanged and continues to model only the observed 17-bucket work-page surface. The five additional categories are exposed separately through `scriptorium-fantlab-methodology-pos-diagnostic-v1` as a diagnostic-only methodology view.

## Fail-closed boundaries

The broader methodology view does not solve the other compatibility gaps:

- runtime `N` remains unresolved because pinned AOT renders both noun (`С`) and cardinal numeral (`ЧИСЛ`) to the same Latin string;
- a token with analyses mapping to different methodology categories remains undefined;
- FantLab dictionary identity and homonym-selection behavior remain unknown;
- no full-methodology count is promoted to reproduced status without source-matched benchmark evidence;
- the relationship between full-methodology categories and the current work-page display remains `unknown`;
- M2 parity remains inadmissible.

The machine-readable evidence contract is `compatibility/fantlab-pos-methodology-v1.json`.
