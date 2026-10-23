"""Private, deterministic, create-only batch analysis for explicit UTF-8 manifests.

POSIX dir-fd anchoring is intentional: never follow input/output path symlinks.
No source bytes or absolute private paths are emitted in derived artifacts.
"""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from html import escape
import io
import json
import os
from pathlib import Path
import secrets
import stat
import sys

from .analyze import MAX_ANALYSIS_BYTES, build_local_analysis, render_html

MANIFEST_SCHEMA = "scriptorium-private-batch-manifest-v1"
INDEX_SCHEMA = "scriptorium-private-batch-index-v1"
MAX_MANIFEST_BYTES = 64 * 1024
MAX_ITEMS = 16
MAX_TOTAL_BYTES = 64 * 1024 * 1024
_DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
_FILE_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)


class BatchError(ValueError):
    """A controlled, path-free error message."""


def _unique_pairs(pairs):
    value = {}
    for key, entry in pairs:
        if key in value:
            raise BatchError("duplicate manifest JSON key")
        value[key] = entry
    return value


def _reject_constant(_):
    raise BatchError("nonfinite manifest JSON value")


def _relative_parts(raw):
    if not isinstance(raw, str) or not raw or len(raw) > 1024 or "\\" in raw or "\x00" in raw:
        raise BatchError("manifest entries must be bounded relative POSIX paths")
    parts = raw.split("/")
    if any(part in ("", ".", "..") for part in parts) or raw.startswith("/"):
        raise BatchError("manifest entries must not traverse directories")
    return parts


def _open_directory(path):
    """Open every component without following symlinks, binding subsequent I/O to its fd."""
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise BatchError("private batch requires POSIX no-follow directory operations")
    absolute = Path(os.path.abspath(path))
    fd = os.open("/", _DIR_FLAGS)
    try:
        for part in absolute.parts[1:]:
            next_fd = os.open(part, _DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def _read_at(root_fd, parts, limit):
    """Read one bounded regular file relative to an already opened trusted directory."""
    opened = []
    parent = root_fd
    fd = -1
    try:
        for component in parts[:-1]:
            next_fd = os.open(component, _DIR_FLAGS, dir_fd=parent)
            opened.append(next_fd)
            parent = next_fd
        fd = os.open(parts[-1], _FILE_FLAGS, dir_fd=parent)
        details = os.fstat(fd)
        if not stat.S_ISREG(details.st_mode) or details.st_size > limit:
            raise BatchError("input_not_regular_or_too_large")
        with os.fdopen(fd, "rb") as stream:
            fd = -1
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise BatchError("input_not_regular_or_too_large")
        return raw
    finally:
        if fd >= 0:
            os.close(fd)
        for directory in reversed(opened):
            os.close(directory)


def _load_manifest(root_fd, name):
    raw = _read_at(root_fd, [name], MAX_MANIFEST_BYTES)
    try:
        doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
                         parse_constant=_reject_constant)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BatchError("invalid UTF-8 manifest JSON") from exc
    if not isinstance(doc, dict) or set(doc) != {"schema_version", "files"}:
        raise BatchError("manifest must contain only schema_version and files")
    if doc["schema_version"] != MANIFEST_SCHEMA:
        raise BatchError("unsupported manifest schema")
    items = doc["files"]
    if not isinstance(items, list) or not (1 <= len(items) <= MAX_ITEMS):
        raise BatchError("manifest must list between 1 and 16 files")
    for item in items:
        _relative_parts(item)
    return raw, items


def _open_output_dir(path):
    absolute = Path(os.path.abspath(path))
    if absolute.name in ("", ".", "..") or absolute == Path("/"):
        raise BatchError("select a private report subdirectory")
    parent = _open_directory(absolute.parent)
    try:
        try:
            os.mkdir(absolute.name, mode=0o700, dir_fd=parent)
        except FileExistsError:
            pass
        fd = os.open(absolute.name, _DIR_FLAGS, dir_fd=parent)
    finally:
        os.close(parent)
    details = os.fstat(fd)
    if not stat.S_ISDIR(details.st_mode) or stat.S_IMODE(details.st_mode) & 0o077:
        os.close(fd)
        raise BatchError("report directory must not be accessible by group or others")
    return fd


def _publish(root_fd, filename, raw):
    """Write and fsync a private temp, atomically hard-link only if destination absent.

    A byte-identical existing result is a valid deterministic retry. Everything else
    is a conflict, never an invitation to overwrite another report or an index.
    """
    temporary = ".scriptorium-" + secrets.token_hex(16) + ".tmp"
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=root_fd)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, filename, src_dir_fd=root_fd,
                    dst_dir_fd=root_fd, follow_symlinks=False)
            os.fsync(root_fd)
        except FileExistsError:
            try:
                previous = _read_at(root_fd, [filename], len(raw))
            except (OSError, BatchError) as exc:
                raise BatchError("output_conflict") from exc
            if previous != raw:
                raise BatchError("output_conflict")
    finally:
        os.unlink(temporary, dir_fd=root_fd)


