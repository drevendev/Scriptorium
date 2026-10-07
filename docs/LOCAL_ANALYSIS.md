# Analyze a local text

From the repository root with Python 3.13, run the existing deterministic engine through
`scriptorium.analyze`. No third-party packages or network access are required.

```bash
python -m scriptorium.analyze manuscript.txt --output analysis.json
python -m scriptorium.analyze manuscript.txt --format html --title "My manuscript" --output report.html
```

JSON is the default; omitting `--output` writes the selected format to standard output.
The HTML file is self-contained and can be opened offline. Its tables include units,
compatibility labels, raw punctuation counts and keyboard-accessible scrolling regions.

## Reproducibility and scientific limits

The `scriptorium-local-analysis-v1` wrapper retains all 29 current engine rows without
changing their values or formulas. It records the metric contract, normalization/metric/
dialogue/vocabulary/punctuation profiles, raw-byte and normalized-text SHA-256 identities,
input size and dictionary identity. `--scriptorium-revision <git-sha>` records an explicit
caller-supplied revision; without it the revision is null, not guessed. The HTML exposes
profiles under **Analysis profiles**.

Inputs must be UTF-8. CRLF/CR and Unicode composition use the existing normalization
profile. Empty inputs are supported: counts may be zero, but undefined means or rates
remain null. A null vocabulary metric can also mean a missing dictionary or an incomplete
UASZ window; HTML therefore says **Unavailable**, not a fabricated zero or pass.

The 300,000-character threshold includes spaces. Shorter inputs are valid local analyses
with limited representativeness; meeting the length floor alone is not corpus admission,
proof of representativeness, an author profile or FantLab parity. FantLab-shaped rows
remain inferred; Scriptorium-only rows remain extensions. No morphology backend is
silently instantiated.

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
