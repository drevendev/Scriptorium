# Local lexical contrast · source-free extension v1

Status: **private, executable Scriptorium extension** (#562), not FantLab reproduction, a rights clearance, corpus admission, or author attribution.

The `scriptorium distinctives` command compares two **local UTF-8 files** without network access. It returns only numeric aggregates, declared edition/language/translation identities, normalized text digests, exact counts and methodology. It does **not** return word forms, top words, source excerpts, rare-word hashes or per-word frequencies. Input files are never added to the repository or Pages. This is deliberately separate from the 29 compatibility metrics and the existing Reader comparison.

## Try offline

```console
scriptorium distinctives left.txt right.txt \
  --left-edition edition-A --right-edition edition-B \
  --format markdown
scriptorium distinctives left.txt right.txt \
  --left-edition edition-A --right-edition edition-B \
  --format json --output private-contrast.json
```

## Re-render an existing private report (no manuscript needed)

After creating `private-contrast.json` above, make an accessible offline HTML,
CSV or Markdown view **without reopening either source text**:

```console
scriptorium distinctives --report private-contrast.json \
  --format html --output private-contrast.html
scriptorium distinctives --report private-contrast.json --format csv
```

The replay accepts only a bounded regular UTF-8 JSON file. It rejects duplicate
JSON keys, NaN/Infinity, unexpected source-bearing fields, contradictory
counts/metadata, and incompatible profiles through the same strict source-free
renderer validation as a freshly analyzed report. Source files/edition flags
cannot be mixed with `--report`; outputs remain create-only. The saved JSON
contains normalized input SHA-256 hashes and user-declared metadata, **not**
word forms or manuscript text. Replay verifies artifact structure and internal
consistency, not independently verified edition rights, source identity or
FantLab parity. Keep the report private unless separately cleared for release.

For a spreadsheet-friendly **source-free, create-only CSV** (fixed four-column
`section,field,value,unit` rows; no words or word-level hashes):

```console
scriptorium distinctives left.txt right.txt \
  --left-edition edition-A --right-edition edition-B \
  --format csv --output private-contrast.csv
```

This local CSV includes normalized source digests, declared edition and translator
metadata, explicit units, method/profile evidence, and aggregate observations. A missing
aggregate is `NOT_RUN`, never numeric zero; optional unknown metadata are `UNKNOWN`.
Potential spreadsheet formulas in untrusted text labels are prefixed with an apostrophe;
CSV quoting alone is not a formula defense. **Never publish** private comparisons on
Pages without independent rights and provenance review. CSV adds an output format,
not a new FantLab compatibility profile or clearance.

To produce a **readable standalone local HTML report** (no scripts, remote fonts, images, network calls or source words):

```console
scriptorium distinctives left.txt right.txt \
  --left-edition edition-A --right-edition edition-B \
  --format html --output private-contrast.html
```

The HTML has accessible labelled tables for numerical aggregates and declared edition identities, mobile horizontal scrolling, print styling and a restrictive Content Security Policy. All user-provided edition/translator metadata are escaped; the result explicitly distinguishes unavailable aggregates from measured zero and shows short/unequal-length warnings. JSON, HTML and Markdown replays now also fail closed on malformed or spoofed aggregate numbers, profile tags, witness fields and contradictory token warnings, using the same CSV validation contract before rendering. JSON additionally rejects undeclared top-level and witness keys, so stored reports cannot smuggle source excerpts into otherwise source-free exports. Previously valid pre-overlap v1 reports remain readable with unchanged JSON serialization; validation is not independent rights verification. The HTML is **private** and must not be published on Pages without independent source/rights review. It contains normalized SHA-256 digests of complete inputs for local replay, but no form-level hashes or manuscript words.

Both `--output` examples **create new** private artifacts; existing files are never overwritten. There is no `--publish` option. Names supplied on the command line are **unverified claims**. Filenames and manuscript content do not appear in the output. Files have the same bounded regular-file and UTF-8 restrictions as local analysis.

For a translation-pair hypothesis, explicitly declare the distinct editions and their common original:

```console
scriptorium distinctives left.txt right.txt \
  --left-edition translation-1900 --right-edition translation-1950 \
  --left-original source-work-A --right-original source-work-A \
  --left-translator "Translator A" --right-translator "Translator B" \
  --translation-pair
```

A missing or different original-work ID in translation-pair mode yields `INCOMPARABLE_TRANSLATION_LINEAGE`, with **null** aggregate fields; differing declared languages yield `INCOMPARABLE_LANGUAGE`. These checks prevent a falsely labeled translation comparison, but cannot authenticate the user-supplied lineage. The two translations must have **distinct edition IDs**, even if their normalized text happens to match. Reusing one edition ID for both sides is allowed only for a self-comparison with the same normalized bytes, declared language, original-work ID and translator; contradictory declarations are rejected instead of producing misleading numeric evidence. General, non-translation comparisons need not share an original.

## Fixed, inspectable method

- Profile: `scriptorium-lexical-aggregate-contrast-v1`; artifact: `scriptorium-private-lexical-contrast-v1`.
- Scriptorium `scriptorium-text-v1` normalization (CRLF/CR to LF, Unicode NFC) and `scriptorium-vocabulary-v1` word tokens followed by NFC + `casefold`. The comparison uses **surface forms**, not lemmas, and does **not** merge `е` and `ё`. The FantLab lexeme/dictionary identity is unknown.
- Each form's unsmoothed denominator is **all word tokens in its own text**. The pooled type union is used for both smoothed dominance denominators. There is no external dictionary; dependency is explicitly `null`.
- Only types with at least **five occurrences pooled across both texts** contribute to dominant-form counts. Excluded rare forms still contribute to the empirical distribution-divergence value; their word identities never leave the process.
- The additive `scriptorium-lexical-type-overlap-v1` extension counts exact **shared**, **left-only**, and **right-only** distinct casefolded surface forms, including types below the five-occurrence dominance threshold. Type Jaccard similarity is `100 × shared / (shared + left-only + right-only)`, reported as a percentage rounded to six places, **not a statistical significance/confidence score**. Neither forms nor per-form hashes are serialized. A true 0% means disjoint nonempty type sets; empty or incomparable inputs return `NOT_RUN`, never 0. All four local formats show these observations. Historical pre-overlap v1 aggregates remain CSV/HTML/Markdown-readable.
- The additive `scriptorium-lexical-token-overlap-v1` extension measures **token-distribution overlap**, `100 × Σ min(count_left / tokens_left, count_right / tokens_right)`, over every pooled casefolded surface form, including rare ones. This unsmoothed probability-mass intersection ranges from 0% (no shared observed forms) to 100% (identical observed relative frequencies), rounded to six places. Two texts with the same two types can have 100% type Jaccard but only 20% token overlap if their 9:1 and 1:9 frequencies are reversed. It is a descriptive token-frequency comparison, not a similarity confidence score, plagiarism metric or author fingerprint. Empty/incomparable input stays `NOT_RUN`; historical v1 reports without this additive field remain readable in all table outputs.
- The descriptive dominance decision is based on Jeffreys pseudocount `0.5` per type on each side: `p_left=(count_left+0.5)/(tokens_left+0.5*pooled_types)`, likewise for right. A left-dominant type has `p_left/p_right >= 2`; a right-dominant type has the inverse at least 2. Other eligible types are balanced. Counts are **types**. Per-side token shares are fractions of all **tokens** on that side that belong to forms dominant on that same side.
- Jensen–Shannon divergence is `(KL(P||M)+KL(Q||M))/2`, where `P` and `Q` are **unsmoothed** observed relative frequencies, `M=(P+Q)/2`, logs are base two. It lies in [0, 1] bits and is rounded to six decimal places. The sorted union and `math.fsum` make reductions deterministic. A zero divergence means identical observed lexical **distributions**, not necessarily identical texts. The smoothing prior affects dominance only, not divergence.
- An empty/no-token input gives `NOT_RUN_EMPTY` and `aggregate: null`, not a fictitious zero contrast. Identical normalized bytes give `IDENTICAL_NORMALIZED_TEXT` and zero divergence. Different source strings can have the same case-folded distributions, also yielding zero divergence.
- Normalized character counts include spaces; the existing `length_ratio_max_over_min` and `length_imbalance_warning` continue to flag **character** lengths at least 2:1.
- The additive `word_token_ratio_max_over_min` and `word_token_imbalance_warning` independently compare **word-token counts**, the actual frequency denominators, at the same 2:1 threshold. A character-balanced pair can still have twice as many words on one side. The ratio is `null` in JSON and `UNKNOWN` in CSV/HTML/Markdown when either input has no words; no missing observation becomes zero. All four local formats expose the token ratio or caution. Older v1 artifacts lacking these additive fields remain CSV-readable.
- Texts below **300,000 characters including spaces** are valid **local, nonrepresentative** previews only.

## Rights and evidence boundary

Every local artifact has `corpus_admission: NOT_VERIFIED`, `public_release_ready: false` and `metadata_verified: false` even if both files exceed 300,000 characters. The caller cannot turn local analysis into public corpus admission by supplying flags, titles or translator labels. A future publicly presented comparison needs independently established lawful source rights, frozen edition/source/translator identity, replayable versioned analysis, and privacy review. In the current Reader, 11 complete measured editions and two research leads must not be retroactively called lexical-contrast results: the existing 29-field derived snapshots do **not** contain the token distributions needed here.

Type overlap is an unweighted surface-form presence comparison: a frequent word and a one-off rare form each count as one type. It complements, but must not be confused with, token-frequency Jensen–Shannon divergence or the five-occurrence dominance threshold. Sharing an aggregate report does **not** imply permission to publish its source text or add it to the corpus.

This extension is descriptive, highly sensitive to length, orthography, vocabulary topic, editions, translations and normalization. It does not produce significance tests, author voice/fingerprint claims, semantic tags, FantLab unpublished scores or M2 parity (**0/5**). No licensed manuscript or private original should be uploaded merely to run or share this extension.

## Frozen two-book experiment (candidate, not published)

The dedicated `python -m scriptorium.grin_lexical_pair` runner replays **two already
frozen, public-domain Russian original works** by Alexander Grin: *Road to Nowhere*
(az.lib-derived Wikisource oldid 5585836, 442,656 characters, SHA-256
`e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee`)
and *Running on Waves* (36 exact pinned literary revisions, 363,819 characters,
SHA-256 `41a1ada3caabea2909976372ca6312fb8a478f2d0d87c088f304fcb30c52fdbc`).

It reuses the separate fail-closed revision/body replay validators and the v1
aggregate lexical CLI; source text exists transiently only during execution.
The GitHub workflow emits reviewed **source-free** JSON and offline HTML as
short-lived CI artifacts, with no prose, form lists or hashes of individual rare
forms. Each work exceeds the 300,000-character calibration floor; that alone does
not prove a source-matched FantLab input, a printable-edition collation, or an
author-fingerprint model. The two editions come from distinct transcription
families; the comparison is descriptive and orthography-sensitive. The v1
lexical report intentionally retains `public_release_ready=false` and
`corpus_admission=NOT_VERIFIED`; its wrapper records verified source replay,
rights evidence and the separate, still-required public Reader review.
**Do not publish the CI artifact on Pages before exact-head acceptance.**

## Reviewed public diagnostic projection (Reader candidate)

The separately reviewed #613 full-text CI result is frozen at GitHub Actions run
[45009800452](https://github.com/drevendev/Scriptorium/actions/runs/45009800452),
artifact ZIP SHA-256
`6c8ab5c170024554e0d92ba116acf0cf028d3bb6abba49e2fb8a86d99a7e2117`
and JSON SHA-256
`90b80850c4a3c7f376bdb4c8deb704c8eac495b3c26b89a5a3c767ae0fbc5d36`.
The public-facing `lexical-grin.html` page and
`assets/grin-lexical-diagnostic.json` are a **new, strictly numeric projection**,
not a publication of the original private JSON or HTML. The original local
`public_release_ready=false`, `metadata_verified=false` and
`corpus_admission=NOT_VERIFIED` claims are **not** changed into a corpus
admission, licensed-source grant, FantLab parity or author fingerprint.

The underlying literary originals by Alexander Grin (1930, 1928) are identified as
public domain on the exact Russian Wikisource works; the first witness is frozen at
oldid 5585836 (az.lib family) and the second at 36 frozen 1965-family chapter
revisions. The new page publishes only aggregate integers/floats, source hashes
and attribution links, no original prose or individual word forms/hashes. Other
edition content, scanner material and unrelated manuscripts are not licensed by
this diagnostic. The page's independent acceptance requires browser desktop,
mobile, keyboard, print and exact Pages-route checks, separate from CI build
or any deployed/live claim. M2 stays **0/5**.