def _serialize_json(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def _render_csv(index):
    buffer = io.StringIO(newline="")
    columns = ("entry_id", "status", "error", "raw_sha256", "json_report", "html_report")
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for entry in index["entries"]:
        links = entry["reports"] or {}
        writer.writerow({
            "entry_id": entry["entry_id"],
            "status": entry["status"],
            "error": entry["error"] or "",
            "raw_sha256": entry["raw_sha256"] or "",
            "json_report": links.get("json", ""),
            "html_report": links.get("html", ""),
        })
    return buffer.getvalue().encode("utf-8")


def _render_html(index, stem):
    rows = []
    for entry in index["entries"]:
        label = escape(entry["entry_id"])
        status = escape(entry["status"])
        error = escape(entry["error"] or "—")
        digest = escape(entry["raw_sha256"] or "not available")
        route = entry["reports"]["html"] if entry["reports"] else None
        link = '<a href="' + escape(route, quote=True) + '">Read analysis</a>' if route else "Unavailable"
        rows.append(f'<tr><th scope="row">{label}</th><td>{status}</td>'
                    f'<td><code>{digest}</code></td><td>{error}</td><td>{link}</td></tr>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Scriptorium · private batch</title><style>'
            f':root{{font:1rem/1.6 Georgia,serif;color-scheme:light dark}}'
            f'body{{max-width:75rem;margin:auto;padding:clamp(1rem,3vw,3rem)}}'
            f'h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15}}'
            f'table{{border-collapse:collapse;width:100%;font:0.9rem/1.5 system-ui,sans-serif}}'
            f'th,td{{text-align:left;padding:.75rem;border-bottom:1px solid currentColor}}'
            f'.scroll{{overflow-x:auto}}a{{display:inline-block;min-height:44px;padding:.6rem 0}}'
            f'code{{overflow-wrap:anywhere}}*:focus-visible{{outline:3px solid currentColor;outline-offset:3px}}'
            f'@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}'
            f'</style></head><body><main><p>Scriptorium · offline workbench</p>'
            f'<h1>Private batch analysis</h1>'
            f'<p>{index["completed"]} analyzed · {index["failed"]} unavailable. '
            f'Text stays local. Rows are inferred or extension metrics, not FantLab parity. '
            f'Short works are valid but limited for author profiles; corpus admission is separate.</p>'
            f'<p><a href="{stem}.json">JSON index</a> · <a href="{stem}.csv">CSV index</a></p>'
            f'<div class="scroll" role="region" tabindex="0" aria-label="Batch results">'
            f'<table><caption>Manifest entry outcomes</caption><thead><tr>'
            f'<th scope="col">Work</th><th scope="col">Status</th><th scope="col">SHA-256</th>'
            f'<th scope="col">Reason</th><th scope="col">Report</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            f'<p>Hashes and values are locally computed, not independent proof of provenance. '
            f'No source text, source filename or absolute path is stored here.</p>'
            f'</main></body></html>\n').encode("utf-8")


def run(manifest, output_dir):
    root = _open_directory(Path(manifest).parent)
    try:
        manifest_raw, paths = _load_manifest(root, Path(manifest).name)
        prepared = {}
        entries = []
        used_bytes = 0
        for position, path in enumerate(paths, 1):
            entry = {"entry_id": f"item-{position:04d}", "status": "error",
                     "error": None, "raw_sha256": None, "reports": None}
            try:
                raw = _read_at(root, _relative_parts(path), MAX_ANALYSIS_BYTES)
                if used_bytes + len(raw) > MAX_TOTAL_BYTES:
                    raise BatchError("total_input_limit_exceeded")
                used_bytes += len(raw)
                digest = sha256(raw).hexdigest()
                entry["raw_sha256"] = digest
                if digest not in prepared:
                    try:
                        artifact = build_local_analysis(raw)
                        prepared[digest] = {
                            "json": _serialize_json(artifact),
                            "html": render_html(artifact).encode("utf-8"),
                        }
                    except (UnicodeError, ValueError, TypeError, OverflowError) as exc:
                        raise BatchError("analysis_failed_or_invalid_utf8") from exc
                entry["reports"] = {
                    "json": f"work-{digest}.json",
                    "html": f"work-{digest}.html",
                }
                entry["status"] = "ok"
            except (BatchError, OSError) as exc:
                entry["error"] = str(exc) if isinstance(exc, BatchError) else "input_unreadable"
            entries.append(entry)
    finally:
        os.close(root)

    index = {
        "schema_version": INDEX_SCHEMA,
        "manifest_sha256": sha256(manifest_raw).hexdigest(),
        "source_text_embedded": False,
        "completed": sum(row["status"] == "ok" for row in entries),
        "failed": sum(row["status"] == "error" for row in entries),
        "entries": entries,
    }
    stem = "batch-" + index["manifest_sha256"][:16]
    folder = _open_output_dir(output_dir)
    try:
        for digest in sorted(prepared):
            for kind in ("json", "html"):
                _publish(folder, f"work-{digest}.{kind}", prepared[digest][kind])
        # A complete JSON index is committed last; a crash before it can be retried.
        _publish(folder, stem + ".csv", _render_csv(index))
        _publish(folder, stem + ".html", _render_html(index, stem))
        _publish(folder, stem + ".json", _serialize_json(index))
    finally:
        os.close(folder)
    return index["failed"] != 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Analyze up to 16 explicitly named UTF-8 files locally. No uploads.")
    parser.add_argument("manifest", type=Path, help="manifest JSON; paths are relative to its directory")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="private directory for create-only reports and indexes")
    args = parser.parse_args(argv)
    try:
        return int(run(args.manifest, args.output_dir))
    except (BatchError, OSError, TypeError, ValueError, RecursionError):
        parser.error("batch rejected: invalid manifest, insecure paths, or output conflict")


if __name__ == "__main__":
    sys.exit(main())
