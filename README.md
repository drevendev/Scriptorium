# Scriptorium · Literary language reader

**See a book's language, not a made-up quality score.** Scriptorium is an open-source, Russian-first literary analyzer. Compare dialogue, sentence rhythm, vocabulary and punctuation across measured editions — or analyze your own UTF-8 text / EPUB **locally**, without uploading it.

**[Explore the Russian Reader →](https://drevendev.github.io/Scriptorium/)** · [See the real measured Robinson Crusoe translation](https://drevendev.github.io/Scriptorium/?book=shishmareva#measurements) · [Compare two Russian books](https://drevendev.github.io/Scriptorium/?left=anna&right=beketova&pair_metric=fantlab.punctuation.dash.per_1000_words#pairs)

**[How to read the 29 metrics →](https://drevendev.github.io/Scriptorium/metrics.html)** — Russian-language, no-JavaScript guide to current inferred formulas, exact units, dictionary requirements, punctuation edge cases and FantLab definition evidence. Each metric name in the interactive single-book and paired tables links to its exact definition; the full guide is also available without JavaScript. Every field remains **inferred** (or an explicitly labeled Scriptorium extension), not source-matched parity.

**Look up metrics offline (English or Russian):** `scriptorium metrics --lang ru` shows the same 29 definitions with Russian labels matching the public glossary; canonical units, IDs and scientific status stay unchanged. The installed `scriptorium metrics` command lists all 29 engine-defined IDs, units, evidence labels and dictionary requirements, while `scriptorium metrics fantlab.dialogue.share_percent --format json` inspects a single definition without opening or uploading a manuscript. See [local analysis and the metric catalog](docs/LOCAL_ANALYSIS.md). These are **inferred/extension definitions, not FantLab parity**.

**Historical translation research preview:** the 1775 Yakov Trusov *Robinson Crusoe* has a reproducible **incomplete** Pages 3–147 diagnostic: 303,882 characters including spaces, 22 numeric metrics and seven unavailable values, each source-bound to 145 pinned Page revisions. [Inspect the Russian-language measured excerpt in Reader](https://drevendev.github.io/Scriptorium/#trusov-excerpt) or [the source-free 29-metric receipt](https://github.com/drevendev/Scriptorium/blob/master/corpus/candidates/diagnostics/defoe-robinson-crusoe-trusov-1775-ru.interior-measured.json) or [download the 29-field source-free CSV](https://drevendev.github.io/Scriptorium/assets/trusov-1775-interior-metrics.csv). Opening Page 2 and final Pages 148–151 are excluded; the synthetic page join and historical rendering are not verified. This is **not** a twelfth complete edition, translation comparison, author profile or FantLab parity (M2 0/5).

### What works now

| In the `master` Reader | Verified source-backed scope |
| --- | --- |
| **11 measured Russian-language editions** | 13 catalogue cards; 2 research leads are explicitly **not analyzed** |
| **298 recorded metric fields** | 249 numeric observations; 49 unavailable / NOT_RUN — never converted to zero |
| **9 interactive charts** | Dialogue, sentence rhythm and punctuation (including questions per 1,000 words); exact-value accessible tables, labels, units, chart links and CSV exports. Each metric shows the measured-edition minimum, median and maximum (missing data excluded, true zero retained); these are descriptive sample summaries, not author scores or FantLab parity. |
| **Book and pair comparisons** | Author/translator attribution, edition hashes, signed **descriptive** chart/table deltas (right minus left; percentage points for percents; nonzero differences below 0.001 visibly bounded instead of rounded to zero), an exact nine-metric no-JavaScript pair-table fallback plus three measured punctuation mini-charts, all 28 Anna Karenina metrics without JavaScript (23 measured, 5 unavailable), accessible tables and exact-value exports |

In the verified pair table, the **Только показатели, измеренные в обеих книгах** checkbox hides rows missing either observation (e.g., 7 shared of 9 for the Beketova comparison), while measured zero remains a number. The live status now reports missing observations separately for the left and right edition (0 left / 2 right for Beketova); the two missing counts can overlap when the same metric is unavailable for both. It changes only the displayed table, not the full nine-field no-JavaScript fallback or source-bound JSON/CSV/Markdown exports; pair links intentionally reopen the complete table.

The catalogue can order all 13 edition cards by Russian title, **measured dialogue share**, or **measured normalized-text length in characters including spaces** (both descending, with missing measurements and unmeasured leads last). Zero is distinct from unavailable; length is not a quality or FantLab parity score. It reorders real page elements so keyboard navigation follows the visual order; without JavaScript the original source-backed catalogue remains readable. Shared catalogue search links preserve the selected sort order through the allow-listed `catalog_order=title|dialogue|length` parameter; invalid values fall back to the original order.

**Find author + translator together:** catalogue search accepts several space-separated words in any order across a book's verified title, author and translator metadata (e.g. `Верн Бекетова` or `Дефо Шишмарева`). All words must match; uppercase, `ё/е` and repeated spaces are normalized. Search is local to the browser; it never searches or uploads book prose. An unmatched combination shows the existing empty state and reset action. Shared search links retain the original query and safe mode/order filters.

**Original-language filter:** the Russian Reader can narrow its thirteen edition cards by Russian, English or French **source-language origin** (10 / 2 / 1 cards, including clearly marked unmeasured leads). Combine it with measurement status, translator/title search and sorting; the safe share link uses `original=ru|en|fr`. This does **not** analyze English/French originals or imply a translated-text equivalence. Invalid URL values fall back to all origins; resetting the catalogue clears this facet without discarding unrelated comparison links.

**Interpret private comparisons:** local two-report HTML and Markdown exports now show length-aware interpretation notes before the 29-field table. Short inputs (under 300,000 normalized characters including spaces), empty inputs, and input pairs with at least a 2× length difference receive explicit caveats. Raw word/character/sentence deltas depend on input length; rates remain descriptive and are **not** author fingerprints, statistical confidence estimates, or FantLab parity proof. This does not upload manuscript text or change JSON/CSV schemas.

**One-click book comparisons:** after the pinned 13-book JSON passes validation, each of the 11 measured book cards gains an accessible **Compare with another book** action. It keeps a different currently selected comparison partner (avoiding self-comparison), selects an actually available shared chart metric when necessary, updates the comparison permalink, and focuses the result. Two unmeasured leads never receive comparison actions. Without JavaScript or verified JSON, cards retain their direct source-evidence links; charts remain diagnostic only.

**Copy measured comparisons:** after the pinned Reader snapshot passes validation, the pair view offers a keyboard-accessible **Скопировать ссылку на сравнение** action. It copies only a same-site link to two distinct measured editions and an allow-listed chart metric, never book text or local input. If secure clipboard access is unavailable or denied, the visible permalink remains usable; without JavaScript the static pair example and link remain available. Slow clipboard completion cannot report success or failure for a comparison that has since changed. The chart's copy action has the same protection.

**Browser acceptance evidence:** the Pages CI also exercises the *actual staged branch-root Reader* in headless Chromium at desktop (1440px) and mobile (390px) widths. It changes books, tests the 7/9 common-metric comparison and real zero/missingness display, checks keyboard skip navigation and all 29 glossary targets, loads the author-evidence page and CSV, then captures screenshots and an A4 print PDF as a seven-day `scriptorium-browser-acceptance` artifact. This is repeatable browser execution, **not** independent inspection of the live GitHub Pages deployment, nor assistive-technology speech verification. A failed interactive or layout assertion blocks the related Pages build; derived source-free data and scientific M2=0/5 claims are unchanged.

**Keyboard and mobile reading:** pressing Tab at the start of the branch-root Reader reveals shortcuts to the catalogue, comparisons and measurement registry. Wide exact-value tables have focusable scroll regions with touch/arrow-key instructions. The source-backed tables remain readable without JavaScript; live mobile/browser visual acceptance is still separate. Deep links from the interactive metric labels now land on one of 29 programmatically focusable, visibly highlighted glossary rows (`tabindex=-1`, not additional Tab stops). This is a structural keyboard improvement; assistive-technology pronunciation and mobile screenshots remain unverified.

Select any measured book in the Reader's measurement registry to see **three other measured editions closest by dialogue share, average sentence length and comma frequency**. The new Scriptorium-neighbors-v1 navigation uses per-field min–max normalization across compatible observed editions and links directly to the existing, source-bound two-book comparison. It is a **relative exploratory distance**, not an author fingerprint, quality score, or FantLab parity result; missing numbers and unmeasured leads never become ranked neighbors. Without JavaScript a clearly labeled starting comparison remains available.

The results include Russian originals and **separately identified translations**, including Alexandra Beketova's *Children of Captain Grant* and Maria Shishmareva's *Robinson Crusoe*. The latter is pinned to Wikisource oldid `5634933`: **572,587 characters including spaces; 24 numeric measurements and 5 NOT_RUN**. See the [source-free measured record](corpus/candidates/diagnostics/defoe-robinson-crusoe-shishmareva-1935-ru.measured.json). An English/French original has **not** been analyzed as a counterpart; cross-language or two-translation conclusions are **not** available yet.

The [translation readiness table](https://drevendev.github.io/Scriptorium/#translations) now distinguishes the **measured 1935 Shishmareva edition** (572,587 characters; 24 numeric fields, five NOT_RUN) from the **unmeasured 1775 Trusov witness** (150 frozen historical Page revisions, not a reconstructed literary body). It links directly to each retained evidence record and keeps cross-translator comparisons disabled until both literary texts are independently measured. Trusov's French intermediary is a material confounder; no translation-style or FantLab parity is claimed.

### Explore two source-backed author rhythm previews from the CLI

The [public author-rhythm preview](https://drevendev.github.io/Scriptorium/voice/) compares **two measured Russian works by Alexander Grin and two by Leo Tolstoy**, using eight versioned metrics per author. Install the Python package from a checkout, then run `scriptorium voice` from **any working directory**. Its wheel includes the exact pinned **source-free measurement snapshot**, not book text or manuscripts. Inspect the same observations offline as Markdown or reproducible JSON:

```bash
scriptorium voice --format markdown
scriptorium voice --check assets/voice-preview.json
scriptorium voice --format json --output author-rhythm.json
```

The report prints individual book values, word-count-weighted author means and **between-book** population standard deviations. It uses only source-free measurement evidence; it does not read manuscripts, train a classifier, or claim confidence intervals. Two works per author are not enough to establish a stable author fingerprint; M3 remains open and FantLab parity remains **M2 0/5**. Generated files are never overwritten. The bundled source snapshot is checked against its retained Git blob identity on every default run. `--check assets/voice-preview.json` needs that separately supplied reference file (available in a checkout); `--snapshot /path/to/evidence-snapshot.json` explicitly overrides the bundle while retaining source-identity validation. This is **not** a general author profiler for arbitrary private text.

**[See the four-fold failures in the public Reader](https://drevendev.github.io/Scriptorium/voice/#holdout): only 1 of 4 books was closer to its known author.** This is an in-sample exploratory negative result, not external validation or FantLab parity.

**Test whether the differences hold up:** `scriptorium voice --holdout --format markdown` performs four leave-one-book-out folds on the same strictly pinned source-free measurements. Each fold removes one book from both author centroids, then reports a normalized, equally weighted eight-feature distance to the remaining books. On these four selected editions, **only 1/4 held-out books is closer to its labelled author** (three are closer to the other author). This is useful *negative* evidence against calling these eight features a reliable author fingerprint. It is not an independently validated classifier, its distance is not a probability, and the selection is too small to establish generalization. Run `scriptorium voice --holdout --format json` for exact machine-readable folds; `--output` still refuses overwrites. The original `voice` JSON/Markdown contracts remain unchanged. M2 0/5, M3 open.

**Probe which of the eight measurements matters to that fragile result:** `scriptorium voice --ablate --format markdown` repeats the same four leave-one-book-out folds eight times, omitting exactly one feature at a time. The result is **1/4 for seven omissions and 2/4 when question-mark frequency is omitted**; only *Дорога в никуда* changes its nearest author. JSON output (`--format json`) contains the exact seven-feature distances for every book, the omitted metric ID/unit, the preserved pinned data hash, and the scientific boundaries. This is a **sensitivity diagnostic, not a reason to remove question marks or tune a classifier on the same four books**. Validation on genuinely new works/authors is still missing; no FantLab parity or M3 acceptance is claimed. `--ablate` and `--holdout` are mutually exclusive and neither can be combined with `--check`. Reports remain offline and source-text-free; `--output` refuses overwrites.

**[Inspect all eight feature-removal results in the public Reader](https://drevendev.github.io/Scriptorium/voice/#sensitivity)** — accessible counts/diagrams, pinned evidence, reproducibility commands and the warning against selecting features on these same four books. The table does not claim external validation, reliability or FantLab parity.

**Optional third author, versioned source-backed CLI preview:** `scriptorium voice --include-dostoevsky --format markdown` adds **Fyodor Dostoevsky** from two previously measured, separately pinned Russian editions: *The Brothers Karamazov* (1,810,351 characters) and *Humiliated and Insulted* (713,925 characters). The distinct v2 JSON contains three authors and six source-bound works with eight descriptive metrics, book-weighted means and between-book dispersion per author. Generate a reproducible private offline report with `scriptorium voice --include-dostoevsky --format json --output three-authors.json`, and verify with `scriptorium voice --include-dostoevsky --check three-authors.json`. The default v1, public four-book Reader preview, 1/4 holdout and ablation experiments remain **unchanged**; the optional third author is not retrospective external validation of those original experiments. Two books per author cannot establish a reliable fingerprint: **M2 0/5, M3 open**. No manuscripts are fetched or exported.

**[Inspect the six-book, three-author negative result in the public Reader](https://drevendev.github.io/Scriptorium/voice/#holdout-three)** — a separate, source-bound table of all six held-out works and their three numeric distances (2/6 nearer their known author). No JavaScript, manuscript downloads, classifier claim or FantLab parity are involved. The existing four-book Reader experiment remains unchanged. **[Download source-bound six-fold CSV](https://drevendev.github.io/Scriptorium/voice/holdout-three.csv)** (dimensionless distances, known/nearest author, and snapshot Git blob). Regenerate exactly with `scriptorium voice --include-dostoevsky --holdout --format csv`. This is an exploratory in-sample diagnostic, not classifier accuracy.

**[See the three-author nearest-profile matrix](https://drevendev.github.io/Scriptorium/voice/#triad-matrix-title):** a no-JavaScript 3×3 chart of which author's profile was nearest for each of the six already measured Russian books. Of Grin's two books, neither is nearest Grin; Tolstoy and Dostoevsky each have one self-nearest book. Every cell is a source-checked count out of two, with an accessible table and the six exact distances below. This describes within-sample mismatches, **not** classifier accuracy, author-quality ranks or FantLab parity.

**Six-book falsification check (opt-in):** `scriptorium voice --include-dostoevsky --holdout --format markdown` independently removes each book before computing the three remaining author centroids, then compares the eight unchanged features. With six already frozen books, only **2/6** are nearest their known author (4/6 nearer another author; 0 ties). JSON is available using `--format json` or `--output six-book-holdout.json`; the result carries the snapshot Git blob, all six excluded keys, per-author training books, distances and an explicit `scriptorium-author-rhythm-holdout-v2` scientific boundary. The four-book v1 holdout and ablation outputs do not change; ablation remains deliberately unavailable with `--include-dostoevsky` to prevent accidental in-sample feature selection. This diagnostic is **not** a classifier accuracy estimate, independent external validation, or M3/FantLab completion. The holdout now checks that an imported preview's declared word-weight totals and all eight six-decimal weighted means/deviations agree with its per-work measurements and versioned metric profiles; inconsistent previews are rejected. This is an **internal consistency** gate, not cryptographic authentication of imported values or proof of source identity.

### Analyze your own writing in two commands

Python **3.13+**; run from a checkout (no account, telemetry, manuscript upload or runtime API required):

```bash
python -m pip install .
scriptorium analyze manuscript.txt --format html --output report.html
```

Open `report.html` locally; use `--output analysis.json` for a reproducible JSON result. The standalone HTML renderer rejects saved JSON rows that relabel any of its 29 registered metrics' units or definition evidence (for example, punctuation rates mislabelled as percentages); this checks internal declarations, **not** the authenticity of source hashes or FantLab parity. For private text on stdin (without creating a manuscript file):

```bash
cat manuscript.txt | scriptorium analyze - --format html --output report.html
```

Only the explicit `-` reads a pipe/redirect, not an interactive terminal. Stdin is limited to 32 MiB, must be UTF-8 and never becomes a corpus upload. The derived report has no source prose; `--output` refuses to overwrite existing output. Avoid piping private results to external services. The analyzer also supports source-free Markdown/CSV, unencrypted EPUB and local pair comparison. **[Commands and examples ↓](#try-your-own-text)** · [EPUB security and limits](docs/PRIVATE_EPUB.md) · [Offline Reader preview](docs/READER_PREVIEW.md).

**Private HTML dialogue chart:** each locally generated HTML report now includes a source-bound, no-JavaScript 0–100% dialogue-character bar alongside its exact numeric table and punctuation chart. The denominator is **non-whitespace characters**, not sentences; the unfilled region is not necessarily narration. Missing values say unavailable rather than drawing a zero bar, and short-excerpt and FantLab-parity caveats remain visible. The metric engine, JSON/CSV contracts and input privacy are unchanged.

### What the numbers do — and do not — mean

Measured counts and rates are **inferred Scriptorium metrics**, not a verified reimplementation of FantLab's hidden algorithms. The original input editions used by FantLab have not been identified, morphology still has documented unknowns, and **M2 parity remains 0/5**. `NOT_RUN` means unavailable, not zero. Short excerpts can be analyzed privately but do not qualify for the ≥300,000-character parity/author-profile corpus. Never assume web availability gives reuse rights; the public Reader stores derived values and provenance, **not book prose**.

This repository serves two different experiences: [branch-root Pages Reader](https://drevendev.github.io/Scriptorium/) and the separately generated local/CI `build/site` Reader. GitHub merges and CI builds alone are **not** independent live-site or mobile-visual verification; current browser `LIVE_VERIFIED` / `VISUAL_VERIFIED` remains **NOT_RUN**. [Full project gates](project/PROJECT_MANIFEST.md) · [Current task state](project/STATE_AND_QUEUE.md) · [Historical Reader release notes](docs/reader-history.md).

**AOT morphology uncertainty for researchers:** `scriptorium n-evidence --root . --format markdown` inspects the retained native `pylem==0.0.18` N-only ambiguity without rerunning the dictionary or reading book prose. It now presents source-bound conditional POS-bigram ranges per **1,000 total word tokens**, sentence-position percentages of **all sentences**, and noun/cardinal ranges as a share of **conditionally defined tokens**; JSON/CSV preserve exact raw bounds and the weaker independent-edge upper bound. Markdown also shows the achievable and looser independent-edge ceilings in **both raw pairs and rates per 1,000 word tokens**, without treating either bound as observed morphology. These are hypothetical individual-cell sensitivity ranges, **not** observed noun/cardinal tags or FantLab parity (M2 **0/5**). See the [public N ambiguity tables](n-uncertainty.html), including exact conditional versus independent-edge limits, and [AOT evidence and units](docs/AOT_PYLEM_COMPATIBILITY.md).

### Quantify a real FantLab word-count discrepancy (diagnostic only)

**[See the annotated Anna Karenina word-density case study →](word-density.html).** The root Reader now has a no-JavaScript, source-free visual comparison, a labelled exact-value table and an explicit unmatched-edition warning. Its eight published numeric cells are checked in regression tests against `scriptorium word-gap` over frozen evidence; the case study does not turn density proximity into parity.

Run `scriptorium word-gap --root . --format markdown` (or `json` / `csv`) to calculate **word density per 1,000 characters including spaces**, plus a conditional character-length-adjusted word residual, from the already-verified, source-free FantLab benchmark evidence. For the frozen *Anna Karenina* candidate, FantLab reports 253,275 words / 1,692,647 characters versus Scriptorium's 269,358 / 1,705,605: **149.632499 vs 157.925194 words per 1,000 characters**, a signed gap of **+8.292695** and conditional residual **+14,144.062082 words** after proportional length scaling. This is a concrete segmentation/evidence investigation lead, **not** a measured tokenization error or proof of identical input editions. No manuscripts are fetched or exported; unknowns are `NOT_RUN`, M2 remains **0/5**.

### Test word boundaries on the **same** local text

Run `scriptorium word-boundaries manuscript.txt --format markdown` to compare seven explicit word-count policies on the *same normalized, privately held UTF-8 input*. The existing `scriptorium-text-v1` tokenization stays unchanged. Independent probes split internal ASCII hyphens, straight/curly apostrophes, or join Unicode U+2010/U+2011 hyphens; a separate probe merges dotted initialisms (such as `А.Б.`), and another excludes decimal-only tokens. The result gives count deltas and per-1,000-current-word rates; use `--format json --output probe.json` to save a create-only, source-free report. Input is bounded to 32 MiB, refuses symlinks, and is never uploaded. Empty input produces `NOT_RUN` for undefined rates. This is a controlled **inferred diagnostic**, not recovered FantLab tokenization or a way to attribute the Anna gap to one cause. [Earlier frozen Anna word/dash sensitivity](benchmarks/fantlab/work270306-policy-sensitivity.json) already tested numeric-only removal and Unicode hyphen joining; the exact-body replay in [#452](https://github.com/drevendev/Scriptorium/pull/452) now records those independent variants without claiming FantLab semantics. **M2 remains 0/5.**

**[Explore the full-book word-boundary experiment in the Russian Reader →](word-density.html#boundary-experiment).** All seven one-factor counts are shown in an accessible exact table and a common-zero delta chart: 269,358 baseline words; ASCII hyphen split +1,611; curly apostrophe split +46; numeric-only removal −17; three other variants 0. All values come from the [retained pinned 239-revision replay](benchmarks/fantlab/work270306-word-boundaries.json), not a fabricated example. Each change is independent (not additive). The FantLab input edition is **UNKNOWN**, diagnostics remain **DIAGNOSTIC_ONLY**, **M2 0/5**. The root branch site has the case study; deployment/live verification is a separate gate.

### Reproduce the pinned full-book boundary experiment

The **existing** frozen Anna Karenina CI replay can run the seven boundary variants
over exactly the **same 239 identity-checked public-domain Wikisource chapter revisions**
as the historical 1,705,605-character diagnostic. The opt-in
`python -m scriptorium.repro_diagnostic --reference benchmarks/fantlab/work270306.json --manifest corpus/candidates/source-edition-traces/tolstoy-anna-karenina-ru.revisions.json --scriptorium-revision LOCAL_SHA --with-boundary-probe --output derived.json`
adds `word_boundary_sensitivity` to the source-free diagnostic; the
[`repro-diagnostic` CI workflow](.github/workflows/repro-diagnostic.yml) also
checks that the prior frozen source digest and three previously measured
word-policy counts have not drifted. **No second fetch** and no prose artifact
is produced. The first verified [CI run #42331164429](https://github.com/drevendev/Scriptorium/actions/runs/42331164429)
replayed all **239 pinned revisions** and produced the
[source-free full-work receipt](benchmarks/fantlab/work270306-word-boundaries.json).
For the frozen 1,705,605-character input, current Scriptorium counted **269,358 words**;
splitting internal ASCII hyphens yields **270,969** (+1,611),
splitting curly apostrophes **269,404** (+46), and excluding numeric-only
tokens **269,341** (−17). Straight-apostrophe splits, Unicode-hyphen joining
and dotted-initialism merging each changed the count by **zero**.
All seven changes are **independent**, not a combined prediction; no variant
accounts for the unmatched FantLab word-count difference. The original
FantLab analyzer-input edition is still UNKNOWN and M2 remains **0/5**.

## Language modules and translations

The Russian module (`ru`) is the initial product priority. Every analyzed literary body has an **analysis language** and an independent **edition identity**. A translated work additionally records the author's original language, a named translator and a specific edition/source family; another translator or translation revision becomes a separate identity, not another spelling of the title. The measured Russian translation of **Дети капитана Гранта** by **А. А. Бекетова** has 11 real derived fields, but no measured French original. The researched translation of **О происхождении видов** by **С. А. Рачинский** has no retained numeric fields, and its English source is not analyzed here. Never place invented English/French numbers into Russian graphs. See [versioned language/translation contract](docs/TRANSLATIONS_AND_LANGUAGE_MODULES.md).

**Current branch-root Reader coverage:** 11 measured Russian-language editions / 13 catalogue entries; the other two are explicitly unmeasured research leads. All 298 recorded fields are source-bound derived observations (249 numeric, 49 unavailable), not FantLab source-matched parity. The stricter FantLab M2 gate remains **0/5**.

## Try your own text

With Python 3.13 or later, from this checkout:

```bash
python -m pip install .
scriptorium analyze manuscript.txt --format html --output report.html
scriptorium analyze manuscript.txt --output analysis.json
scriptorium analyze manuscript.txt --format csv --output metrics.csv
scriptorium analyze manuscript.txt --format markdown --output report.md
```

The standalone HTML report includes a **14-category punctuation-frequency chart** drawn from the same measured values as its exact table. It works without JavaScript; each bar is scaled to the highest available rate **within that one report**, not to a percentage or FantLab score. Zero and unavailable measurements remain distinct; tiny nonzero rates have visible ticks. This is a descriptive visualization, not parity evidence.

Open `report.html` locally, or read `report.md` as a portable, source-free Markdown table
with canonical metric IDs, exact numeric values, profile versions and SHA-256 identities.
Both reports label inferred/extension evidence and preserve unavailable values as unknown;
neither implies FantLab parity. Keep `analysis.json` for reproducible private comparisons.

To **verify a saved JSON report** against its original manuscript locally, without
sending the text or its result to a server:

```bash
scriptorium verify manuscript.txt analysis.json
cat manuscript.txt | scriptorium verify - analysis.json
# Or replay a saved EPUB JSON report using the exact local EPUB archive:
scriptorium verify --epub novel.epub novel-analysis.json
# Also check archive identity when the original provenance sidecar was saved:
scriptorium verify --epub novel.epub novel-analysis.json --provenance novel-identity.json
# Deterministic machine-readable success only (nonzero exit and no JSON on failure):
scriptorium verify manuscript.txt analysis.json --json > verification.json
```

`--json` emits one `scriptorium-local-verification-v1` PASS record after a complete
replay, with `archive_identity` marked `VERIFIED` only when the original EPUB
sidecar was checked. Without `--provenance`, EPUB archive identity is `NOT_CHECKED`;
for TXT it is `NOT_APPLICABLE`. No manuscript content, private paths or saved
revision assertions enter this machine record. A failure exits nonzero with
stderr and **never emits PASS JSON**; do not treat absent output as success.
This record is local computation evidence, not a signed attestation or a
FantLab/rights/edition claim.

A successful verification recomputes all 29 metric rows, source hashes, profiles,
units, missing values and report metadata with the **current** implementation.
It fails on altered text, changed metrics, unsupported report fields or missing
original dictionary configuration. Supply `--dictionary dictionary.txt
--dictionary-profile PROFILE` if the original report used one. Input files are
bounded and symlinks are rejected; error messages do not reveal paths or prose.
For `--epub`, the same bounded in-memory EPUB 2/3 spine extractor replays its
UTF-8 body without writing text to disk. Without the optional `--provenance`
sidecar, **the input hash identifies the extracted body, not the original ZIP**:
different EPUB archives with identical spine text both pass. With the sidecar
from `scriptorium epub --provenance-output`, exact archive SHA-256, extraction
profile, chapter counts and both text digests must also match. Symlinks,
invalid/oversized EPUBs, malformed sidecars and private-path disclosure fail
closed. This checks deterministic replay, **not** a report's claimed Git revision,
legal permission, source-edition match or FantLab parity.
All **29 metric rows** retain their units and algorithm
profiles; unavailable measurements stay unknown. The report has readable metric names,
a four-value overview, exact numeric values and keyboard-accessible tables. JSON and
CSV include source digests, not manuscript content. Choose a new output filename for
each run: existing files are never overwritten.

No runtime dependencies, account, server or telemetry are required. Installation may
fetch build tools; see [offline wheel installation](docs/READER_PREVIEW.md).
`python -m scriptorium` exposes the same commands from a checkout.

## Analyze an unencrypted EPUB locally

Import an EPUB 2/3 with a standard XHTML reading-order spine without uploading
the book or writing its extracted chapters to disk:

```bash
scriptorium epub book.epub --output analysis.json --provenance-output epub-identity.json
scriptorium epub book.epub --format html --output analysis.html
scriptorium epub book.epub --format csv --output metrics.csv
scriptorium epub book.epub --format markdown --output analysis.md
```

The regular Reader **29-metric** reports use the same evidence and profile labels as
TXT analysis. Markdown is a portable source-free table; retain a JSON report for
`scriptorium compare`.
The separate source-free receipt records the **archive**, **extracted UTF-8
body** and **engine-normalized text** SHA-256 identities plus the versioned
extraction profile. EPUB reading order follows OPF spine order; unsupported
encrypted, malformed, unsafe or image-only books fail closed. No DRM bypass,
external network resources or embedded scripts are processed. This local
EPUB text projection is **not** FantLab edition/input parity or corpus admission.
[EPUB formats, safety limits and reproducibility](docs/PRIVATE_EPUB.md).

## Analyze a private batch (POSIX preview)

Select up to 16 UTF-8 manuscripts explicitly in a JSON manifest, then generate
source-free per-work reports and an HTML/JSON/CSV index locally:

```bash
printf '%s\n' '{"schema_version":"scriptorium-private-batch-manifest-v1","files":["first.txt","second.txt"]}' > manifest.json
scriptorium batch manifest.json --output-dir private-results
```

The manifest paths are relative to its directory. No implicit crawling, uploads,
overwrites or source-text publication. Failed items are marked unavailable,
never assigned zero metrics. Re-running an unchanged batch reuses identical
outputs; conflicting files fail closed. Use a private POSIX filesystem:
directory-relative no-follow operations are required. This workflow does not
admit works to the corpus or establish FantLab parity.
[Batch use, limits and exit codes](docs/PRIVATE_BATCH.md).

## Compare your own analyses

```bash
scriptorium analyze second-manuscript.txt --output second-analysis.json
scriptorium compare analysis.json second-analysis.json --output comparison.html
scriptorium compare analysis.json second-analysis.json --format json --output comparison.json
scriptorium compare analysis.json second-analysis.json --format csv --output comparison.csv
scriptorium compare analysis.json second-analysis.json --format markdown --output comparison.md
# Or directly compare two private UTF-8 manuscripts without intermediate JSON:
scriptorium compare --texts first-manuscript.txt second-manuscript.txt --format markdown --output direct-comparison.md
# Or compare two private unencrypted EPUB editions without intermediate JSON:
scriptorium compare --epubs translation-a.epub translation-b.epub --format markdown --output translations.md
# Or mix local TXT, EPUB and existing analysis JSON inputs explicitly:
scriptorium compare draft.txt edition.epub --left-kind text --right-kind epub --output mixed.html
scriptorium compare edition.epub analysis.json --left-kind epub --right-kind json --format markdown --output mixed.md
```

The `--texts` path runs the same local deterministic analyzer on both manuscripts
and compares their 29 measurements without uploading text; each input is bounded
to 32 MiB. Its source-free output is byte-identical to the two-JSON-report path
for the same input bytes and profiles. Unlike imported JSON, the hashes are
computed from the actual selected local files; no edition identity or FantLab
parity is established (M2 0/5).

Imported analysis JSON is treated as an **untrusted declaration**, not a
replayed measurement: the comparison validator checks obligatory counts,
derived punctuation rates and the aggregate budget of disjoint word tokens
plus punctuation events against the stated normalized character count. For
dictionary-backed vocabulary, a rolling UASZ window also cannot claim more
distinct dictionary lexemes than the document's entire active dictionary
vocabulary, even when the external lexicon contains more words.
A self-consistent-looking forged rate cannot claim more events than the
declared text could contain. These checks reject contradictions; they do
not authenticate the declared source SHA-256 or prove FantLab compatibility.
Private `compare --format markdown|html` reports now expose both each metric's
compatibility classification and its actual definition-evidence label; neither
is a claim of reproduced FantLab behavior. CSV/JSON retain those fields.

The `--epubs` mode uses the same bounded EPUB 2/3 XHTML-spine extractor and
29-metric analyzer as the separate `scriptorium epub` command; all four export
formats match separately analyzing each EPUB as JSON and comparing the two reports.
No extracted prose or intermediate JSON is written. Comparison source hashes
identify **extracted UTF-8 bodies, not EPUB archive bytes**; use
`scriptorium epub --provenance-output` for archive/body identities. Encryption,
DRM bypass, guessed translator/edition identities and FantLab parity are excluded.

For different source types, give **both** `--left-kind` and `--right-kind`
(`text`, `epub`, `json`); legacy `--texts` and `--epubs` keep working
for same-type pairs. Types are never inferred from filenames. The mixed
comparison uses the same bounded local readers, 29 metrics, extracted-body
SHA-256 for EPUB and create-only source-free reports; it does not establish
translator/edition identity or FantLab parity.

Use `comparison.md` for a portable Markdown table with complete provenance,
29 metric comparisons, unknown/incompatible statuses and the unchanged scientific caveat.

Open `comparison.html` for the same 29 measurements, plus a no-JavaScript
**14-category punctuation comparison chart**: both reports share one scale for
rates per 1,000 words, with exact values and signed differences beside every pair.
Method-incompatible/missing rates never become false zero bars; the complete
accessible table remains available, alongside source identities and exact **right minus left** differences. Percentage differences use percentage points.
Unknown measurements do not become zero; different methods or dictionaries are labelled
incomparable where applicable. JSON decimal observations and their differences retain
precision. Contradictory counts, means, punctuation rates and same-text results are rejected.
Imported JSON and hashes are declarations, not authenticated proof: rerun the analyzer
on the original bytes to verify them. [Comparison contract and examples](docs/PRIVATE_COMPARISON.md).

## Compare in your browser (private beta)

Build the canonical site with `scriptorium site --repo-root . --output build/site`
and open `build/site/compare/index.html`, or use the **Compare private reports**
action in the generated homepage. Select two local `scriptorium analyze` JSON
reports; no manuscripts or report bytes are uploaded. Inspect all 29 measurements,
incomparable/missing reasons, exact decimal right-minus-left differences, and
download source-free JSON/CSV. The browser validates the same versioned report
contract as the installed Python Reader and rejects duplicate keys, integer
lexeme spoofs, impossible counts, nonfinite values and changed units. Browser
support requires JavaScript; the offline `scriptorium compare` CLI always works.
[Browser validation and limitations](docs/PRIVATE_COMPARISON.md).

This is a **local build capability**, not a live GitHub Pages deployment. No private
manuscripts are included; imported report hashes are unauthenticated declarations.
Scientific/FantLab parity remains unverified (M2 0/5).

## Open a real literary result

The repository contains a source-free, historical full-work diagnostic for
**Anna Karenina**: **28 expected/actual/delta rows**, with 23 numeric results and five
unavailable values. No novel download is needed:

```bash
scriptorium diagnostic benchmarks/fantlab/work270306-wikisource-diagnostic.json \
  --title "Anna Karenina — full-work diagnostic" --output anna-report.html
scriptorium site --repo-root . --output build/site
```

Open `anna-report.html` or `build/site/index.html`. The canonical site retains the five
earlier evidence/report routes and the Reader 0.3 two-book comparison route.
**A successful local build is not a live GitHub Pages deployment.** The Pages activation
interlock is unchanged; this preview does not enable publishing by itself. Atomic site
replacement currently requires Linux `renameat2`; unsupported platforms fail without
deleting the previous build. Private text analysis and comparison are separate capabilities.

## Compare two already-analyzed books

No manuscript download or morphology setup is needed for the frozen **Running on Waves**
and **Children of Captain Grant — Beketova translation** comparison:

```bash
mkdir -p build
python -m scriptorium.full_work_gallery --repo-root . --format html > build/full-work-gallery.html
python -m scriptorium.full_work_gallery --repo-root . --format csv > build/full-work-evidence.csv
```

Open `build/full-work-gallery.html` for ten exact measurements and seven row-wise charts.
These are Scriptorium-side results, not FantLab parity or author-style scores. The pinned
canonical site route is `build/site/works/two-full-work-differences/index.html`, with
`measurements.json` and `measurements.csv` downloads. Navigation and export links have
44-pixel minimum touch targets; visible focus and reduced-motion styles are retained.
Newly approved replacement evidence must declare compatible source units before display;
legacy Grin diagnostics are not assigned invented source-unit fields.
Building this route does not prove GitHub Pages is deployed. Shell redirection replaces
its destination; use new filenames to keep older exports. [Method and limits](docs/FULL_WORK_GALLERY.md).

## Inspect FantLab reproduction readiness

Inspect **five frozen public literary sources** and the distance between their
character counts and the *displayed* FantLab counts, without downloading books:

~~~bash
python -m scriptorium.benchmark_readiness --root . --format markdown
python -m scriptorium.benchmark_readiness --root . --format json --output readiness.json
~~~

Each source-free report includes source rights/edition evidence, immutable body
hashes, dated FantLab references and explicit source-matching status. Differences
are **diagnostic only**: FantLab's analyzer-input identities remain unknown
and **M2 stays 0/5**. This character-count readiness command labels other
metrics NOT_RUN **in this view only**; it does not erase existing, independently
validated field-level observations in the metric matrix below.
[Readiness methodology, CSV and limitations](docs/BENCHMARK_READINESS.md).

To inspect **actual retained per-metric differences** rather than character counts alone,
run `python -m scriptorium.benchmark_metric_matrix --root . --format markdown`.
The Markdown summary now separates locally measured fields, retained FantLab
reference values and numeric pairs; individual missing reference values say
**UNKNOWN**, not **NOT_RUN**. CSV keeps its existing numeric cells and adds
`reference_availability` / `actual_availability` labels so an absent public
reference cannot be mistaken for a failed local measurement. Numeric pairs
remain source-unmatched diagnostics, not evidence of parity. The CSV
`parity_blockers` column and Markdown per-field blocker labels now show exactly
which source, reference, local or displayed-rounding evidence is still missing;
they do not change JSON v1 or count as M2 parity.
The source-free matrix validates **171 field-level diagnostic/extension rows**:
142 across the five core works (**five works with retained measurements**),
plus 29 *Resurrection* rows as a sixth, separately pinned source-unmatched
diagnostic. All **five** frozen works have field observations; none has an
established FantLab analyzer-input identity. *Anna Karenina* has 28 rows
(23 numeric, five without actuals), *Running on Waves* has 27
(23 numeric, four NOT_RUN), while *The Silver Dove*, *The Brothers Karamazov*
and *The Hyperboloid of Engineer Garin* each have 29 rows (24 numeric,
five dictionary-dependent NOT_RUN). Among these five core works, 118
actual values are measured and 24 remain unavailable. The Hyperboloid
rows reuse the already SHA-pinned, successful CI receipt and verified
499,066-character source body; its unmatched-reference differences are
+3,527 characters and +2,795 words, **not** a FantLab parity result.
The supplemental *Resurrection* contributes 29 fields (24 measured, five
NOT_RUN), with two retained FantLab counts and unmatched differences
+9,591 characters and +9,672 words. In total, the six diagnostics have
142 measured fields and 29 unavailable actuals. 
Other reference values and exact input identity remain
UNKNOWN; none establishes FantLab parity. Anna's historical rows include 4/4 general, 4/4 dialogue,
14/14 punctuation and 1/6 vocabulary measurements; its other five vocabulary
actuals are two NOT_RUN and three unresolved.

The generated evidence Reader displays all 29 Silver Dove, 29 Brothers Karamazov and 29 supplemental Resurrection fields in accessible static tables, and links to the existing independently validated 29-row Hyperboloid detail route,
including separate unknown FantLab references and an explicit extension marker.
It also labels metric units and percentage-point differences, and offers
**independent search/filter controls for both books** by metric name/ID,
family and availability. Tables and source-free JSON/CSV remain available
without JavaScript and in print. A separate **20-row side-by-side comparison**
shows only shared measured word/sentence lengths, punctuation rates and dialogue
percentages (Running on Waves minus Anna Karenina, percentage differences in
percentage points). Unlike total characters or vocabulary counts, these carry
explicit per-unit denominators, but remain **descriptive, source-unmatched
Scriptorium candidates**, not author-style or FantLab-parity evidence.
Neither retained work is source-matched to FantLab's analyzer input, displayed
rounding is unproven, and **M2 stays 0/5**.
Build the site with `scriptorium site --repo-root . --output build/site` and open
`build/site/evidence/fantlab/index.html` to browse the same verified five-work readiness evidence plus the separately labelled Resurrection diagnostic
and download its source-free JSON/CSV. The same page now also shows each
frozen work's character count, signed diagnostic difference from FantLab's
displayed count and source/edition/rights link. It also shows **signed
relative drift** as (frozen minus FantLab displayed) divided by FantLab
displayed, expressed in percent and rounded to two decimal places.
This display-only diagnostic is not a parity score and does not alter JSON/CSV.
These counts do not establish FantLab analyzer-input identity. The evidence page
also offers **source provenance JSON/CSV** downloads generated from the same
five validated readiness witnesses as the visible work table. The JSON contains
raw and normalized SHA-256 digests, reference dates and legal/source metadata;
the CSV retains raw digests and reference dates. No manuscript text is included.
The homepage links to this route.
This is a
**locally built** page, not a confirmed live GitHub Pages deployment.
[Field-level matrix and evidence checks](docs/BENCHMARK_METRIC_MATRIX.md).


To join a separately generated **source-free POS artifact from the same normalized
text** into a FantLab benchmark, add `--pos-metrics pos.json` to the
`python -m scriptorium.benchmark --reference ... --text ... --scriptorium-revision ...`
command. This adds **40 explicitly unresolved/diagnostic POS rows**, including
17 visible category counts and percentages, but never claims POS parity.
Unmatched text digests, profiles or inconsistent 17×17/20×17 structures are
rejected. The work488 FantLab category counts are not a simple partition of
defined words, and service-word actuals remain unknown.
[POS benchmark usage and evidence boundaries](docs/BENCHMARKING.md).

## What the results mean

FantLab-shaped metrics are **inferred compatibility candidates**, not demonstrated
parity. Scriptorium-only features are **extensions**. The historical Anna diagnostic
has no established identity match to FantLab's input text. **M2 remains 0/5**; none of
M1–M5 is declared complete by this preview. The AOT-lineage morphology target and
field-by-field parity criteria remain unchanged.

Texts shorter than 300,000 characters including spaces are valid inputs with explicit
representativeness limits. That length is a corpus-admission floor, not a guarantee of
quality; legal provenance and source identity require separate evidence. Source books,
private manuscripts and dictionary contents are not included in reports or uploaded.
Hashes can identify known works; share derived reports deliberately.

## Safety and reproducibility

The CLI bounds manuscripts to 32 MiB and dictionaries and comparison reports to 8 MiB
per file, rejects special files and symlinks, and uses a create-only atomic writer.
Operational errors do not echo private paths or source text. CSV neutralizes formula-like
**text** while preserving numeric cells; spreadsheet import/save behavior is not universally guaranteed.

```bash
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . --wheel-dir dist
```

The Reader workflow runs the complete canonical suite, builds a full wheel and tests it
outside the checkout: actual manuscript analysis/comparison, HTML/JSON/CSV, historical
report, safe failures and deterministic source-free gallery/site. No analyzer stubs are
used in the private-comparison acceptance. Package, project and CLI versions must agree.
The full Python public API, morphology modules, benchmark data and corpus records remain
in place. No external package-registry release is performed by CI.

Site locks are persistent regular files whose kernel locks are released on process death.
Do not delete a lock file while a publisher could be using it. Legacy directory locks
from an interrupted older preview fail closed and are not automatically deleted.

## Documentation

[Reader installation and commands](docs/READER_PREVIEW.md) ·
[Local analysis and dictionaries](docs/LOCAL_ANALYSIS.md) ·
[Private comparison](docs/PRIVATE_COMPARISON.md) ·
[Private batch](docs/PRIVATE_BATCH.md) ·
[Frozen diagnostic methodology](docs/FROZEN_DIAGNOSTIC_REPORT.md) ·
[Five-work benchmark readiness](docs/BENCHMARK_READINESS.md) ·
[Canonical site and publication boundary](docs/FULL_WORK_SITE_REPORT.md) ·
[Roadmap and repository assessment](project/ROADMAP.md)

The detailed [Research and evidence index](RESEARCH_INDEX.md) retains project history,
corpus investigations and original reference links. Private EPUB and batch Reader
capabilities have been integrated into the repository; their inputs remain local.
The browser comparison is merged into master as a local-build capability;
public deployment remains unverified and separately gated. Code/data licensing and Pages activation retain separate gates (#284/#285).

Reader FantLab evidence now includes an offline-only metric explorer (label/ID, family and measurement availability) with a complete no-JavaScript/print table. Scientific source-match and parity status remain unchanged; see [benchmark evidence](docs/BENCHMARK_METRIC_MATRIX.md).
