"""Exercise an installed Reader outside its checkout, with real analyzer reports."""
from __future__ import annotations

import csv
from decimal import Decimal
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def run(*args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    process = subprocess.run([sys.executable, '-I', '-m', 'scriptorium', *args],
                             capture_output=True, text=True, timeout=30)
    if ok and process.returncode:
        raise AssertionError('installed Reader command failed: ' + process.stderr)
    if not ok and not process.returncode:
        raise AssertionError('invalid report was accepted')
    return process


def main() -> None:
    import scriptorium
    from scriptorium.compare import build_comparison, load_report

    checkout = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else None
    location = Path(scriptorium.__file__).resolve()
    if checkout and location.is_relative_to(checkout):
        raise AssertionError('smoke must import the installed wheel, not the checkout')
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        texts = ('Кот спит. Кот и пёс гуляют!\n— Да? — сказал пёс.',
                 'Кот, кот, кот!\n— А? — ответил он.')
        paths = []
        for index, text in enumerate(texts):
            source, report = root / f'private-{index}.txt', root / f'analysis-{index}.json'
            source.write_text(text, encoding='utf-8')
            run('analyze', str(source), '--output', str(report))
            paths.append(report)
        a, b = map(load_report, paths)
        expected = build_comparison(a, b)
        values = {}
        for fmt in ('json', 'html', 'csv'):
            output = root / f'comparison.{fmt}'
            run('compare', *map(str, paths), '--format', fmt, '--output', str(output))
            payload = output.read_text(encoding='utf-8')
            values[fmt] = payload
            assert not any(text in payload for text in texts)
            assert payload == run('compare', *map(str, paths), '--format', fmt).stdout
            failure = run('compare', *map(str, paths), '--format', fmt, '--output', str(output), ok=False)
            assert output.read_text(encoding='utf-8') == payload
            assert str(root) not in failure.stderr
        result = json.loads(values['json'])
        assert result == expected and len(result['metrics']) == 29
        csv_rows = list(csv.DictReader(io.StringIO(values['csv'])))
        assert len(csv_rows) == 29 and values['html'].count("scope='row'") == 29
        for row, exported in zip(result['metrics'], csv_rows):
            assert row['metric_id'] == exported['metric_id']
            assert (row['difference'] or '') == exported['difference']
            if row['comparison_status'] == 'comparable':
                assert Decimal(row['difference']) == Decimal(row['right']) - Decimal(row['left'])
        assert 'unauthenticated declarations' in values['html']
        assert "<th scope='col'>Unit</th>" in values['html']
        forged = json.loads(paths[0].read_text())
        forged['metrics']['fantlab.general.mean_word_length_chars']['value'] = 100000
        bad = root / 'private-invalid-report.json'
        bad.write_text(json.dumps(forged))
        failed_output = root / 'should-not-exist.json'
        failure = run('compare', str(bad), str(paths[1]), '--output', str(failed_output), ok=False)
        assert not failed_output.exists() and str(root) not in failure.stderr
    print('Installed private comparison PASS: real analyzer, 29 metrics, HTML/JSON/CSV, exact deltas, deterministic create-only exports and invalid-report rejection')


if __name__ == '__main__':
    main()
