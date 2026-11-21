# Analyze a local text

From the repository root with Python 3.13, run the existing deterministic engine through
`scriptorium.analyze`. No third-party packages or network access are required.

```bash
python -m scriptorium.analyze manuscript.txt --output analysis.json
python -m scriptorium.analyze manuscript.txt --format html --title "My manuscript" --output report.html
```

JSON is the default; omitting `--output` writes the selected format to standard output.
The HTML file is self-contained and can be opened offline. Its table rows, punctuation
chart and headline figures display English and Russian labels for the 29 registered
metrics, using the same translations as the public Reader and the offline
`scriptorium metrics --lang ru` command. The page retains English as its
primary document language and marks Russian
text with `lang="ru"`, and preserves exact metric IDs, canonical units, evidence/status,
raw punctuation counts and keyboard-accessible scrolling regions. The metric row headers
use native `<th scope="row">` contents rather than `aria-label` overrides, so the nested
Russian language spans remain available to assistive technology instead of being
flattened to the English page language. Automated markup checks do not replace
screen-reader pronunciation testing, which remains unverified. This is a display
translation only; it does not localize the scientific contract or prove FantLab parity.

## Reproducibility and scientific limits

The `scriptorium-local-analysis-v1` wrapper retains all 29 current engine rows without
changing their values or formulas. It records the metric contract, normalization/metric/
dialogue/vocabulary/punctuation profiles, raw-byte and normalized-text SHA-256 identities,
input size and dictionary identity. `--scriptorium-revision <git-sha>` records an explicit
caller-supplied revision; without it the revision is null, not guessed. The HTML exposes
profiles under **Analysis profiles**. The HTML renderer requires all 29 current
metric IDs and rejects unregistered FantLab fields, unsupported metric namespaces,
malformed SHA-256 identifiers, contradictory character counts or length thresholds,
invalid analyzer/dictionary metadata, and missing metric evidence. Explicitly
labelled Scriptorium extension fields remain visible under **Other**; no added field
silently becomes a FantLab-compatible result. This checks the artifact's internal consistency; it cannot prove a
caller's hashes came from a particular manuscript or establish FantLab parity.

**Offline CSV and Markdown exports use the same registered evidence validator** as
HTML: metric IDs, units and evidence classes, SHA-256 shapes, source counts,
300,000-character threshold, analyzer profiles and dictionary provenance must agree.
Malformed or relabelled declarations are rejected rather than published as
plausible-looking data. This validation does **not** replay an imported JSON
against the manuscript: use `scriptorium verify` with the original local input for
independent source-bound checking. Unknown metric values remain unavailable,
not zero.

Inputs must be UTF-8. CRLF/CR and Unicode composition use the existing normalization
profile. Empty inputs are supported: counts may be zero, but undefined means or rates
remain null. A null vocabulary metric can also mean a missing dictionary or an incomplete
UASZ window; HTML therefore says **Unavailable**, not a fabricated zero or pass.

The 300,000-character threshold includes spaces. Shorter inputs are valid local analyses
with limited representativeness; meeting the length floor alone is not corpus admission,
proof of representativeness, an author profile or FantLab parity. FantLab-shaped rows
remain inferred; Scriptorium-only rows remain extensions. No morphology backend is
silently instantiated.

## Inspect the installed metric definitions offline

The local report uses the same registered definitions as the deterministic engine.
To see the exact ID, unit, evidence class and compatibility label behind any row
without opening a book or sending data to a service, use the installed CLI:

```bash
scriptorium metrics
scriptorium metrics fantlab.dialogue.share_percent
scriptorium metrics --format json --output metric-contract.json
scriptorium metrics --lang ru
scriptorium metrics fantlab.dialogue.share_percent --lang ru --format json
```

Russian `--lang ru` labels match the reviewed public Reader glossary while preserving
the canonical metric IDs, units, evidence/status flags and dictionary requirements.
Opted-in Russian JSON declares `label_language: "ru"`; default English text and JSON
remain unchanged. This localizes presentation, not scientific evidence or calculations.

The machine-readable `scriptorium-metric-catalog-v1` view lists all 29
registered metric IDs in sorted order and marks the five rows that need
an explicitly supplied dictionary. Its scientific claim is
`DEFINITIONS_ONLY_NOT_FANTLAB_PARITY`: an inferred FantLab-shaped
declaration is not evidence of reproduction, and the one Scriptorium
extension is not an undocumented FantLab feature. The command
performs no manuscript analysis, network access, or registry updates.
Output files are create-only and never silently replaced. Unknown
metric IDs fail without echoing caller-controlled input.

## Optional external dictionary

Supply a UTF-8 file with one lexeme per line and a non-empty profile together:

```bash
python -m scriptorium.analyze manuscript.txt --dictionary dictionary.txt \
  --dictionary-profile my-dictionary-v1 --output with-dictionary.json
```

The engine performs its existing NFC/case-folded set normalization. A supplied dictionary
can enable active dictionary/nondictionary counts and complete-window UASZ values; short
inputs still lack complete larger windows. Results retain profile, normalized lexeme-set
SHA-256 and count, not dictionary contents. Reproducibility does not establish equivalence
to FantLab's undisclosed production dictionary.

