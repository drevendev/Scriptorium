# Reader preview 0.2.0a1

Refs #273. This is a substantial integration preview, not completion of the scientific
v1 milestone. It combines #268, #270 and #272 with selected reader improvements from
local handoffs. It does not replace the canonical package with the minimal initializer
used by the old standalone Workbench.

## Install and use

Python >=3.13 is required. The distribution is `scriptorium-reader`; the import package
and console command remain `scriptorium`. Install into a dedicated virtual environment
so a previous experimental Workbench distribution cannot overwrite the same package.

```bash
python -m venv .venv
# Activate .venv with the command appropriate to your shell.
python -m pip install .
scriptorium --version
scriptorium --help
```

To prepare an offline installation on another compatible machine:

```bash
python -m pip wheel --no-deps . --wheel-dir dist
# Transfer the wheel; the destination does not need the source checkout to analyze text.
python -m pip install --no-index --no-deps dist/scriptorium_reader-0.2.0a1-py3-none-any.whl
```

Building may fetch setuptools/wheel. Runtime processing and installation of a prepared
wheel with `--no-index --no-deps` do not need a package index. No package is automatically
published to an external registry.

## Three real commands

- `analyze manuscript.txt --format json|html|csv --output report.ext` computes all 29
  current metric rows with the unchanged deterministic core. `--dictionary` and
  `--dictionary-profile` must be supplied together. Titles/profile labels are intentionally
  visible; do not put private data in them.
- `diagnostic artifact.json --title "A reviewed result" --output report.html` presents
  the canonical frozen-diagnostic schema. It is not a fresh analyzer run. Input is
  bounded to 8 MiB, duplicate JSON keys are rejected, and operational errors are path-free.
  Use curated source-free artifacts: the renderer is not a manuscript sanitizer.
- `site --repo-root /path/to/Scriptorium --output build/site` runs the existing allow-list
  renderer. Site data are not bundled into the wheel: point it at a repository checkout.
  This maintenance/build command retains its existing repository-path diagnostics.

The legacy module commands remain available. Prefer `scriptorium diagnostic` over the
legacy `python -m scriptorium.frozen_diagnostic_report` CLI when reading external files;
the new wrapper supplies bounded I/O without altering the historical renderer bytes.

## Numeric and security contracts

JSON values and all core algorithm versions are unchanged. HTML floats now use their
round-trip decimal representation. CSV v1 requires exactly the current 29 metric IDs,
nonempty units/definition evidence and explicit source/profile fields. Null numeric
values become empty cells. These serialization checks are not proof of authenticity or
FantLab parity. CSV text formula neutralization includes Unicode formatting prefixes;
spreadsheet-specific import and re-save behavior remains outside this guarantee.

Manuscripts are limited to 32 MiB and dictionaries to 8 MiB. Byte limits are checked
before and after reading. POSIX nonblocking/no-follow flags prevent FIFO blocking and
final-component symlink swaps; equivalent race guarantees on other platforms are not
claimed. Parent directory symlinks are not sandboxed. New outputs use mode 0600 on
POSIX and atomic hard-link creation: a filesystem without hard-link support fails
rather than overwriting. Process/OS crashes can leave a hidden derived-output temporary
file. The limits bound input bytes, not total analyzer working memory.

## Acceptance and adoption

Run all canonical tests, not only a reconstructed subset. Reader CI builds the wheel,
installs it into a clean virtual environment, runs from outside the checkout, checks
the exported public API and exercises all three commands. Pages CI separately rebuilds
the actual five-route site twice. Neither CI success nor a PR is a live deployment.

The new PR targets master directly. Old #268/#270/#272 are provenance/de-duplication
references and remain open until the integrated result is accepted. A later fresh
exact-head acceptance is required; no same-run merge is authorized. Preserve all
historical artifacts, AOT compatibility, scientific tolerances and corpus/rights gates.
