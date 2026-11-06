"""Replay a private analysis against its original bytes; never upload manuscripts.

The saved report is an untrusted declaration, not authenticated provenance or a
FantLab reference. Only an exact current-engine replay is reported as PASS.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyze import (
    LOCAL_ANALYSIS_SCHEMA, MAX_ANALYSIS_BYTES, MAX_DICTIONARY_BYTES,
    LocalInputError, _read_bounded_regular_file, _read_bounded_stdin,
    build_local_analysis,
)
from .epub import EpubError, MAX_ARCHIVE_BYTES, extract_epub

MAX_REPORT_BYTES = 2 * 1024 * 1024


class VerificationError(ValueError):
    """Controlled message without input paths or manuscript fragments."""


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("duplicate report JSON key")
        result[key] = value
    return result


def _reject_constant(_):
    raise VerificationError("non-finite report JSON number")


def _canonical_json(value):
    # Also rejects float infinity created from a JSON exponent such as 1e999;
    # bool, int and float stay different despite Python equality semantics.
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False)


def verify_private_report(source_bytes: bytes, report_bytes: bytes, *,
                          dictionary_bytes: bytes | None = None,
                          dictionary_profile: str | None = None) -> None:
    """Raise unless all 29 metrics, source identities and profiles replay exactly.

    The optional saved revision is replayed as a declaration only: a JSON file
    cannot authenticate a Git commit, a rights grant or a FantLab input.
    """
    try:
        saved = json.loads(report_bytes.decode("utf-8"),
                           object_pairs_hook=_unique_pairs,
                           parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise VerificationError("report must be valid UTF-8 JSON") from exc
    if not isinstance(saved, dict) or saved.get("schema_version") != LOCAL_ANALYSIS_SCHEMA:
        raise VerificationError("unsupported local analysis report")
    source = saved.get("source")
    analyzer = saved.get("analyzer")
    if (not isinstance(source, dict) or source.get("source_text_embedded") is not False
            or not isinstance(analyzer, dict)
            or not isinstance(analyzer.get("dependencies"), dict)):
        raise VerificationError("invalid source-free report")
    revision = analyzer.get("scriptorium_revision")
    if revision is not None and (not isinstance(revision, str) or not revision.strip()):
        raise VerificationError("invalid revision declaration")
    declared_dictionary = analyzer["dependencies"].get("vocabulary_dictionary")
    if (dictionary_bytes is None) != (dictionary_profile is None):
        raise VerificationError("dictionary and profile must be supplied together")
    if (declared_dictionary is None) != (dictionary_bytes is None):
        raise VerificationError("dictionary inputs do not match saved report")
    words = None
    if dictionary_bytes is not None:
        try:
            words = dictionary_bytes.decode("utf-8").splitlines()
        except UnicodeDecodeError as exc:
            raise VerificationError("dictionary must be UTF-8") from exc
    try:
        actual = build_local_analysis(
            source_bytes, dictionary_words=words,
            dictionary_profile=dictionary_profile,
            scriptorium_revision=revision,
        )
        if _canonical_json(actual) != _canonical_json(saved):
            raise VerificationError("report differs from current analyzer replay")
    except UnicodeDecodeError as exc:
        raise VerificationError("manuscript must be UTF-8") from exc
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        if isinstance(exc, VerificationError):
            raise
        raise VerificationError("report could not be replayed safely") from exc


def verify_epub_provenance(
    report_bytes: bytes, receipt_bytes: bytes, extracted_provenance: dict[str, object],
) -> None:
    """Verify exact EPUB archive identity as well as its extracted-body report.

    An extracted-body hash alone cannot distinguish EPUB archives with identical
    spine text. This optional source-free sidecar is checked only *after* the
    report has been replayed against the actual extracted bytes.
    """
    try:
        receipt = json.loads(
            receipt_bytes.decode("utf-8"), object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
        report = json.loads(
            report_bytes.decode("utf-8"), object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
        expected = {
            **extracted_provenance,
            "normalized_sha256": report["source"]["normalized_sha256"],
            "analysis_schema": LOCAL_ANALYSIS_SCHEMA,
        }
        if _canonical_json(receipt) != _canonical_json(expected):
            raise VerificationError("EPUB provenance differs from original archive or extraction")
    except VerificationError:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError, TypeError,
            ValueError, KeyError, OverflowError) as exc:
        raise VerificationError("EPUB provenance must be valid source-free JSON") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Recompute a private JSON report from its original UTF-8 manuscript or EPUB.")
    parser.add_argument("text", type=Path, help="original UTF-8 file, - for piped stdin, or EPUB with --epub")
    parser.add_argument("report", type=Path, help="saved Scriptorium analyze/epub JSON")
    parser.add_argument("--epub", action="store_true",
                        help="extract and verify the original unencrypted EPUB spine in memory")
    parser.add_argument("--provenance", type=Path,
                        help="with --epub, also match the original archive against its source-free sidecar")
    parser.add_argument("--json", action="store_true",
                        help="print one source-free, machine-readable PASS record after successful replay")
    parser.add_argument("--dictionary", type=Path, help="same dictionary used in original run")
    parser.add_argument("--dictionary-profile", help="same dictionary profile as original run")
    args = parser.parse_args(argv)
    if (args.dictionary is None) != (args.dictionary_profile is None):
        parser.error("--dictionary and --dictionary-profile must be supplied together")
    if args.provenance is not None and not args.epub:
        parser.error("--provenance requires --epub")
    if args.epub and str(args.text) == "-":
        parser.error("--epub requires an original regular EPUB file")
    if args.epub and args.dictionary is not None:
        parser.error("EPUB reports do not support a vocabulary dictionary")
    try:
        if args.epub:
            archive = _read_bounded_regular_file(args.text, MAX_ARCHIVE_BYTES, "EPUB")
            raw, extracted_provenance = extract_epub(archive)
        else:
            raw = (_read_bounded_stdin(MAX_ANALYSIS_BYTES) if str(args.text) == "-"
                   else _read_bounded_regular_file(args.text, MAX_ANALYSIS_BYTES, "manuscript"))
        saved = _read_bounded_regular_file(args.report, MAX_REPORT_BYTES, "report")
        dictionary = (_read_bounded_regular_file(args.dictionary, MAX_DICTIONARY_BYTES, "dictionary")
                      if args.dictionary is not None else None)
        verify_private_report(raw, saved, dictionary_bytes=dictionary,
                              dictionary_profile=args.dictionary_profile)
        if args.provenance is not None:
            receipt = _read_bounded_regular_file(args.provenance, MAX_REPORT_BYTES, "EPUB provenance")
            verify_epub_provenance(saved, receipt, extracted_provenance)
    except (VerificationError, LocalInputError, EpubError) as exc:
        parser.error(str(exc))
    except (OSError, UnicodeError, TypeError, ValueError, OverflowError, RecursionError):
        parser.error("unable to verify private inputs")
    if args.json:
        print(json.dumps({
            "schema_version": "scriptorium-local-verification-v1",
            "status": "PASS",
            "replay_scope": "current-analyzer-only",
            "input_kind": "epub" if args.epub else "utf8-text",
            "verified_metric_count": 29,
            "archive_identity": ("VERIFIED" if args.provenance is not None else
                                 "NOT_CHECKED" if args.epub else "NOT_APPLICABLE"),
            "revision_authenticated": False,
            "edition_identity": "NOT_ESTABLISHED",
            "fantlab_parity": "NOT_ESTABLISHED",
        }, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    print("PASS: source hashes, all 29 metrics and current algorithm profiles replay exactly.")
    if args.epub:
        if args.provenance is not None:
            print("PASS: original EPUB archive SHA-256 and extraction provenance replay exactly.")
        else:
            print("EPUB input hash covers extracted UTF-8 spine text, not archive identity; use --provenance to check the archive.")
    print("Saved revision is an unverified declaration; this is NOT rights, edition, or FantLab parity proof.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
