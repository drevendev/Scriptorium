"""Installed reader entry point; reuse canonical analysis and publication modules."""
from __future__ import annotations

import argparse
import importlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import sys

COMMANDS = {"batch": "scriptorium.batch", "analyze": "scriptorium.analyze", "epub": "scriptorium.epub", "compare": "scriptorium.compare", "site": "scriptorium.site_renderer", "evidence": "scriptorium.benchmark_metric_matrix", "n-evidence": "scriptorium.native_n_evidence"}
MAX_DIAGNOSTIC_BYTES = 8 * 1024 * 1024


def diagnostic_main(argv: list[str]) -> int:
    from .analyze import LocalInputError, _read_bounded_regular_file, _write_new
    from .frozen_diagnostic_report import _unique_keys, render_html

    parser = argparse.ArgumentParser(description="Read a curated frozen diagnostic without downloading a book.")
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        raw = _read_bounded_regular_file(args.artifact, MAX_DIAGNOSTIC_BYTES, "diagnostic")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys)
        rendered = render_html(value, title=args.title)
        if args.output is None:
            print(rendered, end="")
        else:
            _write_new(args.output, rendered)
    except FileExistsError:
        parser.error("report output already exists; choose another destination")
    except LocalInputError as exc:
        parser.error(str(exc))
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError):
        parser.error("unable to read the curated diagnostic or create the report")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--version"]:
        try:
            installed = version("scriptorium-reader")
        except PackageNotFoundError:
            installed = "source checkout (distribution version not recorded)"
        print(f"Scriptorium Reader {installed}; inferred/extension preview, not FantLab parity")
        return 0
    if not args or args[0] in {"-h", "--help"}:
        print("Scriptorium Reader — private text analysis and evidence-labelled literary reports")
        print("Usage: scriptorium <analyze|epub|batch|compare|diagnostic|evidence|n-evidence|site> [options]")
        print("  analyze     UTF-8 manuscript -> JSON, HTML, Markdown or CSV (29 metrics)")
        print("  epub        Local EPUB XHTML spine -> Reader reports and source-free identity")
        print("  batch       Explicit UTF-8 manifest -> private JSON/HTML reports and index")
        print("  compare     Two private analysis JSON files -> HTML, JSON or CSV; no uploads")
        print("  diagnostic  Curated historical diagnostic -> offline HTML")
        print("  evidence    Source-free FantLab metric deltas (requires repository checkout; M2 0/5)")
        print("  n-evidence  Retained native AOT/pylem N-only uncertainty bounds (M2 0/5)")
        print("  site        Build the canonical allow-listed site from a repository checkout")
        print("Run scriptorium <command> --help for command options.")
        return 0 if args else 2
    command, rest = args[0], args[1:]
    if command == "diagnostic":
        return diagnostic_main(rest)
    module = COMMANDS.get(command)
    if module is None:
        print("Unknown command. Run scriptorium --help.", file=sys.stderr)
        return 2
    return importlib.import_module(module).main(rest)
