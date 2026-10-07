# Read a frozen full-work diagnostic

From a repository checkout with Python 3.13, turn the existing aggregate Anna Karenina
comparison into a standalone report without downloading the novel:

```bash
python -m scriptorium.frozen_diagnostic_report \
  benchmarks/fantlab/work270306-wikisource-diagnostic.json \
  --title "Anna Karenina — full-work diagnostic" \
  --output anna-diagnostic.html
```

Open `anna-diagnostic.html` in a browser. It needs no network, JavaScript, remote fonts
or external assets. Omit `--output` to write HTML to standard output. The file option is
create-only: an existing output is never overwritten, including after invalid input.
Use a new filename for a second report. Without `--title`, the candidate ID is shown.

## What the report contains

The existing historical diagnostic has 28 rows: 23 numeric actuals and five missing
actuals, with 26 `unresolved` and two `not_run` results. Tables group general, dialogue,
vocabulary and punctuation metrics and show units, expected values, actual values and
raw deltas. Captions, row/column headers, a skip link, focus styles and keyboard-focusable
horizontal table regions keep the wide tables inspectable on small screens.

Replay hashes, chapter count, analyzer revision, Python version and hosted-run identity
are retained. Omitted families and observations are explicitly historical: the report
is not a new replay and does not imply that an old provider limitation is current.

## Scientific boundary

This renderer accepts the reviewed `scriptorium-frozen-diagnostic-v1` shape only. Its
source edition is unknown; parity admissibility remains false. The displayed M2 `0/5`
is the value recorded in that historical artifact, not a live project-progress query.
Numeric resemblance, including a zero delta, is never promoted to pass/fail or a
similarity score. No analyzer formula, source body or historical JSON is modified.

Display uses up to six decimal places and scientific notation for very small nonzero
values. This is readability formatting, **not** FantLab display rounding or a tolerance
change. Percentage deltas are percentage points; missing values are not zero.
Integer delta arithmetic is exact. The `1e-9` absolute consistency check for floating
raw deltas handles serialized arithmetic only; it cannot admit a parity result.

## Validation and privacy

The CLI rejects duplicate JSON keys, unexpected fields, invalid hashes/locators,
non-finite or out-of-range numbers, delta inconsistency, `not_run` with an actual value,
pass/fail promotion, source-text publication flags, and source-match/M2 upgrades.
All artifact-controlled strings are HTML-escaped.

Inputs must already be curated source-free aggregate artifacts. This is not a manuscript
sanitizer: reviewed observations and reason strings are intentionally displayed, so a
producer must not put private source prose in those fields. The renderer never fetches
source text or uploads anything. Generated HTML stays local and is not committed.

## Verification and publication

```bash
python -m unittest discover -s tests -p 'test_frozen_diagnostic_report.py' -v
python -m unittest discover -s tests -v
```

The focused suite includes the exact canonical diagnostic blob and deterministic output,
large-integer precision, tiny deltas, escaping, invalid-input rejection and preservation
of an existing output. The existing Pages PR workflow runs the full repository suite and
a byte-identical static-site rebuild on the PR head.

This unit supplies a standalone report, not a new live Pages route. Adding the report to
the publication allow-list and renderer is a subsequent integration; Pages activation
and the existing deployment interlock are unchanged.