## Privacy and file safety

Manuscripts and dictionary contents are not embedded in the returned aggregate artifacts,
sent to a service, or added to the corpus. Titles, dictionary profile labels and optional
revision metadata are caller-controlled and intentionally appear in reports. Hashes and
aggregate metrics can themselves identify a known work: treat generated reports as
private unless deliberately shared. There is no telemetry or external asset loading.

Output is create-only, including existing files, hard-link aliases and dangling symlinks.
The writer stages derived output in the destination directory, flushes it, then uses an
atomic hard-link creation without replacement. The filesystem must support hard links;
otherwise the command reports an error rather than falling back to unsafe overwriting.
Handled write failures remove temporary files and leave previous output untouched. A
process/OS crash may leave a hidden `.scriptorium-*.tmp` derived-report file. On POSIX,
new reports have mode 0600. Parent directories are created as needed.

## Optional original-coordinate spans (local Python API)

The deterministic text profile returns **normalized** half-open token/sentence offsets.
When a local annotator needs to highlight the original manuscript, use the separate,
opt-in `scriptorium-source-spans-v1` API. It does not change the installed CLI, metrics,
source hashes, segmentation profiles, default reports, Pages or FantLab claims.

```python
from scriptorium.text import word_tokens
from scriptorium.source_spans import normalize_with_provenance

original = "A\r\ne\u0301"
p = normalize_with_provenance(original)
assert p.normalized == "A\né"
assert [(w.text, w.start, w.end) for w in word_tokens(original)] == [
    ("A", 0, 1), ("é", 2, 3)]
assert [(p.original_span(i, i + 1).start, p.original_span(i, i + 1).end)
        for i in range(3)] == [(0, 1), (1, 3), (3, 5)]
```

All offsets are Python **Unicode code-point** indices, not UTF-8 bytes or
JavaScript UTF-16 units. `original_span(start, end)` returns an `OriginalSpan`
with conservative source bounds and `exact: bool`. NFC composition and CRLF
can merge source code points; reordering of combining marks can make a
normalized interior span impossible to invert exactly. In that case the
bounds cover all contributing original code points but `exact` is **false**:
never treat such a slice as an exact quotation. The zero-length query is
deliberately rejected rather than inventing an ambiguous interior boundary.

Construction holds the original manuscript plus O(number of input + output
code points) alignment data in memory, with temporary decomposed units;
it is **not** enabled automatically for whole-book analysis or report export.
No source content is persisted, uploaded, logged, or added to the corpus by
this API. Run `python -m unittest discover -s tests -p 'test_source_spans.py' -v`
to exercise original-coordinate consumer, CRLF/CR, NFC, canonical reordering,
Hangul Jamo, empty input and invalid span cases.
## Library and checks

```python
from pathlib import Path
from scriptorium.analyze import build_local_analysis, render_html

artifact = build_local_analysis(Path("manuscript.txt").read_bytes())
html = render_html(artifact, title="Local analysis")
```

Run focused checks with `python -m unittest discover -s tests -p 'test_analyze*.py' -v`.
Tests exercise the real engine, deterministic output, Unicode normalization, dictionary
limits, privacy, output aliases, failed publication and empty inputs.

## Replay the pinned two-book native N diagnostic offline

Run from a complete repository checkout; no manuscript download, morphology
installation or network is required. This **reuses** two previously measured
AOT/pylem 0.0.18 receipts, not a new native experiment.

```bash
scriptorium n-compare --root . --format markdown
scriptorium n-compare --root . --format json --output n-compare.json
scriptorium n-compare --root . --format csv --output n-compare.csv
scriptorium n-compare --root . --format html --output n-compare.html
python -m scriptorium.native_n_crosswork_cli --root . --format markdown
```

The outputs give **counts and denominators** for three disjoint/combined
candidate groups: exclusively N, mixed N plus other runtime POS candidates,
and their sum (any N). Every share is per observed word token; signed deltas
are **Resurrection minus Anna Karenina**, in percentage points. Native
source/edition candidate IDs, normalized/runtime-analysis SHA-256 digests and
native-workflow URLs are included for **both works in every format**, including
standalone CSV rows. The self-contained, no-JavaScript **HTML** report provides a
responsive, keyboard-scrollable table, print layout, decorative percentage bars with
numeric alternatives, and source hashes/workflow links for both books. HTML and
Markdown display two decimal places; CSV displays six, only for presentation;
those are not FantLab's rounding or a parity threshold.

Before deriving values, the reader checks the **exact reviewed Git blob bytes**
of both `assets/n-uncertainty-anna.json` and
`assets/n-uncertainty-resurrection-summary.json`, as well as their pinned
provider/input/artifact identities and consistent counters. Changed, missing,
oversized, symlinked or malformed receipts fail closed. `--output` never
overwrites an existing file. Output contains only source-free aggregates.

The runtime tag `N` collapses noun/cardinal representations; it is **not**
a recovered noun frequency, classifier accuracy, individual-word decision or
FantLab's unpublished homonym policy. Different works are not a controlled
morphology intervention. Corpus and source-matched parity gates do not move:
**M2 remains 0/5**. For the full retained Anna-only conditional interval and
bigram/position evidence use `scriptorium n-evidence --root .`.
