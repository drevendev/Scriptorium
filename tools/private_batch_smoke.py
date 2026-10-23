"""Installed-wheel end-to-end batch smoke; run outside the repository checkout."""
from __future__ import annotations

import csv
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    checkout = Path(sys.argv[1]).resolve()
    assert not Path.cwd().resolve().is_relative_to(checkout), "run this smoke outside checkout"
    cli = Path(sys.executable).parent / "scriptorium"
    assert cli.is_file(), "installed console script required"

    with tempfile.TemporaryDirectory(prefix="scriptorium-batch-smoke-") as private:
        root = Path(private)
        inputs = root / "inputs"
        inputs.mkdir()
        a = "Кот идёт. Пёс спит!".encode("utf-8")
        b = "Ветер шумит. Волны движутся.".encode("utf-8")
        (inputs / "a.txt").write_bytes(a)
        (inputs / "b.txt").write_bytes(b)
        manifest = inputs / "manifest.json"
        data = {"schema_version": "scriptorium-private-batch-manifest-v1",
                "files": ["a.txt", "b.txt", "a.txt"]}
        manifest.write_text(json.dumps(data), encoding="utf-8")
        out = root / "private-reports"

        def command():
            return subprocess.run(
                [str(cli), "batch", str(manifest), "--output-dir", str(out)],
                cwd=root, capture_output=True, text=True, check=False,
            )

        first = command()
        assert first.returncode == 0, ("installed batch failed", first.stderr)
        json_indexes = sorted(out.glob("batch-*.json"))
        assert len(json_indexes) == 1
        index = json.loads(json_indexes[0].read_text(encoding="utf-8"))
        assert (index["completed"], index["failed"]) == (3, 0)
        assert index["source_text_embedded"] is False
        assert index["entries"][0]["reports"] == index["entries"][2]["reports"]
        assert index["entries"][0]["raw_sha256"] == sha256(a).hexdigest()
        assert index["entries"][1]["raw_sha256"] == sha256(b).hexdigest()
        assert len(list(out.glob("work-*.json"))) == 2
        assert len(list(out.glob("work-*.html"))) == 2
        html_index = next(out.glob("batch-*.html")).read_text(encoding="utf-8")
        csv_index = next(out.glob("batch-*.csv"))
        assert len(list(csv.DictReader(csv_index.open(encoding="utf-8", newline="")))) == 3
        for row in index["entries"]:
            for route in row["reports"].values():
                assert route == Path(route).name
                assert (out / route).is_file(), "missing linked report"
            assert row["reports"]["html"] in html_index
            artifact = json.loads((out / row["reports"]["json"]).read_text(encoding="utf-8"))
            assert artifact["schema_version"] == "scriptorium-local-analysis-v1"
            assert len(artifact["metrics"]) == 29

        snapshot = {p.name: p.read_bytes() for p in out.iterdir()}
        assert command().returncode == 0, "same manifest must be a safe retry"
        assert snapshot == {p.name: p.read_bytes() for p in out.iterdir()}
        private_outputs = b"".join(snapshot.values())
        assert a not in private_outputs and b not in private_outputs
        assert str(root).encode() not in private_outputs

        (inputs / "bad.txt").write_bytes(b"\xff")
        data["files"] = ["a.txt", "bad.txt", "missing.txt"]
        manifest.write_text(json.dumps(data), encoding="utf-8")
        failed = command()
        assert failed.returncode == 1, ("partial errors must be explicit", failed.stderr)
        latest = next(p for p in out.glob("batch-*.json") if p not in json_indexes)
        result = json.loads(latest.read_text(encoding="utf-8"))
        assert result["completed"] == 1 and result["failed"] == 2
        assert all(row["reports"] is None for row in result["entries"][1:])
        assert snapshot[json_indexes[0].name] == json_indexes[0].read_bytes()

        # Conflicting report content must not overwrite anything.
        report = out / index["entries"][0]["reports"]["json"]
        report.write_bytes(b"conflicting existing output")
        rejected = command()
        assert rejected.returncode == 2
        assert b"conflicting existing output" == report.read_bytes()
        assert str(root) not in rejected.stderr
    print("installed private batch: real analyzer, 2 works, duplicate, partial errors, collision, retry PASS")


if __name__ == "__main__":
    main()
