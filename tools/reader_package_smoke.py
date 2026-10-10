"""Run with the installed wheel, outside the checkout; no manuscript is retained."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    repo = Path(sys.argv[1]).resolve()
    import scriptorium
    package = Path(scriptorium.__file__).resolve()
    assert not package.is_relative_to(repo), "smoke test imported checkout instead of installed wheel"
    for name in ("analyze_deterministic_metrics", "analyze_pos_metrics", "normalize_text", "word_tokens"):
        assert callable(getattr(scriptorium, name)), f"public API missing: {name}"
    def run(*args):
        return subprocess.run([sys.executable, "-m", "scriptorium", *map(str, args)],
                              check=True, capture_output=True, text=True, timeout=60)
    assert "0.2.0a1" in run("--version").stdout
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "private.txt"
        raw = "Кот идёт. Пёс спит!\n— Да? — спросил он.".encode("utf-8")
        source.write_bytes(raw)
        for kind in ("json", "html", "csv"):
            run("analyze", source, "--format", kind, "--output", root / f"report.{kind}")
            assert "Кот идёт" not in (root / f"report.{kind}").read_text(encoding="utf-8")
        data = json.loads((root / "report.json").read_text(encoding="utf-8"))
        assert len(data["metrics"]) == 29
        assert data["source"]["raw_sha256"] == hashlib.sha256(raw).hexdigest()
        assert len(list(csv.DictReader(io.StringIO((root / "report.csv").read_text(encoding="utf-8"))))) == 29
        run("diagnostic", repo / "benchmarks/fantlab/work270306-wikisource-diagnostic.json",
            "--output", root / "historical.html")
        assert (root / "historical.html").read_text(encoding="utf-8").count('scope="row"') == 28
        run("site", "--repo-root", repo, "--output", root / "site")
        assert (root / "site/works/anna-karenina-full-work-diagnostic/index.html").is_file()
        assert "anna-karenina-full-work-diagnostic" in (root / "site/index.html").read_text(encoding="utf-8")
    print("Installed Reader smoke PASS: public API, 29 metrics, JSON/HTML/CSV, historical report and canonical site")


if __name__ == "__main__":
    main()
